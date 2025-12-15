"""
llm.py

Low-level LLM runtime for the project.
- Single agent identity
- Ollama-backed
- No task logic here
"""

import ollama
import time
from typing import Optional


DEFAULT_SYSTEM_PROMPT = """
You are a single autonomous coding agent.

You solve programming tasks by internally performing analysis,
planning, code generation, self-evaluation, and refinement.

You always act as one agent with one identity.
"""


def call_llm(
    *,
    user_prompt: str,
    model: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.0,
    max_retries: int = 2,
) -> str:
    """
    Core LLM call used by ALL agent nodes.

    This function:
    - Enforces single-agent identity
    - Handles retries
    - Returns raw text output
    """

    sys_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT

    for attempt in range(max_retries + 1):
        try:
            response = ollama.chat(
                model=model,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                options={
                    "temperature": temperature,
                },
            )
            return response["message"]["content"]

        except Exception as e:
            if attempt == max_retries:
                raise e
            time.sleep(0.5)

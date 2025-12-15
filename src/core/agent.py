"""
agent.py

Defines the single-agent cognitive steps.
Each function corresponds to ONE node in the LangGraph pipeline.
"""

from src.core.llm import call_llm


def analyze_task(*, signature: str, docstring: str, model: str) -> str:
    prompt = f"""
Analyze the following programming task.

- Extract required behavior
- Identify constraints
- Identify edge cases
- Do NOT write code

Function signature:
{signature}

Docstring:
{docstring}
"""
    return call_llm(user_prompt=prompt, model=model)


def plan_solution(*, analysis: str, model: str) -> str:
    prompt = f"""
Based on the analysis below, produce a clear step-by-step plan
to implement the function.

Analysis:
{analysis}
"""
    return call_llm(user_prompt=prompt, model=model)


def generate_code(*, signature: str, plan: str, model: str) -> str:
    prompt = f"""
Using the plan below, generate the Python function.

Constraints:
- Follow the function signature EXACTLY
- Do not include explanations
- Do not include markdown
- Output ONLY valid Python code

Function signature:
{signature}

Plan:
{plan}
"""
    return call_llm(user_prompt=prompt, model=model)


def review_code(*, code: str, model: str) -> str:
    prompt = f"""
Review the Python code below.

- Identify logical errors
- Identify missing edge cases
- Identify violations of the signature or docstring
- If the code appears correct, state that explicitly

Code:
{code}
"""
    return call_llm(user_prompt=prompt, model=model)


def refine_code(*, code: str, review: str, model: str) -> str:
    prompt = f"""
You previously generated this code:

{code}

You then produced this review:

{review}

If issues were identified, fix the code.
If no issues were found, return the code unchanged.

Constraints:
- Output ONLY the final Python code
"""
    return call_llm(user_prompt=prompt, model=model)

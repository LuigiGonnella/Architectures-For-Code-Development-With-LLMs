
from src.core.llm import call_llm


def generate_code(
    *,
    signature: str,
    plan: str,
    model: str,
    critic_feedback: str = None,
    exec_summary: str = None,
) -> str:
    """
    Generate code based on the implementation plan.
    Can incorporate feedback from critic and execution summary if available.
    
    """
    prompt = (
        "You are an expert Python engineer.\n"
        "Generate a complete and correct Python function strictly following the provided plan.\n\n"
        "ABSOLUTE RULES (NON-NEGOTIABLE):\n"
        "- Output ONLY valid Python code\n"
        "- Do NOT include explanations, comments, markdown, or extra text\n"
        "- Do NOT include imports unless strictly required by the plan\n"
        "- Do NOT change the function name, parameters, or order\n"
        "- Do NOT add helper functions unless explicitly implied by the plan\n"
        "- Do NOT print, log, or read input\n"
        "- The code must be directly executable\n\n"
        "CORRECTNESS REQUIREMENTS:\n"
        "- Handle all edge cases mentioned in the plan\n"
        "- Respect all constraints and assumptions\n"
        "- Prefer clarity and correctness over cleverness\n\n"
        "FUNCTION SIGNATURE (MUST MATCH EXACTLY):\n"
        f"{signature}\n\n"
        "IMPLEMENTATION PLAN:\n"
        f"{plan}\n\n"
    )

    # Include critic feedback
    if critic_feedback:
        prompt += (
            "CRITIC FEEDBACK FROM PREVIOUS ITERATIONS:\n"
            f"{critic_feedback}\n\n"
            "Address the issues and suggestions provided in the feedback above.\n\n"
        )

    # Include execution 
    if exec_summary:
        prompt += (
            "PREVIOUS EXECUTION SUMMARY:\n"
            f"{exec_summary}\n\n"
            "Learn from the previous execution results and fix any issues identified.\n\n"
        )

    prompt += (
        "FINAL CHECK BEFORE RESPONDING:\n"
        "- The output must start with 'def'\n"
        "- The output must contain exactly one function\n"
        "- No text before or after the code\n"
    )
    
    return call_llm(user_prompt=prompt, model=model)

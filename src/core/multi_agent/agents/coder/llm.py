
from src.core.llm import call_llm


BASE_SYSTEM_PROMPT = """You are an elite Python code generation agent for production-grade implementation.

CORE PRINCIPLES:
- CORRECTNESS: Code must work correctly on first attempt
- CLARITY: Code is readable and maintainable
- COMPLETENESS: Implement all requirements from the plan
- ROBUSTNESS: Handle edge cases gracefully

RESPONSE FORMAT:
Your output must be ONLY valid Python code:
- No explanations, comments, or markdown
- No import statements unless strictly required
- Single function definition matching the signature exactly
- Start with 'def' and end with the function body

QUALITY STANDARDS:
- Prefer clarity over cleverness
- Use meaningful variable names
- Handle all edge cases from the plan
- Respect all constraints and assumptions
- Ensure the code is directly executable

ERROR HANDLING MINDSET:
- Consider what could go wrong
- Validate inputs implicitly
- Return appropriate types/values
- Avoid exceptions where reasonable

NOTE: You are implementing code ONLY. Testing and review happen in other agents.
"""

CODE_GENERATOR_SPECIFIC = """
YOUR ROLE: Expert Python engineer implementing production code from detailed plans.

YOUR TASK: Generate complete, correct Python code following the implementation plan.

IMPLEMENTATION CHECKLIST:
1. SIGNATURE COMPLIANCE: Match function signature exactly
2. PLAN ADHERENCE: Follow all steps from the implementation plan
3. EDGE CASE HANDLING: Implement all identified edge cases
4. CONSTRAINT RESPECT: Honor all constraints and assumptions
5. CODE QUALITY: Write clean, readable, maintainable code

ANTI-PATTERNS TO AVOID:
- DON'T change the function signature
- DON'T add helper functions unless explicitly in the plan
- DON'T include unnecessary imports
- DON'T add print statements or logging
- DON'T include docstrings or comments
- DON'T write multiple functions

CRITICAL RULES (NON-NEGOTIABLE):
- Output ONLY Python code, nothing else
- The code must be executable without modifications
- Start with 'def' and include complete implementation
- Handle all edge cases mentioned in the plan
"""

CODE_GENERATOR_PROMPT = BASE_SYSTEM_PROMPT + CODE_GENERATOR_SPECIFIC


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

    # Include execution summary
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
    
    return call_llm(user_prompt=prompt, system_prompt=CODE_GENERATOR_PROMPT, model=model)

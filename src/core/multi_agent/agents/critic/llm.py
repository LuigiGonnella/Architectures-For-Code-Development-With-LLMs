from src.core.llm import call_llm

# ═══════════════════════════════════════════════════════════════════════
# CORRECTNESS ANALYZER
# ═══════════════════════════════════════════════════════════════════════

CORRECTNESS_SYSTEM_PROMPT = """You are an expert Software Architect and QA Lead focused on FUNCTIONAL CORRECTNESS.

Your goal is to rigorously review Python code against its specifications, plan, and execution results.

OBJECTIVES:
1. Functional Correctness (Highest Priority):
   - Analyze execution feedback to identify runtime errors or test failures.
   - Verify logic against the requirements stringently.
   - Spot missing edge case handling.

2. Constraint & Contract Compliance:
   - Ensure NO forbidden behavior: NO valid stdout/stderr output (unless asked), NO global variables.
   - Ensure exactly ONE function is defined.
   - Ensure function signature matches exactly.
   - Verify type hints compliance.

OUTPUT FORMAT:
Provide a structured analysis:
- STATUS: [PASSED / FAILED / WARNING]
- BUG_ANALYSIS: List specific logic errors or test failures.
- CONSTRAINT_CHECK: List any violations.
- EDGE_CASES: List missing or mishandled boundary conditions.

If execution failed, this is an AUTOMATIC FAILED status.
"""

def analyze_correctness(
    *,
    signature: str,
    docstring: str,
    plan: str,
    code: str,
    exec_summary: str | None,
    model: str,
) -> str:
    exec_block = (
        f"\nEXECUTION FEEDBACK (SUMMARY):\n{exec_summary}\n"
        if exec_summary
        else "\nEXECUTION FEEDBACK (SUMMARY):\nNo execution data available.\n"
    )

    prompt = f"""
TASK SPECIFICATION:
Signature: {signature}
Docstring: {docstring}

INTENDED PLAN:
{plan}

CANDIDATE CODE:
{code}
{exec_block}

Analyze the functional correctness and constraint compliance of the code.
"""
    return call_llm(
        system_prompt=CORRECTNESS_SYSTEM_PROMPT,
        user_prompt=prompt,
        model=model,
    )


# ═══════════════════════════════════════════════════════════════════════
# QUALITY REVIEWER
# ═══════════════════════════════════════════════════════════════════════

QUALITY_SYSTEM_PROMPT = """You are a Code Quality expert.

OBJECTIVES:
1. Code Quality Assessment:
   - Enforce clarity and maintenance standards.
   - Interpret quality metrics:
     * Cyclomatic Complexity: >10 is complex, >15 is very complex.
     * Maintainability Index: <60 is poor, <80 is moderate.

2. Code Structure:
   - Check for nested loops/conditions that can be flattened.
   - Check for clear variable naming.
   - Check for efficient logic.

OUTPUT FORMAT:
Provide a structured analysis:
- COMPLEXITY_STATUS: [ACCEPTABLE / TOO_COMPLEX]
- MAINTAINABILITY_STATUS: [ACCEPTABLE / NEEDS_REFACTORING]
- ISSUES: List specific style/complexity issues.
"""

def analyze_quality(
    *,
    code: str,
    quality_metrics: dict | None,
    model: str,
) -> str:
    qm_block = (
        f"\nQUALITY METRICS:\n{quality_metrics}\n"
        if quality_metrics
        else "\nQUALITY METRICS:\nNo metrics available.\n"
    )

    prompt = f"""
CANDIDATE CODE:
{code}
{qm_block}

Analyze the code quality, complexity, and maintainability.
"""
    return call_llm(
        system_prompt=QUALITY_SYSTEM_PROMPT,
        user_prompt=prompt,
        model=model,
    )


# ═══════════════════════════════════════════════════════════════════════
# FEEDBACK SYNTHESIZER
# ═══════════════════════════════════════════════════════════════════════

SYNTHESIZER_SYSTEM_PROMPT = """You are the Lead Critic for a code generation pipeline.
Synthesize the analysis from the Correctness and Quality experts into a final, actionable critique.

REVIEW GUIDELINES:
1. Prioritize fixes: Correctness > Edge Cases > Complexity > Readability.
2. If Correctness failed (execution logic bugs):
   - SKIP quality comments.
   - Focus 100% on fixing the bugs.
3. If Correctness passed but Quality failed:
   - Provide refactoring instructions.
4. Do NOT rewrite the full code. Provide specific instructions.

FORMAT:
### Analysis
[Summary: "CRITICAL FAILURE", "FUNCTIONAL BUT COMPLEX", or "CORRECT"]

### Critical Issues (Bugs & Constraints)
- [Correctness] ...
- [Constraint] ...

### Quality Review
[Skip if execution failed]
- [Complexity] ...

### Refinement Instructions (Step-by-Step)
1. [Line X] ...
2. [Line Y] ...
"""

def synthesize_feedback(
    *,
    correctness_analysis: str,
    quality_analysis: str,
    model: str,
) -> str:
    prompt = f"""
CORRECTNESS ANALYSIS:
{correctness_analysis}

QUALITY ANALYSIS:
{quality_analysis}

Synthesize the final critique based on the above analyses.
"""
    return call_llm(
        system_prompt=SYNTHESIZER_SYSTEM_PROMPT,
        user_prompt=prompt,
        model=model,
    )

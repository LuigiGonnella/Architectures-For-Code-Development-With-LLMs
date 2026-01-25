from src.core.multi_agent.agents.planner.state import AgentState
from src.core.llm import call_llm
from src.core.multi_agent.agents.planner.llm import (
    ARCHITECTURE_DESIGNER_PROMPT,
    extract_and_parse_json,
    compress_phase_output,
)
import json

def architecture_design_node(state: AgentState) -> AgentState:
    """
    Design optimal architecture: components, patterns, data structures.
    """
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║  PHASE 3: ARCHITECTURE DESIGN                            ║")
    print("╚══════════════════════════════════════════════════════════╝")

    requirements_summary = compress_phase_output(
        "requirements", state.get("requirements", {})
    )

    # Include feedback from quality review if this is a refinement iteration
    feedback_section = ""
    if state.get("quality_review") and state.get("iteration_count", 0) > 0:
        quality_review = state.get("quality_review", {})
        issues = quality_review.get("issues", [])
        if issues:
            issues_text = "\n".join(
                [
                    f"- [{i['severity']}] {i['description']}: {i['recommendation']}"
                    for i in issues[:5]
                ]
            )
            feedback_section = f"""

## Quality Review Feedback (Iteration {state.get('iteration_count', 0)})
The previous architecture had these issues:
{issues_text}

Please address these in your revised design.
"""

    user_prompt = f"""## Task
Design the optimal architecture to satisfy these requirements.

## Requirements
{requirements_summary}
{feedback_section}

## Your Mission
1. Decompose into single-responsibility components
2. Select appropriate design patterns with justification
3. Choose optimal data structures with O(n) analysis
4. Recommend specific algorithms
5. Design exception hierarchy
6. Define clear component interfaces

## Instructions
Think through design alternatives in <thinking> tags.
Consider trade-offs (performance vs complexity, memory vs speed).
Then provide your architecture in <output> tags as JSON.

## Design Principles
- Single Responsibility Principle
- Fail-fast with clear error messages
- Optimize for the common case
- Use standard library where possible
"""
    
    response = call_llm(
        user_prompt=user_prompt,
        system_prompt=ARCHITECTURE_DESIGNER_PROMPT,
        model=state["model"],
    )

    try:
        architecture = extract_and_parse_json(response)
        state["architecture"] = architecture

        if state.get("show_node_info"):
            components = architecture.get("components", [])
            print(f"\n🏗️  Components Designed: {len(components)}")
            for comp in components[:3]:  # Show first 3
                print(f"   • {comp.get('name')}: {comp.get('responsibility')}")
            print(
                f"📐 Design Patterns: {len(architecture.get('exception_hierarchy', []))}"
            )

    except json.JSONDecodeError as e:
        print(f"⚠️  JSON parse error: {e}")
        state["architecture"] = {"raw_response": response, "error": str(e)}
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(f"Architecture JSON parse failed: {str(e)}")

    return state

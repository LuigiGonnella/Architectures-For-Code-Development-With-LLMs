from src.core.multi_agent.agents.planner.state import AgentState
from src.core.llm import call_llm
from src.core.multi_agent.agents.planner.llm import (
    REQUIREMENTS_ENGINEER_PROMPT,
    extract_and_parse_json,
    compress_phase_output,
)
import json

def requirements_engineering_node(state: AgentState) -> AgentState:
    """
    Define comprehensive functional and non-functional requirements.
    """
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║  PHASE 2: REQUIREMENTS ENGINEERING                       ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # Use compressed summary for efficiency
    intent_summary = compress_phase_output(
        "intent_analysis", state.get("intent_analysis", {})
    )

    user_prompt = f"""## Task
Transform the following intent into comprehensive requirements.

## Intent Analysis
{intent_summary}

## Your Mission
1. Define functional requirements (what the code must do)
2. Specify non-functional requirements (performance, security, reliability)
3. List constraints (technical and business)
4. Identify edge cases and boundary conditions

## Instructions
Think step-by-step in <thinking> tags about what requirements are needed.
Then provide complete requirements in <output> tags as JSON.

## Remember
- Be specific with O(n) complexity bounds
- List exact input validation checks
- Consider security implications
- Think about failure scenarios
"""

    response = call_llm(
        user_prompt=user_prompt,
        system_prompt=REQUIREMENTS_ENGINEER_PROMPT,
        model=state["model"],
    )

    try:
        requirements = extract_and_parse_json(response)
        state["requirements"] = requirements

        if state.get("show_node_info"):
            func_count = len(requirements.get("functional", []))
            edge_count = len(requirements.get("edge_cases", []))
            print(f"\n📝 Functional Requirements: {func_count}")
            print(
                f"⚡ Performance Constraints: {requirements.get('non_functional', {}).get('performance', {})}"
            )
            print(
                f"🔒 Security Requirements: {len(requirements.get('non_functional', {}).get('security', []))}"
            )
            print(f"🧪 Edge Cases Identified: {edge_count}")

    except json.JSONDecodeError as e:
        print(f"⚠️  JSON parse error: {e}")
        state["requirements"] = {"raw_response": response, "error": str(e)}
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append(f"Requirements JSON parse failed: {str(e)}")

    return state

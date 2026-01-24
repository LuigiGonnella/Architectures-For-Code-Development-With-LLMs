from src.core.multi_agent.agents.critic.state import CriticAgentState
from src.core.multi_agent.agents.critic.llm import analyze_quality

def quality_reviewer_node(state: CriticAgentState) -> CriticAgentState:
    """
    Review code quality and metrics.
    """
    if not state.get("should_proceed"):
        return state

    # Optimization: If correctness analysis found critical failures, 
    # we might skip quality review to save tokens/time, or we can just proceed.
    # The synthesizer will handle priority. 
    # However, getting quality feedback is still useful unless code is completely broken.

    if state.get("show_node_info"):
        print("Reviewing quality...")

    analysis = analyze_quality(
        code=state["code"],
        quality_metrics=state.get("quality_metrics"),
        model=state["model"],
    )

    state["quality_analysis"] = analysis
    return state

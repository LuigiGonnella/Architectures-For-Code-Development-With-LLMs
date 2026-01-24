from src.core.multi_agent.agents.critic.state import CriticAgentState
from src.core.multi_agent.agents.critic.llm import synthesize_feedback

def feedback_synthesizer_node(state: CriticAgentState) -> CriticAgentState:
    """
    Synthesize final feedback from analyses.
    """
    if not state.get("should_proceed"):
        return state

    if state.get("show_node_info"):
        print("Synthesizing feedback...")

    # If any analysis is missing, we can't synthesize properly.
    if not state.get("correctness_analysis") or not state.get("quality_analysis"):
        state["feedback"] = "Error: Incomplete analysis."
        return state

    feedback = synthesize_feedback(
        correctness_analysis=state["correctness_analysis"],
        quality_analysis=state["quality_analysis"],
        model=state["model"],
    )

    state["feedback"] = feedback
    
    if state.get("show_node_info"):
        print("Critique generation complete.")

    return state

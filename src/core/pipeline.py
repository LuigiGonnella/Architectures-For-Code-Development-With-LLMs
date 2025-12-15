from langgraph.graph import StateGraph, START, END
from src.core.state import AgentState
from src.core import agent


def analysis_node(state: AgentState) -> AgentState:
    print(">> ANALYSIS NODE")
    state["analysis"] = agent.analyze_task(
        signature=state["signature"],
        docstring=state["docstring"],
        model=state["model"],
    )
    return state


def planning_node(state: AgentState) -> AgentState:
    print(">> PLANNING NODE")
    state["plan"] = agent.plan_solution(
        analysis=state["analysis"],
        model=state["model"],
    )
    return state


def generation_node(state: AgentState) -> AgentState:
    print(">> GENERATION NODE")
    state["code"] = agent.generate_code(
        signature=state["signature"],
        plan=state["plan"],
        model=state["model"],
    )
    return state


def review_node(state: AgentState) -> AgentState:
    print(">> REVIEW NODE")
    state["review"] = agent.review_code(
        code=state["code"],
        model=state["model"],
    )
    return state


def refinement_node(state: AgentState) -> AgentState:
    print(">> REFINEMENT NODE")
    state["code"] = agent.refine_code(
        code=state["code"],
        review=state["review"],
        model=state["model"],
    )
    return state


def build_single_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("analysis", analysis_node)
    graph.add_node("planning", planning_node)
    graph.add_node("generation", generation_node)
    graph.add_node("review", review_node)
    graph.add_node("refinement", refinement_node)

    graph.add_edge(START, "analysis")
    graph.add_edge("analysis", "planning")
    graph.add_edge("planning", "generation")
    graph.add_edge("generation", "review")
    graph.add_edge("review", "refinement")
    graph.add_edge("refinement", END)

    return graph.compile()

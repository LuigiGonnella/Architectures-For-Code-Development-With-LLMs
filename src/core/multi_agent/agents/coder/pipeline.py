from langgraph.graph import StateGraph, START, END
from src.core.multi_agent.agents.coder.state import CoderAgentState
from src.core.multi_agent.agents.coder.llm import generate_code
from src.utils.code_parser import extract_python_code


def code_generation_node(state: CoderAgentState) -> CoderAgentState:
    """
    Generate code based on the implementation plan.
    
    """
  
    try:
        raw_code = generate_code(
            signature=state["signature"],
            plan=state["plan"],
            model=state["model"],
            critic_feedback=state.get("critic_feedback"),
            exec_summary=state.get("exec_summary"),
        )
        
        # Extract Python code from the response
        extracted = extract_python_code(raw_code)
        if extracted is None:
            error_msg = "Failed to extract valid Python code from generation output"
            state["errors"] = state.get("errors", []) + [error_msg]
            print(f"⚠️  {error_msg}")
            return state
        
        state["code"] = extracted
        
        if state.get("show_node_info"):
            lines = extracted.split('\n')
            preview = '\n'.join(lines[:5]) + (f"\n... ({len(lines)} lines total)" if len(lines) > 5 else "")
            print(f"✓  Generated Code:\n{preview}\n")
    
    except Exception as e:
        error_msg = f"Code generation error: {str(e)}"
        state["errors"] = state.get("errors", []) + [error_msg]
        print(f"✗  {error_msg}")
    
    return state

def build_coder_graph():
    """
    Build the LangGraph for the coder agent.
    
    Returns:
        Compiled LangGraph workflow
    """
    graph = StateGraph(CoderAgentState)
    
    # Add single code generation node
    graph.add_node("code_generation", code_generation_node)
    
    # Connect edges
    graph.add_edge(START, "code_generation")
    graph.add_edge("code_generation", END)
    
    return graph.compile()

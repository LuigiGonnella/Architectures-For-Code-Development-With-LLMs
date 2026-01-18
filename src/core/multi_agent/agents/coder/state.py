from typing_extensions import TypedDict
from typing import Optional, List


class CoderAgentState(TypedDict):
    """
    State for the coder agent.
    Tracks code generation workflow from plan to generated code.
    """
    
    # ═══ INPUT ═══
    task_id: str
    signature: str
    plan: str
    model: str
    show_node_info: Optional[bool]
    
    # ═══ ITERATION FEEDBACK ═══
    critic_feedback: Optional[str]
    exec_summary: Optional[str]
    
    # ═══ OUTPUT ═══
    code: Optional[str]
    
    # ═══ METADATA ═══
    errors: Optional[List[str]]

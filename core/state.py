from typing import TypedDict, Annotated, List, Optional, Dict, Tuple, Any
import pandas as pd
import operator

class GraphState(TypedDict):
    """Represents the state of our graph."""
    target: str
    # raw data
    raw_data_path: str
    raw_data: Optional[Dict[str, Any]] = None
    raw_data_description: Optional[str] = None
    raw_data_info: Optional[Dict[str, Any]] = None
    raw_data_samples: Optional[Dict[str, Any]] = None
    # analysis parameters
    analysis_params: Optional[dict] = None
    # validated data
    validated_data_path: Optional[str] = None
    validated_data: Optional[Dict[str, Any]] = None
    validated_data_description: Optional[str] = None
    validated_data_info: Optional[Dict[str, Any]] = None
    # analysis plan
    analysis_plan: Optional[List[str]] = None
    current_step: Optional[str] = None
    past_steps: Annotated[List[Tuple[str, str]], operator.add] = []  # List of (step, result) tuples
    step_index: Optional[int] = None
    # generated code
    generated_code: Optional[str] = None
    execution_stdout: Optional[str] = None
    execution_stderr: Optional[str] = None
    generated_files: Optional[List[str]] = None
    # analysis summary
    analysis_summary: Optional[str] = None
    report_content: Optional[str] = None
    error_message: Optional[str] = None
    # user feedback
    user_feedback: Optional[str] = None  # Store user input from HITL
    agent_outcome: Optional[str] = None  # Latest agent execution result for routing decisions
    # human in the loop
    pending_human_input: Optional[bool] = False  # Flag to indicate when human input is needed
    human_feedback_request: Optional[str] = None  # Question to ask the human
    human_feedback_response: Optional[str] = None  # Human's response
    # visualization tracking
    visualizations: Optional[List[Dict[str, Any]]] = []  # Track generated visualizations
    visualization_paths: Optional[List[str]] = []  # Paths to saved visualization files
    # analysis metrics
    analysis_metrics: Optional[Dict[str, Any]] = {}  # Store analysis metrics and results
    # state management
    analysis_status: Optional[str] = "not_started"  # Track overall status (not_started, in_progress, human_review, completed, error)
    interruption_reason: Optional[str] = None  # Reason why process was paused for human input

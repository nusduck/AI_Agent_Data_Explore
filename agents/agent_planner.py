from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from core.model import LanguageModelManager, ModelType
from utils.logger import setup_logger
from typing import List, Dict, Any, Tuple, Union, cast, Optional, Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from tools.python_executor import create_python_repl_tool
from core.state import GraphState
import operator
import asyncio
import os
import re
import glob
import matplotlib
import uuid
matplotlib.use('Agg')  # Use non-interactive backend

logger = setup_logger("agent_planner.log")

model_manager = LanguageModelManager()

llm = model_manager.get_model(ModelType.OPENAI_O3)
stronger_llm = model_manager.get_model(ModelType.OPENAI_4O)

# Define data analysis tools
python_tool = create_python_repl_tool()
tools = [python_tool]

# Ensure output directories exist
os.makedirs("outputs/visualizations", exist_ok=True)

# Create execution agent
execution_prompt = """You are a helpful data analysis assistant. Your task is to help with data analysis and visualization. Execute the tasks precisely as instructed.

Follow these guidelines for visualizations:
1. For each visualization, save the figure to a file using: plt.savefig('outputs/visualizations/viz_name.png', dpi=300, bbox_inches='tight')
2. Always include clear titles, labels, and legends in your visualizations
3. Use appropriate color schemes for different types of data
4. For time series data, use line charts with proper date formatting
5. For categorical comparisons, use bar charts or box plots
6. Always close the figure after saving it using plt.close()

Use seaborn and plotly for more advanced visualizations when appropriate.
"""

execution_agent = create_react_agent(llm, tools, prompt=execution_prompt)

# Define planning models
class AnalysisPlan(BaseModel):
    """Plan for data analysis and visualization"""
    steps: List[str] = Field(
        description="different steps to follow for data analysis and visualization, in sequential order"
    )

class Response(BaseModel):
    """Response to user."""
    response: str

class Act(BaseModel):
    """Action to perform."""
    action: Union[Response, AnalysisPlan] = Field(
        description="Action to perform. If you want to respond to user with a final answer, use Response. "
        "If you need to further use tools to complete the analysis, use AnalysisPlan."
    )

class HumanInputRequest(BaseModel):
    """Request for human input during analysis"""
    question: str = Field(description="Question to ask the human")
    context: str = Field(description="Context about the current state of the analysis")

# Create planning prompts
planner_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """For the given objective, develop a detailed step-by-step plan for data analysis and visualization.
        
This plan should include specific tasks such as:
1. Loading and examining the dataset
2. Data cleaning and preprocessing
3. Exploratory data analysis
4. Statistical analysis if needed
5. Creating appropriate visualizations
6. Interpreting results

Make sure each step is clear, specific, and provides all information needed for execution.
The final step should produce the desired analysis outcome or visualization.
Do not add unnecessary steps and focus on the specific analysis goals.
"""
    ),
    ("user", "{objective}"),
])

replanner_prompt = ChatPromptTemplate.from_template(
    """For the given data analysis objective, update your plan based on what has been done so far.

Your objective was:
{objective}

Your original plan was:
{plan}

You have currently completed these steps:
{past_steps}

Human feedback (if any): {user_feedback}

Update your plan accordingly. If no more steps are needed and you can return the final analysis results, respond with that. 
Otherwise, provide only the steps that still NEED to be done (do not include previously completed steps).
"""
)

human_input_prompt = ChatPromptTemplate.from_template(
    """Based on the current state of the data analysis, formulate a clear question to ask the human for guidance.

Current objective: {objective}
Current plan: {plan}
Completed steps: {past_steps}
Current issue or uncertainty: {issue}

Formulate a specific question that will help you proceed with the analysis. 
Provide enough context about what has been done so far and what assistance you need.
"""
)

planner = planner_prompt | stronger_llm.with_structured_output(AnalysisPlan)
replanner = replanner_prompt | stronger_llm.with_structured_output(Act)
human_input_requester = human_input_prompt | stronger_llm.with_structured_output(HumanInputRequest)

def find_visualization_paths(content: str) -> List[str]:
    """Extract visualization file paths from agent response content"""
    # Look for references to saved visualization files
    viz_paths = []
    
    # Pattern to find saved visualization files in the agent output
    patterns = [
        r"plt\.savefig\(['\"](.*?)['\"]",
        r"saved (?:the )?(?:plot|figure|visualization|chart) (?:to|as) ['\"](.*?)['\"]",
        r"saved (?:as|to) ['\"](.*?\.(?:png|jpg|jpeg|svg|pdf))['\"]",
        r"outputs/visualizations/[\w\d_-]+\.(?:png|jpg|jpeg|svg|pdf)"
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        viz_paths.extend(matches)
    
    # Check if the paths exist and normalize them
    existing_paths = []
    for path in viz_paths:
        # If the path doesn't have outputs/visualizations prefix, add it
        if not path.startswith("outputs/visualizations/"):
            normalized_path = os.path.join("outputs/visualizations", os.path.basename(path))
        else:
            normalized_path = path
        
        if os.path.exists(normalized_path):
            existing_paths.append(normalized_path)
    
    # If no specific paths were found in the output, check the directory for new files
    if not existing_paths:
        viz_files = glob.glob("outputs/visualizations/*.png") + \
                   glob.glob("outputs/visualizations/*.jpg") + \
                   glob.glob("outputs/visualizations/*.jpeg") + \
                   glob.glob("outputs/visualizations/*.svg") + \
                   glob.glob("outputs/visualizations/*.pdf")
        existing_paths.extend(viz_files)
    
    return existing_paths

# Define graph functions
async def plan_step(state: GraphState) -> Dict[str, Any]:
    """Create the initial analysis plan"""
    logger.info("Creating initial analysis plan")
    
    objective = state.get("user_feedback", "Analyze the provided data")
    if "raw_data_description" in state and state["raw_data_description"]:
        objective += f"\nData description: {state['raw_data_description']}"
    
    plan = await planner.ainvoke({"objective": objective})
    
    logger.info(f"Created plan with {len(plan.steps)} steps")
    return {
        "analysis_plan": plan.steps, 
        "current_step": plan.steps[0] if plan.steps else None,
        "analysis_status": "in_progress",
        "step_index": 0
    }

async def execute_step(state: GraphState) -> Dict[str, Any]:
    """Execute a single step in the analysis plan"""
    if not state.get("analysis_plan") or not state.get("current_step"):
        return {
            "error_message": "No analysis plan or current step available",
            "analysis_status": "error"
        }
    
    plan = state["analysis_plan"]
    plan_str = "\n".join(f"{i+1}. {step}" for i, step in enumerate(plan))
    current_step = state["current_step"]
    step_idx = state.get("step_index", plan.index(current_step))
    
    # Get existing visualization paths to track new ones
    existing_viz_paths = state.get("visualization_paths", [])
    
    # Prepare data loading instruction if needed
    data_loading_instruction = ""
    if "raw_data_path" in state and state["raw_data_path"]:
        file_path = state["raw_data_path"]
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == ".csv":
            data_loading_instruction = f"df = pd.read_csv('{file_path}')"
        elif file_ext in [".xlsx", ".xls"]:
            data_loading_instruction = f"df = pd.read_excel('{file_path}')"
        elif file_ext == ".json":
            data_loading_instruction = f"df = pd.read_json('{file_path}')"
        elif file_ext == ".parquet":
            data_loading_instruction = f"df = pd.read_parquet('{file_path}')"
    
    task_formatted = f"""For the following data analysis plan:
{plan_str}

You are tasked with executing step {step_idx+1}: {current_step}.

{data_loading_instruction}

If you need to create visualizations, save them to the 'outputs/visualizations/' directory with descriptive filenames.
For example: plt.savefig('outputs/visualizations/time_series_analysis.png', dpi=300, bbox_inches='tight')

Always include proper titles, axis labels, and legends in your visualizations.
"""

    logger.info(f"Executing step: {current_step}")
    
    try:
        agent_response = await execution_agent.ainvoke({"messages": [("user", task_formatted)]})
        
        # Extract the response content
        response_content = agent_response["messages"][-1].content
        
        # Find any visualization files created
        new_viz_paths = find_visualization_paths(response_content)
        
        # Update visualization paths - only add new ones
        updated_viz_paths = existing_viz_paths.copy()
        for path in new_viz_paths:
            if path not in updated_viz_paths:
                updated_viz_paths.append(path)
        
        # Update the state with the current progress
        next_step_idx = step_idx + 1
        next_step = plan[next_step_idx] if next_step_idx < len(plan) else None
        
        result = {
            "agent_outcome": response_content,
            "past_steps": [(current_step, response_content)],
            "step_index": next_step_idx,
            "current_step": next_step,
            "visualization_paths": updated_viz_paths
        }
        
        return result
    except Exception as e:
        logger.error(f"Error executing step: {str(e)}")
        return {
            "error_message": f"Error executing step: {str(e)}",
            "analysis_status": "error"
        }

async def replan_step(state: GraphState) -> Dict[str, Any]:
    """Update the plan based on execution results and human feedback"""
    logger.info("Replanning based on execution results and feedback")
    
    objective = state.get("user_feedback", "Analyze the provided data")
    if "raw_data_description" in state and state["raw_data_description"]:
        objective += f"\nData description: {state['raw_data_description']}"
    
    plan = state.get("analysis_plan", [])
    past_steps = state.get("past_steps", [])
    user_feedback = state.get("user_feedback", "")
    human_feedback = state.get("human_feedback_response", "")
    
    if human_feedback:
        user_feedback = f"{user_feedback}\nHuman feedback: {human_feedback}"
    
    # Format past steps for the prompt
    past_steps_formatted = "\n".join([f"Step: {step}\nResult: {result}" for step, result in past_steps])
    
    output = await replanner.ainvoke({
        "objective": objective,
        "plan": plan,
        "past_steps": past_steps_formatted,
        "user_feedback": user_feedback
    })
    
    if isinstance(output.action, Response):
        # Analysis is complete, return final response
        logger.info("Analysis completed, returning final response")
        
        # Add visualization information to the response if available
        viz_paths = state.get("visualization_paths", [])
        response = output.action.response
        
        if viz_paths:
            viz_info = "\n\n## Visualizations\n\n"
            viz_info += f"{len(viz_paths)} visualizations were created during this analysis. "
            viz_info += "They are displayed in the Visualizations section below."
            
            response += viz_info
        
        return {
            "analysis_summary": response,
            "analysis_status": "completed"
        }
    else:
        # Update the plan
        new_plan = output.action.steps
        logger.info(f"Updated plan with {len(new_plan)} steps")
        
        # Find the first step that hasn't been completed yet
        completed_steps = [step for step, _ in past_steps]
        next_step = None
        next_step_idx = 0
        
        for i, step in enumerate(new_plan):
            if step not in completed_steps:
                next_step = step
                next_step_idx = i
                break
        
        return {
            "analysis_plan": new_plan, 
            "current_step": next_step,
            "step_index": next_step_idx,
            "human_feedback_response": None  # Reset human feedback after incorporating it
        }

async def request_human_input(state: GraphState) -> Dict[str, Any]:
    """Request human input for the current analysis"""
    logger.info("Requesting human input")
    
    objective = state.get("user_feedback", "Analyze the provided data")
    plan = state.get("analysis_plan", [])
    past_steps = state.get("past_steps", [])
    error = state.get("error_message", "")
    
    # Format plan and past steps
    plan_str = "\n".join(f"{i+1}. {step}" for i, step in enumerate(plan))
    past_steps_formatted = "\n".join([f"Step: {step}\nResult: {result}" for step, result in past_steps])
    
    # Generate a question for the human
    input_request = await human_input_requester.ainvoke({
        "objective": objective,
        "plan": plan_str,
        "past_steps": past_steps_formatted,
        "issue": error if error else "Need guidance on how to proceed with the analysis"
    })
    
    return {
        "pending_human_input": True,
        "human_feedback_request": input_request.question,
        "interruption_reason": input_request.context,
        "analysis_status": "human_review"
    }

async def handle_human_input(state: GraphState, human_input: str) -> Dict[str, Any]:
    """Process human input and update the state accordingly"""
    logger.info(f"Received human input: {human_input}")
    
    return {
        "pending_human_input": False,
        "human_feedback_response": human_input,
        "analysis_status": "in_progress"
    }

def should_continue_analysis(state: GraphState) -> str:
    """Determine if we should continue analysis or conclude"""
    # If we have an analysis summary, we're done
    if "analysis_summary" in state and state["analysis_summary"]:
        return "conclude"
    
    # If there's an error, we need human intervention
    if "error_message" in state and state["error_message"]:
        return "request_human_input"
    
    # If there are steps left to execute, continue
    analysis_plan = state.get("analysis_plan", [])
    past_steps = state.get("past_steps", [])
    
    if not analysis_plan:
        return "request_human_input"  # No plan, need human input
    
    completed_steps = [step for step, _ in past_steps]
    
    # Check if we've completed all steps
    all_steps_completed = True
    for step in analysis_plan:
        if step not in completed_steps:
            all_steps_completed = False
            break
    
    if all_steps_completed:
        return "conclude"
    else:
        return "continue_analysis"  # Still have steps to complete

def create_planner_graph() -> StateGraph:
    """Create the data analysis planner workflow graph"""
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("create_plan", plan_step)
    workflow.add_node("execute_step", execute_step)
    workflow.add_node("replan", replan_step)
    workflow.add_node("request_human_input", request_human_input)
    workflow.add_node("conclude", lambda x: x)  # Placeholder for conclusion
    
    # Add edges
    workflow.add_edge(START, "create_plan")
    workflow.add_edge("create_plan", "execute_step")
    workflow.add_edge("execute_step", "replan")
    
    # Conditional edges from replan
    workflow.add_conditional_edges(
        "replan",
        should_continue_analysis,
        {
            "continue_analysis": "execute_step",
            "request_human_input": "request_human_input",
            "conclude": "conclude"
        }
    )
    
    # Edge from human intervention back to replan
    workflow.add_edge("request_human_input", END)
    
    # End from conclude
    workflow.add_edge("conclude", END)
    
    return workflow.compile()

# Create graph with checkpointing
memory_saver = MemorySaver()
data_analysis_app = create_planner_graph().with_config(
    {"checkpointer": memory_saver}
)

# Human-in-the-loop function to continue execution after human input
async def continue_with_human_input(thread_id: str, human_input: str) -> Dict[str, Any]:
    """Continue the analysis after receiving human input"""
    # Get the current state
    checkpoint = memory_saver.get_checkpoint(thread_id)
    
    if checkpoint is None:
        logger.error(f"No checkpoint found for thread {thread_id}")
        return {"error": "No analysis session found"}
    
    # Update the state with human input
    current_state = cast(GraphState, checkpoint.state)
    
    # Create a new state with the human input
    new_state = {**current_state, **await handle_human_input(current_state, human_input)}
    
    # Continue execution from replan node
    config = {"recursion_limit": 50}
    
    # Create a new thread starting from the replan node
    new_thread = await data_analysis_app.acontinue_from_checkpoint(
        checkpoint,
        "replan", 
        new_state, 
        config=config
    )
    
    # Return the final state
    events = [event async for event in new_thread]
    final_state = events[-1] if events else {}
    
    return final_state

# Function to start a new analysis
async def start_analysis(input_data: Dict[str, Any]) -> str:
    """Start a new data analysis planning session"""
    # Create initial state
    initial_state = GraphState(
        raw_data_path=input_data.get("data_path", ""),
        raw_data_description=input_data.get("data_description", ""),
        user_feedback=input_data.get("objective", "Analyze the provided data"),
        analysis_status="not_started",
        visualization_paths=[]
    )
    
    # Generate a thread ID
    thread_id = str(uuid.uuid4())
    
    # Start the analysis
    config = {"recursion_limit": 50}
    thread = data_analysis_app.astream(initial_state, config=config, thread_id=thread_id)
    
    # Start the thread in the background
    asyncio.create_task(_process_thread(thread, thread_id))
    
    return thread_id

async def _process_thread(thread, thread_id: str) -> None:
    """Process a thread in the background"""
    async for event in thread:
        logger.info(f"Thread {thread_id} event: {event.keys()}")
    
    logger.info(f"Thread {thread_id} completed")

def get_analysis_state(thread_id: str) -> Optional[Dict[str, Any]]:
    """Get the current state of an analysis"""
    checkpoint = memory_saver.get_checkpoint(thread_id)
    
    if checkpoint is None:
        return None
    
    return cast(GraphState, checkpoint.state)



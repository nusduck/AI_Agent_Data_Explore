
from typing import Any
from langgraph.prebuilt import create_react_agent

from core.model import LanguageModelManager, ModelType
from core.state import GraphState
from utils.logger import setup_logger
from agents.agent_planner_new import AnalysisPlan
logger = setup_logger("agent_replanner.log")
model_manager = LanguageModelManager()


def replanner_agent(state: GraphState) -> Any:
    logger.info(f"Start replanner agent")
    # model manager
    llm = model_manager.get_model(ModelType.OPENAI_O3)

    prompt = """
    For the given data analysis objective, update your plan based on what has been done so far.

    Your objective was:
    {objective}

    Your original plan was:
    {plan}

    Human feedback (if any): {user_feedback}

    Update your plan accordingly. If no more steps are needed and you can return the final analysis results, respond with that. 
    Otherwise, provide only the steps that still NEED to be done (do not include previously completed steps).
    """
    
    # Safely extract values from state with defaults to prevent KeyError
    try:
        formatted_prompt = prompt.format(
            objective=state.get("target", "Analyze the provided data"),
            plan=state.get("analysis_plan", "No plan provided"),
            user_feedback=state.get("human_feedback_response", "No feedback provided")
        )
        logger.info(f"Created replanner agent successfully")
        
        return create_react_agent(
            model=llm,
            tools=[],
            prompt=formatted_prompt,
            response_format=AnalysisPlan
        )
    except Exception as e:
        logger.error(f"Error creating replanner agent: {str(e)}")
        raise

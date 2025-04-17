from typing import List, Dict, Any, Tuple, Union, cast, Optional, Literal
from pydantic import BaseModel, Field
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, START, END

from core.model import LanguageModelManager, ModelType
from core.state import GraphState
from utils.logger import setup_logger
from tools.web_search import create_web_search_tool

logger = setup_logger("agent_planner.log")
model_manager = LanguageModelManager()

class AnalysisPlan(BaseModel):
    """Plan for data analysis and visualization"""
    steps: Optional[str] = Field(
        description="The data visualization and analysis plan includes detailed steps across four modules: data processing, data description, data exploration, and data visualization."
    )

def planner_agent(state: GraphState) -> Any:
    logger.info(f"Start planner agent")
    # model manager
    llm = model_manager.get_model(ModelType.OPENAI_O4)
    # Define data analysis tools
    tools = [create_web_search_tool()]
    # Create planning prompts
    prompt = """For the given objective, develop a detailed step-by-step plan for data analysis and visualization.
    first, here is some information about the data:
        - the objective is:
        {objective}
        - the data description is:
        {data_description}
        - the data samples are:
        {data_samples}
        - the data path is:
        {data_path}
        - the data information is:
        {data_info}
    second, use the web search tool to find some analysis ideas and add them to the plan.
    third, create a plan for the analysis.
        This plan should include specific tasks such as:
        1. data cleaning and preprocessing
        2. exploratory data analysis
        3. statistical analysis if needed
        4. creating appropriate visualizations
        5. interpreting results
    Make sure each step is clear, specific, and provides all information needed for execution.
    The final step should produce the desired analysis outcome or visualization.
    Do not add unnecessary steps and focus on the specific analysis goals.
    """
    
    # Safely extract values from state with defaults to prevent KeyError
    try:
        formatted_prompt = prompt.format(
            objective=state.get("target", "Analyze the provided data"),
            data_description=state.get("raw_data_description", "No description provided"),
            data_samples=state.get("raw_data_samples", "No samples provided"),
            data_path=state.get("raw_data_path", "No path provided"),
            data_info=state.get("raw_data_info", "No info provided")
        )
        logger.info(f"Created planner agent successfully")
        return create_react_agent(model=llm, tools=tools, prompt=formatted_prompt, response_format=AnalysisPlan)
    except Exception as e:
        logger.error(f"Error creating planner agent: {str(e)}")
        raise


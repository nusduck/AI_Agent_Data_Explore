from langchain_core.messages import SystemMessage, HumanMessage

from core.state import GraphState
from core.model import LanguageModelManager, ModelType
from utils.file_loader import load_analysis_files,load_visualization_files
from utils.logger import setup_logger

model_manager = LanguageModelManager()
llm = model_manager.get_model(ModelType.GOOGLE_FLASH)

def report_node(state: GraphState) -> GraphState:
    """
    Generate a markdown report based on the content create by the execute node.

    Args:
        state (GraphState): The state.

    Returns:
        GraphState: The updated state.
    """
    logger = setup_logger("report_node.log")
    logger.info("Report node...")

    # read the number from state
    number = state["number"]
    logger.info(f"Report number: {number}")
    report_content = load_analysis_files(number)
    image_list = load_visualization_files(number)
    # read the analysis plan from state
    plan = state["analysis_plan"]
    # construct the prompt:
    system_prompt_text = (
        "You are a data scientist and you are writing data analysis reports and do some interpretation. "
    )
    system_message = SystemMessage(content=system_prompt_text)
    human_prompt = []
    human_prompt_base_text = f"""
    "You are an expert data analyst tasked with generating a complete and insightful report based on a pre-defined analysis plan, a data analysis report, and accompanying visualizations. The report must adhere to the structure outlined in the analysis plan and provide thorough interpretations of the findings."

    "You will be provided with the following:"

    "*   **Analysis Plan:**  {plan}
    "*   **Analysis Report {report_content}
    "*   **Visualizations:**  provided in the below

    "Your task is to generate a complete markdown report that adheres strictly to the structure defined in the `Analysis Plan`. For each section of the report, you must:"

    "*   **Synthesize information:**  Combine information from the `Analysis Report and Data` and the `Visualizations` to create a coherent and comprehensive narrative."
    "*   **Provide Interpretation:**  Offer insightful interpretations of the data and results. Explain the meaning of the findings, their significance, and any potential implications."
    "*   **Support with Evidence:**  Cite specific data points, statistical results, and visualizations to support your interpretations."

    "The report must be well-written, clear, and concise. Avoid simply restating the information from the `Analysis Report and Data`. Instead, focus on providing context, explaining the 'why' behind the numbers, and highlighting the key takeaways."

    "**Important Constraints:**"

    "*   **Report Structure:** The report must strictly follow the structure and order outlined in the `Analysis Plan`."
    "*   **No Code Fences:**  Do NOT enclose the entire report within triple backticks (```). "
    "*   **Complete Report:**  You must generate the entire report, including all sections defined in the `Analysis Plan`."
    "*   **Focus on Interpretation:**  The primary focus should be on the interpretation of the data and results.  The report should not simply be a summary of the analysis."

    """ 
    human_prompt.append({"type": "text", "text": human_prompt_base_text})
    # Added images to the prompt
    image_base64 = load_visualization_files(number)

    for image in image_base64:
        human_prompt.append({
                "type": "image_url",
                "image_url": {"url": "data:image/png;base64," + image['base64']}
            })
    human_message = HumanMessage(content=human_prompt)
    result = llm.invoke([system_message, human_message])

    logger.info("Node report successfully.")
    # print(f"report result: {result.content}")
    return {"final_report": result.content}
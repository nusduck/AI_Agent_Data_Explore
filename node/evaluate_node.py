import base64
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

from core.state import GraphState
from core.model import LanguageModelManager, ModelType
from utils.file_loader import load_analysis_files,load_visualization_files
from utils.logger import setup_logger
import streamlit as st

model_manager = LanguageModelManager()

def evaluate_node(state: GraphState) -> GraphState:
    """
    Evaluate a node in the graph state.

    Args:
        state (GraphState): The current state of the graph.

    Returns:
        GraphState: The updated state of the graph.
    """
    logger = setup_logger("evaluate_node.log")
    logger.info("Evaluating node...")
    
    # 从 Streamlit session_state 中获取模型选择，如果有的话
    if 'st' in globals() and hasattr(st, 'session_state') and 'model_selections' in st.session_state:
        model_type_str = st.session_state.model_selections.get('evaluate', 'GOOGLE_FLASH')
        model_type = getattr(ModelType, model_type_str)
        logger.info(f"Using model from streamlit: {model_type.name}")
    else:
        model_type = ModelType.GOOGLE_FLASH
        logger.info(f"Using default model: {model_type.name}")
        
    llm = model_manager.get_model(model_type)

    # read the number from state
    number = state["number"]
    logger.info(f"execution number: {number}")
    data = load_analysis_files(number)
    image_list = load_visualization_files(number)
    # read the analysis plan from state
    plan = state["analysis_plan"]
    report_content = state["final_report"]
    # construct the prompt:
    system_prompt_text = (
        "You are a critical data scientist tasked with evaluating the quality, accuracy, relevance, and insightfulness of a data analysis report based on the original plan and the results produced. "
    )
    system_message = SystemMessage(content=system_prompt_text)
    human_prompt = []
    human_prompt_base_text = f"""

**Inputs You Will Be Provided With:**

1.  **Analysis Plan (`plan`):**
    ```
    {plan}
    ```
    *(The original step-by-step plan that guided the analysis execution. Use this to assess if the report covers the intended scope and structure.)*

2.  **Generated Analysis Report (`report_content`):**
    ```
    {report_content}
    ```
    *(The Markdown report generated by the reporting agent. This is the primary object of evaluation.)*

3.  **Analysis Results & Visualization Info (`analysis_results`):**
    ```
    {data}
    ```
    *(Contains the outputs from the code execution, such as statistical summaries, calculated values, model results, and information about the visualizations generated (e.g., filenames, types like 'histogram of column X'). Use this to verify the accuracy and evidence base of the report.)*

**Your Task:**

Critically evaluate the provided `Analysis Report` based on the `Analysis Plan` and `Analysis Results & Visualization Info`. Your output must *only* be the evaluation itself, formatted exactly as specified below.

**Evaluation Criteria (Base your assessment on these points):**

*   **Adherence to Plan:** Does the report structure and content directly follow the `Analysis Plan`? Are all planned steps/objectives addressed?
*   **Accuracy:** Are the findings, data points, and summaries presented in the report consistent with the `Analysis Results & Visualization Info`?
*   **Clarity & Structure:** Is the report well-organized, clearly written, and easy to understand? Is the Markdown formatting appropriate?
*   **Quality of Interpretation:** Does the report provide meaningful insights and explain the *significance* of the findings, or does it merely summarize? Is the interpretation logical and well-supported?
*   **Visualization Referencing & Relevance:** Are the visualizations (as described in `analysis_results` and referenced in the report) relevant to the analysis step? Are they clearly referenced in the report text?
*   **Evidence-Based:** Does the report effectively use specific data points, statistical results, or references to visualizations from the `Analysis Results & Visualization Info` to support its claims and interpretations?
*   **Completeness:** Are there any significant gaps or omissions in the report compared to what the `Analysis Plan` specified?

**Required Output Format:**

**Strictly follow this format:**

### **Overall Rating:** 
    (Provide a single qualitative rating on the first line, e.g., Excellent, Good, Fair, Poor)
### **Evaluation Logic:**
    *   (Provide detailed justification for the rating below the "Overall Rating" line.)
    *   (Structure your points logically, ideally referencing the specific evaluation criteria above.)
    *   (Include specific examples from the `report_content` or `analysis_results` to illustrate strengths and weaknesses.)
    *   (Example structure for logic section:
        *   **Adherence to Plan:** [Your assessment with evidence]
        *   **Accuracy:** [Your assessment with evidence]
        *   **Clarity & Structure:** [Your assessment with evidence]
        *   **Interpretation:** [Your assessment with evidence]
        *   **Visualization Referencing:** [Your assessment with evidence]
        *   **Evidence-Based:** [Your assessment with evidence]
        *   **Completeness:** [Your assessment with evidence]
        *   **Overall Summary:** [Optional brief summary of key feedback points])
### Strenghtens and Weaknesses:
    *   (Provide a detail statement of the report's strengths and weaknesses, if applicable.)
### **Suggestions for Improvement:**
    *   (Provide specific suggestions for improving the report, if applicable.)

**Important Constraints:**

*   **Output Content:** Do not include any greetings, introductory sentences, explanations of your role, or any text outside this specific structure.
*   **Focus:** Base your evaluation strictly on comparing the `report_content` against the `plan` and `analysis_results`.
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

    logger.info("Node evaluated successfully.")
    # print(f"Evaluation result: {result.content}")
    return {"evaluation_results": result.content}
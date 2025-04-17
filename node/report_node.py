from langchain_core.messages import SystemMessage, HumanMessage

from core.state import GraphState
from core.model import LanguageModelManager, ModelType
from utils.file_loader import load_analysis_files,load_visualization_files
from utils.logger import setup_logger
import streamlit as st

model_manager = LanguageModelManager()

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
    
    # 从 Streamlit session_state 中获取模型选择，如果有的话
    if 'st' in globals() and hasattr(st, 'session_state') and 'model_selections' in st.session_state:
        model_type_str = st.session_state.model_selections.get('report', 'GOOGLE_FLASH')
        model_type = getattr(ModelType, model_type_str)
        logger.info(f"Using model from streamlit: {model_type.name}")
    else:
        model_type = ModelType.GOOGLE_FLASH
        logger.info(f"Using default model: {model_type.name}")
        
    llm = model_manager.get_model(model_type)

    # read the number from state
    number = state["number"]
    logger.info(f"Report number: {number}")
    report_content = load_analysis_files(number)
    image_list = load_visualization_files(number)
    # read the analysis plan from state
    plan = state["analysis_plan"]
    # construct the prompt:
    system_prompt_text = (
        "You are an expert data analyst. Your task is to synthesize information from a completed analysis execution (including results) guided by an initial analysis plan, and generate a comprehensive, insightful final report in Markdown format. You will reference visualizations provided externally."
    )
    system_message = SystemMessage(content=system_prompt_text)
    human_prompt = []
    human_prompt_base_text = f"""

**Agent Role:** You are an expert data analyst. Your task is to synthesize the results from a completed data analysis execution and generate a structured, insightful final report in Markdown format. You will focus on summarizing the methodology, interpreting the key findings, discussing implications, and concluding based on the provided execution results, using the original plan for context and objectives.

**Inputs You Will Be Provided With:**

1.  **Analysis Plan (`plan`):**
    ```
    {plan}
    ```
    *(Provides the overall objective and context for the analysis that was performed.)*

2.  **Execution Results (`execution_results`):**
    ```
    {report_content}
    ```
    *(Contains the factual outputs from the code execution: statistical summaries, calculated values, model results, descriptions/confirmation of generated visualizations, etc. This is the primary source for your report's content.)*

3.  **Visualization Information (`visualization_info`):**
    *   Information describing the visualizations generated, typically including filenames or identifiers. Example:
        ```
        Visualizations generated:
        - feature_X_histogram.png (Histogram of feature X)
        - Y_vs_Z_scatterplot.png (Scatter plot of Y vs Z)
        - key_metrics_summary_table.png (Table showing key metrics)
        ```
    *(Provides identifiers for referencing the visualizations discussed in the report. Assume these visuals are available externally.)*



**Your Task:**

Generate the **content** of a final analysis report in **Markdown format** using the structure defined below. The report must summarize the analysis approach and provide interpretation, discussion, and conclusions based *primarily* on the provided `execution_results`.

**Required Report Structure and Content Instructions:**

Generate the report using the following Markdown structure precisely. Populate each section based on the inputs:


## xxx Data Analysis Report

### Methodology

*   Briefly summarize the key steps taken during the analysis.
*   Refer to the `Analysis Plan` for the intended steps and `execution_results` for confirmation of what was actually done (e.g., specific data cleaning techniques used, statistical tests performed, models built).
*   Keep this section concise and focused on the *how* of the analysis.

### Interpretation

*   This is the main section detailing the findings.
*   Synthesize the key results and insights presented in the `execution_results`. Do not just list outputs; explain what they *mean*.
*   For each significant finding:
    *   State the finding clearly.
    *   Support it with specific data points or statistical values from `execution_results`.
    *   Reference the relevant visualization(s) by their identifiers from `visualization_info` (e.g., "The trend is visible in `sales_trend_lineplot.png`."). **Do not embed images.**
    *   Explain the interpretation: What insight does this finding provide regarding the analysis objective (from the `Analysis Plan`)?

### Discussion

*   Provide broader context for the findings presented in the Interpretation section.
*   Discuss any potential limitations of the analysis (e.g., data limitations, assumptions made based on the methodology).
*   Suggest possible implications of the findings.
*   If appropriate, propose potential next steps or areas for further investigation based on the results.

### Conclusion

*   Summarize the most critical insights and main takeaways from the analysis.
*   Directly address the original analysis objective stated in the `Analysis Plan`. What is the answer or key message derived from the interpretation of the results?
*   Keep this section brief and focused on the high-level summary.
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
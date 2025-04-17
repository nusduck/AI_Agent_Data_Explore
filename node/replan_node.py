from agents.agent_replanner import replanner_agent 
from core.state import GraphState
from utils.data_loader import DataLoader
from core.model import ModelType
import streamlit as st

def replan_node(state: GraphState) -> GraphState:
    """Replan node"""
    # 如果 Streamlit session_state 中有模型选择，则使用它
    if 'st' in globals() and hasattr(st, 'session_state') and 'model_selections' in st.session_state:
        model_type = st.session_state.model_selections.get('replan', 'OPENAI_O3')
        model_type = getattr(ModelType, model_type)
    else:
        model_type = ModelType.OPENAI_O3
    
    replan = replanner_agent(state, model_type)
    result = replan.invoke(state)
    return {"analysis_plan": result["structured_response"].steps}
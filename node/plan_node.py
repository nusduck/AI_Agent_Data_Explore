from agents.agent_planner_new import planner_agent
from core.state import GraphState
from core.model import ModelType, LanguageModelManager
from utils.data_loader import DataLoader
import streamlit as st

def plan_node(state: GraphState) -> GraphState:
    """Plan node"""
    # 如果 Streamlit session_state 中有模型选择，则使用它
    if 'st' in globals() and hasattr(st, 'session_state') and 'model_selections' in st.session_state:
        model_type = st.session_state.model_selections.get('plan', 'OPENAI_O4')
        model_type = getattr(ModelType, model_type)
    else:
        model_type = ModelType.OPENAI_O4
    
    plan = planner_agent(state, model_type)
    result = plan.invoke(state)
    return {"analysis_plan": result["structured_response"].steps}
from agents.agent_replanner import replanner_agent 
from core.state import GraphState
from utils.data_loader import DataLoader

def replan_node(state: GraphState) -> GraphState:
    """Replan node"""
    replan = replanner_agent(state)
    result = replan.invoke(state)
    return {"analysis_plan": result["structured_response"].steps}
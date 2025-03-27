from agents.agent_planner_new import planner_agent
from core.state import GraphState
from utils.data_loader import DataLoader

def plan_node(state: GraphState) -> GraphState:
    """Plan node"""
    plan = planner_agent(state)
    result = plan.invoke(state)
    return {"analysis_plan": result["structured_response"].steps}
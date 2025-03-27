from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from typing import Dict, Any
from langchain_core.messages import HumanMessage

from node.human_plan_feedback import human_plan_feedback_node
from node.plan_node import plan_node
from node.replan_node import replan_node
from core.state import GraphState

memory = MemorySaver()
def replan_executor_condition(state: GraphState):
    if state["pending_human_input"]:
        return "replan"
    else:
        return END

def workflow() -> StateGraph:
    graph = StateGraph(GraphState)
    graph.add_node("plan", plan_node)
    graph.add_node("human_plan_feedback", human_plan_feedback_node)
    graph.add_node("replan", replan_node)

    graph.set_entry_point("plan")
    graph.add_edge(START, "plan")
    graph.add_edge("plan", "human_plan_feedback")
    # conditional edge
    # graph.add_conditional_edges(
    #     "human_plan_feedback",
    #     replan_executor_condition
    # )
    graph.add_edge("replan", END)
    return graph.compile(checkpointer=memory)


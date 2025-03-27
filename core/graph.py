from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from typing import Dict, Any
from langchain_core.messages import HumanMessage

from node.human_plan_feedback import human_plan_feedback_node
from node.plan_node import plan_node
from core.state import GraphState

memory = MemorySaver()

def workflow() -> StateGraph:
    graph = StateGraph(GraphState)
    graph.add_node("plan", plan_node)
    graph.add_node("human_plan_feedback", human_plan_feedback_node)

    graph.set_entry_point("plan")
    graph.add_edge(START, "plan")
    graph.add_edge("plan", "human_plan_feedback")
    graph.add_edge("human_plan_feedback", END)
    return graph.compile(checkpointer=memory)


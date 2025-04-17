from langgraph.graph import StateGraph, END, START
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
# from langgraph.checkpoint.memory import MemorySaver
from typing import Dict, Any
from langchain_core.messages import HumanMessage

from node.human_plan_feedback import human_plan_feedback_node
from node.plan_node import plan_node
from node.replan_node import replan_node
from node.execute_node import execute_node
from node.evaluate_node import evaluate_node
from node.report_node import report_node
from core.state import GraphState

conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)   
memory = SqliteSaver(conn)
# memory = MemorySaver()
def replan_executor_condition(state: GraphState):
    if state["pending_human_input"]:
        return "replan"
    else:
        return "execute"


def workflow() -> StateGraph:
    graph = StateGraph(GraphState)
    graph.add_node("plan", plan_node)
    graph.add_node("human_plan_feedback", human_plan_feedback_node)
    graph.add_node("replan", replan_node)
    graph.add_node("execute", execute_node)
    graph.add_node("report", report_node)
    graph.add_node("evaluate", evaluate_node)

    graph.set_entry_point("plan")
    graph.add_edge(START, "plan")
    graph.add_edge("plan", "human_plan_feedback")
    # conditional edge
    # graph.add_conditional_edges(
    #     "human_plan_feedback",
    #     replan_executor_condition
    # )
    graph.add_edge("replan", "execute")
    graph.add_edge("execute", "report")
    graph.add_edge("report", "evaluate")
    graph.add_edge("evaluate", END)
    return graph.compile(checkpointer=memory)


from core.state import GraphState
from node.plan_node import plan_node
from langgraph.types import interrupt, Command
from langgraph.graph import END
from typing import Any

def human_plan_feedback_node(state: GraphState) -> Any:
    humanReview = interrupt(
        {
            "analysis_plan": state["analysis_plan"]
        }
    )

    action, review = humanReview 

    if action == "go":
        return Command(goto= END)
    elif action == "edit":
        return {"human_feedback_response": review}
    else:
        return Command(goto= plan_node)
    
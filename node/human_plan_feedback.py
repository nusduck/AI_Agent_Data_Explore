from core.state import GraphState
from typing_extensions import TypedDict, Literal
from langgraph.types import interrupt, Command
from langgraph.graph import END
from typing import Any

def human_plan_feedback_node(state: GraphState) -> Command[Literal["plan","replan","execute"]]:
    # this is the value we'll be providing via Command(resume=<human_review>)
    human_review = interrupt(
        {
            "analysis_plan": state["analysis_plan"]
        }
    )

    # Get action and review data from the human_review dictionary
    action = human_review.get("action")
    review = human_review.get("review")

    if action == "go":
        return Command(goto="execute")
    elif action == "edit":
        return Command(goto="replan", update={"human_feedback_response": review, "pending_human_input": True})
    else:
        return Command(goto="plan")
    
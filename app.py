from langgraph.types import Command
from core.graph import workflow
from core.state import GraphState
from utils.data_loader import DataLoader


data_loader = DataLoader()
df = data_loader.load_data("data/sample_data.csv")[0]

state = GraphState(
    target="Show me technical indicators for the stock market",
    raw_data_path="data/sample_data.csv",
    raw_data_description=data_loader.generate_data_description(df),
    raw_data_samples=data_loader.get_data_samples(df).to_dict(),
    raw_data_info=data_loader.get_data_info(df),
    pending_human_input=False
)
thread_config = {"configurable": {"thread_id": "11"}}

result = workflow().invoke(state, config=thread_config)
print("-"*100)
print("Here is the plan:")
print(result["analysis_plan"])
print("-"*100)

workflow().stream(Command(resume={"action": "edit","review":"please simplyfy the plan"}), config=thread_config, stream_mode=["values", "messages"])
print(state)
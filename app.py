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
    #raw_data_samples=data_loader.get_data_samples(df).to_dict(),
    raw_data_info=data_loader.get_data_info(df)
)
thread_config = {"configurable": {"thread_id": "2"}}

result = workflow().invoke(state, config=thread_config)
for i in result["analysis_plan"]:
    print("Here is the plan:")
    print(i)
    print("-"*100)

workflow().invoke(Command(resume={"action": "edit","review":"YES OK"}), config=thread_config)
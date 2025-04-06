from langgraph.types import Command
from core.graph import workflow
from core.state import GraphState
from utils.data_loader import DataLoader
import uuid
number = uuid.uuid4()
print(number)
data_loader = DataLoader()
df = data_loader.load_data("data/temp_upload.csv")[0]

state = GraphState(
    target="help me predict the price",
    number=number,
    raw_data_path="data/temp_upload.csv",
    raw_data_description=data_loader.generate_data_description(df),
    raw_data_samples=data_loader.get_data_samples(df).to_dict(),
    # raw_data_info=data_loader.get_data_info(df),
    pending_human_input=False
)
# generate thread_id randomly
thread_config = {"configurable": {"thread_id": str(number)}}

result = workflow().invoke(state, config=thread_config)
print("-"*100)
print("Here is the plan:")
print(result["analysis_plan"])
print("-"*100)

workflow().invoke(Command(resume={"action": "go","review":"please simplyfy the plan"}), config=thread_config)
print(state)
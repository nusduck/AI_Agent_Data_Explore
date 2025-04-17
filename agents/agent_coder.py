from langgraph_codeact import create_codeact
from e2b_code_interpreter import Sandbox
from core.model import LanguageModelManager, ModelType


from core.state import GraphState
from utils.logger import setup_logger
from tools.code_executor import eval, e2b_code_executor
from utils.file_operate_e2b import upload_file_to_sandbox

logger = setup_logger("agent_coder.log")
model_manager = LanguageModelManager()

def agent_coder(state: GraphState, model_type: ModelType = ModelType.OPENAI_O4):
    logger.info(f"Start agent coder with model: {model_type.name}")
    
    llm = model_manager.get_model(model_type)
    codeact = create_codeact(model=llm,tools=[],eval_fn=eval)
    return codeact.compile()

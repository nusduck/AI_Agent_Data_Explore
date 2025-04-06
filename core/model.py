from enum import Enum
from typing import Dict, Optional
from dotenv import load_dotenv
import os
load_dotenv()  

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.logger import setup_logger

class ModelType(Enum):
    """Enum for different model types"""
    OPENAI_MINI = "gpt-4o-mini"
    OPENAI_O3 = "o3-mini-2025-01-31"
    GOOGLE_FLASH = "gemini-2.0-flash"
    OPENAI_4O = "gpt-4o"
    DEEPSEEK = "deepseek-ai/DeepSeek-V3-0324"

class ModelConfig:
    """Configuration for different models"""
    DEFAULT_CONFIGS = {
        ModelType.OPENAI_MINI: {
            "temperature": 0.6,
            "provider": "openai"
        },
        ModelType.OPENAI_O3: {
            "provider": "openai",
            "reasoning_effort": "high"
        },
        ModelType.GOOGLE_FLASH: {
            "temperature": 0,
            "provider": "google"
        },
        ModelType.OPENAI_4O: {
            "temperature": 0.5,
            "provider": "openai"
        },
        ModelType.DEEPSEEK: {
            "temperature": 0.6,
            "provider": "openai",
            "base_url": "https://llm.chutes.ai/v1",
            "api_key": os.getenv("DEEPSEEK_API_KEY")
        }
    }

class LanguageModelManager:
    def __init__(self):
        """Initialize the language model manager"""
        self.logger = setup_logger("model.log")
        self.models: Dict[ModelType, Optional[ChatOpenAI | ChatGoogleGenerativeAI]] = {
            model_type: None for model_type in ModelType
        }
        self.initialize_models()

    def initialize_models(self):
        """Initialize all language models"""
        try:
            for model_type in ModelType:
                config = ModelConfig.DEFAULT_CONFIGS[model_type]
                if config["provider"] == "openai":
                    self.models[model_type] = ChatOpenAI(
                        model=model_type.value,
                        **{k: v for k, v in config.items() if k != "provider"}
                    )
                elif config["provider"] == "google":
                    self.models[model_type] = ChatGoogleGenerativeAI(
                        model=model_type.value,
                        **{k: v for k, v in config.items() if k != "provider"}
                    )
            self.logger.info("Language models initialized successfully.")
        except Exception as e:
            self.logger.error(f"Error initializing language models: {str(e)}")
            raise

    def get_model(self, model_type: ModelType) -> Optional[ChatOpenAI | ChatGoogleGenerativeAI]:
        """Get a specific model by type"""
        if model_type not in self.models:
            raise ValueError(f"Model type {model_type} not found")
        return self.models[model_type]

    def get_all_models(self) -> Dict[ModelType, Optional[ChatOpenAI | ChatGoogleGenerativeAI]]:
        """Return all initialized language models"""
        return self.models
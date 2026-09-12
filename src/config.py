"""Configuration and LLM Provider Factory.

Supports:
1. Local LLM via Ollama (http://localhost:11434)
2. OpenAI Cloud API (via OPENAI_API_KEY)
3. Offline Mock Engine for testing and validation
"""

import os
from typing import Literal, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env file if available
load_dotenv()

ProviderType = Literal["ollama", "openai", "mock"]


@dataclass
class AgentConfig:
    provider: Optional[ProviderType] = None
    openai_api_key: Optional[str] = None
    openai_model: Optional[str] = None
    ollama_base_url: Optional[str] = None
    ollama_model: Optional[str] = None
    max_retries: Optional[int] = None
    execution_timeout_seconds: Optional[int] = None

    def __post_init__(self):
        if not self.provider:
            self.provider = os.getenv("LLM_PROVIDER", "ollama").lower()  # type: ignore
        if self.openai_api_key is None:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_model:
            self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        if not self.ollama_base_url:
            self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        if not self.ollama_model:
            self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
        if self.max_retries is None:
            self.max_retries = int(os.getenv("MAX_RETRY_COUNT", "3"))
        if self.execution_timeout_seconds is None:
            self.execution_timeout_seconds = int(os.getenv("EXECUTION_TIMEOUT_SECONDS", "45"))


def get_llm(
    provider: Optional[ProviderType] = None,
    model: Optional[str] = None,
    temperature: float = 0.0,
    config: Optional[AgentConfig] = None
):
    """Factory creating the configured BaseChatModel instance.
    
    Args:
        provider: 'ollama', 'openai', or 'mock'. Defaults to config.provider.
        model: Model identifier (e.g. 'llama3.2' or 'gpt-4o-mini').
        temperature: Sampling temperature (default 0.0 for deterministic code/plans).
        config: Optional pre-loaded AgentConfig instance.
        
    Returns:
        Configured BaseChatModel instance.
    """
    cfg = config or AgentConfig()
    selected_provider = (provider or os.getenv("LLM_PROVIDER") or cfg.provider).lower()
    
    if selected_provider == "mock":
        from src.mock_llm import MockAnalyticsChatModel
        return MockAnalyticsChatModel()
        
    elif selected_provider == "openai":
        from langchain_openai import ChatOpenAI
        api_key = cfg.openai_api_key
        if not api_key:
            raise ValueError(
                "OpenAI API key is missing! Please set OPENAI_API_KEY in your .env file "
                "or pass it via the environment."
            )
        selected_model = model or cfg.openai_model
        return ChatOpenAI(
            model=selected_model,
            api_key=api_key,
            temperature=temperature
        )
        
    elif selected_provider == "ollama":
        from langchain_ollama import ChatOllama
        selected_model = model or cfg.ollama_model
        return ChatOllama(
            model=selected_model,
            base_url=cfg.ollama_base_url,
            temperature=temperature
        )
    else:
        raise ValueError(
            f"Unsupported LLM provider: '{selected_provider}'. "
            "Supported options are 'ollama', 'openai', or 'mock'."
        )

from __future__ import annotations

from typing import Any

from mia_agents._env import load_env_files
from mia_agents.llm_client import BedrockProvider, LLMClient, OllamaProvider


PROVIDERS = {
    "ollama": OllamaProvider,
    "bedrock": BedrockProvider,
}


LLM_CONFIGS: dict[str, dict[str, Any]] = {
    "llama3.1": {
        "provider": "ollama",
        "model": "llama3.1",
        "num_ctx": 32768,
    },
    "qwen2.5:7b": {
        "provider": "ollama",
        "model": "qwen2.5:7b",
        "num_ctx": 32768,
    },
    "nova-lite": {
        "provider": "bedrock",
        "model": "amazon.nova-lite-v1:0",
        "region": "us-west-2",
    }
}


def build_llm_client(config_name: str) -> LLMClient:
    load_env_files()

    config = dict(LLM_CONFIGS[config_name])
    provider_name = config.pop("provider")

    if provider_name not in PROVIDERS:
        raise ValueError(
            f"Unknown Provider: {provider_name!r}. "
            f"Options: {sorted(PROVIDERS)}."
        )

    return LLMClient(
        PROVIDERS[provider_name](**config)
    )

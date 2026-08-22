from __future__ import annotations

import os
from typing import Any

from mia_agents._env import load_env_files
from mia_agents.llm_client import BedrockProvider, LLMClient, OllamaProvider
from mia_agents.protocols import ToolSpecInput
from mia_agents.types import LLMResponse


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


class _ConfiguredLLMClient(LLMClient):
    """LLMClient que fija los parámetros efectivos de inferencia."""

    def __init__(
        self,
        provider,
        temperature: float,
    ) -> None:
        super().__init__(provider)
        self._temperature = temperature

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[ToolSpecInput] | None = None,
        system: str | None = None,
        temperature: float = 0.2,
        response_format: dict[str, Any] | None = None,
    ) -> LLMResponse:
        return super().chat(
            messages=messages,
            tools=tools,
            system=system,
            temperature=self._temperature,
            response_format=response_format,
        )


def build_llm_client(config: dict[str, Any]) -> LLMClient:
    load_env_files()

    config = dict(config)
    provider_name = config.pop("provider")

    if provider_name == "bedrock" and "region" not in config:
        config["region"] = os.environ.get("AWS_REGION", "us-west-2")
    temperature = config.pop("temperature", 0.2)

    if provider_name not in PROVIDERS:
        raise ValueError(
            f"Unknown Provider: {provider_name!r}. "
            f"Options: {sorted(PROVIDERS)}."
        )

    return _ConfiguredLLMClient(
        PROVIDERS[provider_name](**config),
        temperature=temperature,
    )

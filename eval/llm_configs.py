"""Configuraciones de LLM para la evaluación de M3."""

from __future__ import annotations

from typing import Any

from mia_agents.llm_client import LLMClient, OllamaProvider


LLM_CONFIGS: dict[str, dict[str, Any]] = {
    "llama3.1": {
        "model": "llama3.1",
        "num_ctx": 32768,
    },
    "qwen2.5:7b": {
        "model": "qwen2.5:7b",
        "num_ctx": 32768,
    },
}


def build_llm_client(config_name: str) -> LLMClient:
    """Construye el cliente LLM indicado por su configuración."""

    config = dict(LLM_CONFIGS[config_name])

    return LLMClient(
        OllamaProvider(**config)
    )
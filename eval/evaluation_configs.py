"""Configuraciones de evaluaciones para M3."""

from __future__ import annotations

from typing import Any


M3_EVALUATION: dict[str, Any] = {
    "systems": [
        {
            "agent_config": "minimal",
            "llm_config": "llama3.1",
        },
        {
            "agent_config": "minimal",
            "llm_config": "qwen2.5:7b",
        },
    ],
    "scenarios": [
        "study-with-key",
        "color-locks",
        "apartment-keys",
        "library-search",
        "office-sequence",
        "extreme-archive",
        "vault-combination",
        "backtracking-vault",
    ],
    "runs_per_case": 5,
    "metrics": [
        "success_rate",
    ],
}
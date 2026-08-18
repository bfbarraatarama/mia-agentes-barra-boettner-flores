"""Configuraciones de corridas para M3."""

from __future__ import annotations

from typing import Any


M3_RUN_CONFIG: dict[str, Any] = {
    "systems": [
        {
            "agent_config": "minimal",
            "llm_config": "llama3.1",
        },
        {
            "agent_config": "minimal",
            "llm_config": "qwen2.5:7b",
        },
        {
            "agent_config": "minimal",
            "llm_config": "nova-lite",
        },
    ],
    "trial_configs": [
        "single_attempt",
    ],
    "scenarios": [
        "study-with-key"
    #    "color-locks",
    #    "apartment-keys",
    #    "library-search",
    #    "office-sequence",
    #    "extreme-archive",
    #    "vault-combination",
    #    "backtracking-vault",
    ],
    "trials_per_case": 5,
}


M3_BASELINE_RUN_CONFIG: dict[str, Any] = {
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
    "trial_configs": [
        "single_attempt",
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
    "trials_per_case": 5,
}


M3_TOOL_REPAIR_COMPARISON_RUN_CONFIG: dict[str, Any] = {
    "systems": [
        {
            "agent_config": "minimal",
            "llm_config": "llama3.1",
        },
        {
            "agent_config": "minimal_tool_repair",
            "llm_config": "llama3.1",
        },
        {
            "agent_config": "minimal",
            "llm_config": "qwen2.5:7b",
        },
        {
            "agent_config": "minimal_tool_repair",
            "llm_config": "qwen2.5:7b",
        },
    ],
    "trial_configs": [
        "single_attempt",
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
    "trials_per_case": 5,
}
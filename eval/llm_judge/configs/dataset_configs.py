"""Configuraciones de datasets para evaluación cualitativa."""

from __future__ import annotations

from typing import Any

from eval.llm_judge.sampling import (
    RANDOM_STRATIFIED_BY_SCENARIO_METHOD,
)


M3_QUALITATIVE_PILOT_DATASET_CONFIG: dict[str, Any] = {
    "dataset_id": "qualitative-pilot-v1",
    "run_ids": [
        "m3-nova-multi-attempt-run-004",
    ],
    "population": {
        "agent_configs": None,
        "llm_configs": [
            "nova-lite",
        ],
        "trial_configs": [
            "multi_attempt",
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
    },
    "sampling": {
        "method": RANDOM_STRATIFIED_BY_SCENARIO_METHOD,
        "seed": 20260821,
        "cases_per_scenario": 3,
        "dev_per_scenario": 2,
    },
}


M3_LLM_JUDGE_SMOKE_DATASET_CONFIG: dict[str, Any] = {
    "dataset_id": "qualitative-llm-judge-smoke-v1",
    "run_ids": [
        "m3-llm-judge-smoke-summary-run-001",
    ],
    "population": {
        "agent_configs": [
            "minimal_summary",
        ],
        "llm_configs": [
            "nova-lite",
        ],
        "trial_configs": [
            "multi_attempt",
        ],
        "scenarios": [
            "office-sequence",
        ],
    },
    "sampling": {
        "method": RANDOM_STRATIFIED_BY_SCENARIO_METHOD,
        "seed": 20260823,
        "cases_per_scenario": 2,
        "dev_per_scenario": 1,
    },
}


DATASET_CONFIG = M3_LLM_JUDGE_SMOKE_DATASET_CONFIG
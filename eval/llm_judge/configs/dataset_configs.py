"""Configuraciones de datasets para evaluación cualitativa."""

from __future__ import annotations

from typing import Any

from eval.llm_judge.sampling import (
    RANDOM_STRATIFIED_BY_SCENARIO_METHOD,
)


M3_QUALITATIVE_PILOT_DATASET_CONFIG: dict[str, Any] = {
    "dataset_id": "qualitative-pilot-v1",
    "run_ids": [
        "m3-nova-tool-repair-comparison-run-003",
    ],
    "population": {
        "agent_configs": None,
        "llm_configs": [
            "nova-lite",
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
    },
    "sampling": {
        "method": RANDOM_STRATIFIED_BY_SCENARIO_METHOD,
        "seed": 20260821,
        "cases_per_scenario": 3,
        "dev_per_scenario": 2,
    },
}


DATASET_CONFIG = M3_QUALITATIVE_PILOT_DATASET_CONFIG
"""Configuraciones de datasets para evaluación cualitativa."""

from __future__ import annotations

from typing import Any

from eval.llm_judge.sampling import (
    BALANCED_HOLDOUT_THEN_DIAGNOSTIC_DEV_METHOD,
    RANDOM_STRATIFIED_BY_SCENARIO_METHOD,
    RANDOM_STRATIFIED_BY_SYSTEM_SCENARIO_METHOD,
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


M3_QUALITATIVE_FINAL_DATASET_CONFIG: dict[str, Any] = {
    "dataset_id": "m3-qualitative-final-v2",
    "run_ids": [
        "m3-final-run-001",
    ],
    "population": {
        "agent_configs": [
            "baseline",
            "planner",
            "summary",
            "planner_summary",
        ],
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
        "method": BALANCED_HOLDOUT_THEN_DIAGNOSTIC_DEV_METHOD,
        "seed": 20260824,
        "holdout_shortest_per_cell": 5,
        "holdout_cases_per_system": 2,
        "holdout_successes": 4,
        "dev_successes": 2,
        "dev_require_plan_for_agent_configs": [
            "planner",
            "planner_summary",
        ],
        "dev_require_summary_for_agent_configs": [
            "summary",
            "planner_summary",
        ],
        "dev_require_multi_attempt": True,
    },
}


M3_FINAL_SELECTION_QUALITATIVE_DATASET_CONFIG: dict[str, Any] = {
    "dataset_id": "m3-final-selection-qualitative-v1",
    "run_ids": [
        "m3-final-run-008",
    ],
    "population": {
        "agent_configs": [
            "planner",
            "baseline_incremental",
            "planner_incremental",
        ],
        "llm_configs": [
            "nova-lite",
        ],
        "trial_configs": [
            "multi_attempt_recovery",
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
        "method": RANDOM_STRATIFIED_BY_SYSTEM_SCENARIO_METHOD,
        "seed": 20260826,
        "cases_per_system_scenario": 3,
    },
}


DATASET_CONFIG = M3_QUALITATIVE_FINAL_DATASET_CONFIG
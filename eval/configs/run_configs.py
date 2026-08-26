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
    "trials_per_case": 10,
}


M3_NOVA_TOOL_REPAIR_COMPARISON_RUN_CONFIG: dict[str, Any] = {
    "systems": [
        {
            "agent_config": "minimal",
            "llm_config": "nova-lite",
        },
        {
            "agent_config": "minimal_tool_repair",
            "llm_config": "nova-lite",
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
    "trials_per_case": 10,
}


M3_NOVA_MULTI_ATTEMPT_RUN_CONFIG: dict[str, Any] = {
    **M3_NOVA_TOOL_REPAIR_COMPARISON_RUN_CONFIG,
    "trial_configs": [
        "multi_attempt",
    ],
}


M3_PLANNER_RUN_CONFIG: dict[str, Any] = {
    "systems": [
        {
            "agent_config": "planner",
            "llm_config": "nova-lite",
        },
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
    "trials_per_case": 10,
}


# Experimento de gestión de contexto (issue #26). El baseline "minimal"
# no se repite: ya está persistido en m3-nova-multi-attempt-run-004 con
# la misma configuración de trial, y la evaluación puede combinar ambos
# runs vía run_ids.
M3_CONTEXT_COMPARISON_RUN_CONFIG: dict[str, Any] = {
    "systems": [
        {
            "agent_config": "minimal_history_200",
            "llm_config": "nova-lite",
        },
        {
            "agent_config": "minimal_compaction",
            "llm_config": "nova-lite",
        },
        {
            "agent_config": "minimal_summary",
            "llm_config": "nova-lite",
        },
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
    "trials_per_case": 10,
}


# Piloto funcional mínimo de la evaluación cualitativa v2.
# Cada corrida apunta a producir evidencia real de uno de los artefactos
# internos que ahora forman parte de la presentación cualitativa.
M3_QUALITATIVE_PILOT_V2_PLANNER_RUN_CONFIG: dict[str, Any] = {
    "systems": [
        {
            "agent_config": "planner",
            "llm_config": "nova-lite",
        },
    ],
    "trial_configs": [
        "multi_attempt",
    ],
    "scenarios": [
        "study-with-key",
    ],
    "trials_per_case": 3,
}


M3_QUALITATIVE_PILOT_V2_COMPACTION_RUN_CONFIG: dict[str, Any] = {
    "systems": [
        {
            "agent_config": "qualitative_pilot_compaction",
            "llm_config": "nova-lite",
        },
    ],
    "trial_configs": [
        "multi_attempt",
    ],
    "scenarios": [
        "vault-combination",
    ],
    "trials_per_case": 3,
}


M3_QUALITATIVE_PILOT_V2_SUMMARY_RUN_CONFIG: dict[str, Any] = {
    "systems": [
        {
            "agent_config": "minimal_summary",
            "llm_config": "nova-lite",
        },
    ],
    "trial_configs": [
        "multi_attempt",
    ],
    "scenarios": [
        "office-sequence",
    ],
    "trials_per_case": 3,
}


M3_LLM_JUDGE_SMOKE_SUMMARY_RUN_CONFIG: dict[str, Any] = {
    "systems": [
        {
            "agent_config": "minimal_summary",
            "llm_config": "nova-lite",
        },
    ],
    "trial_configs": [
        "multi_attempt",
    ],
    "scenarios": [
        "office-sequence",
    ],
    "trials_per_case": 2,
}


M3_FINAL_RUN_CONFIG: dict[str, Any] = {
    "systems": [
        {
            "agent_config": "baseline",
            "llm_config": "nova-lite",
        },
        {
            "agent_config": "planner",
            "llm_config": "nova-lite",
        },
        {
            "agent_config": "summary",
            "llm_config": "nova-lite",
        },
        {
            "agent_config": "planner_summary",
            "llm_config": "nova-lite",
        },
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
    "trials_per_case": 10,
}


M3_FINAL_RECOVERY_RUN_CONFIG: dict[str, Any] = {
    **M3_FINAL_RUN_CONFIG,
    "trial_configs": [
        "multi_attempt_recovery",
    ],
}


M3_FINAL_RECOVERY_TOKEN_TRIGGER_RUN_CONFIG: dict[str, Any] = {
    **M3_FINAL_RECOVERY_RUN_CONFIG,
    "systems": [
        {
            "agent_config": "summary_token_trigger",
            "llm_config": "nova-lite",
        },
        {
            "agent_config": "planner_summary_token_trigger",
            "llm_config": "nova-lite",
        },
    ],
}


M3_FINAL_RECOVERY_STRATEGIC_SUMMARY_RUN_CONFIG: dict[str, Any] = {
    **M3_FINAL_RECOVERY_TOKEN_TRIGGER_RUN_CONFIG,
    "systems": [
        {
            "agent_config": "summary_strategic",
            "llm_config": "nova-lite",
        },
        {
            "agent_config": "planner_summary_strategic",
            "llm_config": "nova-lite",
        },
    ],
}


M3_FINAL_INCREMENTAL_RUN_CONFIG: dict[str, Any] = {
    **M3_FINAL_RECOVERY_RUN_CONFIG,
    "systems": [
        {
            "agent_config": "baseline_incremental",
            "llm_config": "nova-lite",
        },
        {
            "agent_config": "planner_incremental",
            "llm_config": "nova-lite",
        },
        {
            "agent_config": "summary_incremental",
            "llm_config": "nova-lite",
        },
        {
            "agent_config": "planner_summary_incremental",
            "llm_config": "nova-lite",
        },
    ],
}


M3_FINAL_TOKEN_TRIGGER_RUN_CONFIG: dict[str, Any] = {
    **M3_FINAL_INCREMENTAL_RUN_CONFIG,
    "systems": [
        {
            "agent_config": "summary_incremental_token_trigger",
            "llm_config": "nova-lite",
        },
        {
            "agent_config": "planner_summary_incremental_token_trigger",
            "llm_config": "nova-lite",
        },
    ],
}


M3_FINAL_STRATEGIC_SUMMARY_RUN_CONFIG: dict[str, Any] = {
    **M3_FINAL_TOKEN_TRIGGER_RUN_CONFIG,
    "systems": [
        {
            "agent_config": "summary_incremental_strategic",
            "llm_config": "nova-lite",
        },
        {
            "agent_config": "planner_summary_incremental_strategic",
            "llm_config": "nova-lite",
        },
    ],
}
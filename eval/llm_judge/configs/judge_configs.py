"""Configuraciones de ejecuciones del LLM-as-judge."""

from __future__ import annotations

from typing import Any


# La configuración activa corresponde exclusivamente al smoke reproducible.
# La configuración de calibración final todavía no está definida; cuando se
# defina, se declarará con un nombre propio:
#
# M3_..._JUDGE_CONFIG: dict[str, Any] = {
#     "dataset_id": "...",
#     "judge_eval_id": "...",
#     "split": "dev",
#     "judge_llm_config": "...",
#     "max_repair_attempts": 2,
# }
#
# JUDGE_CONFIG = M3_..._JUDGE_CONFIG
M3_LLM_JUDGE_SMOKE_HOLDOUT_CONFIG: dict[str, Any] = {
    "dataset_id": "qualitative-llm-judge-smoke-v1",
    "judge_eval_id": "m3-llm-judge-smoke-holdout-001",
    "split": "holdout",
    "judge_llm_config": "nova-pro",
    "max_repair_attempts": 2,
}


M3_QUALITATIVE_JUDGE_CALIBRATION_CONFIG: dict[str, Any] = {
    "dataset_id": "m3-qualitative-final-v2",
    "judge_eval_id": "m3-qualitative-judge-calibration-003",
    "split": "dev",
    "judge_llm_config": "claude-opus-4.5",
    "max_repair_attempts": 2,
}


M3_QUALITATIVE_JUDGE_HOLDOUT_CONFIG: dict[str, Any] = {
    "dataset_id": "m3-qualitative-final-v2",
    "judge_eval_id": "m3-qualitative-judge-holdout-001",
    "split": "holdout",
    "judge_llm_config": "claude-opus-4.5",
    "max_repair_attempts": 2,
}


JUDGE_CONFIG = M3_QUALITATIVE_JUDGE_HOLDOUT_CONFIG
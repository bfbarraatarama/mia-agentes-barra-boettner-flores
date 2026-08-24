"""Configuraciones de ejecuciones del LLM-as-judge."""

from __future__ import annotations

from typing import Any


# Se mantiene intencionalmente sin configurar hasta definir el dataset
# de calibración y la configuración concreta del judge.
#
# Cuando exista una configuración real, se declarará con nombre propio:
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


JUDGE_CONFIG = M3_LLM_JUDGE_SMOKE_HOLDOUT_CONFIG
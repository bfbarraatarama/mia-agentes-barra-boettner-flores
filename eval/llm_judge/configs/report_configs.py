"""Configuraciones de reportes cualitativos y de calibración."""

from __future__ import annotations

from typing import Any


# Las configuraciones activas corresponden exclusivamente a reportes del smoke.
# El reporte de calibración final todavía no está definido.
#
# Una configuración podrá seleccionar una o varias secciones:
#
# M3_..._REPORT_CONFIG: dict[str, Any] = {
#     "status": {
#         "dataset_id": "...",
#         "judge_eval_id": "...",
#     },
#     "judge_agreement": {
#         "dataset_id": "...",
#         "judge_eval_id": "...",
#         "annotator_id": "...",
#     },
#     "human_agreement": {
#         "dataset_id": "...",
#         "annotator_a_id": "...",
#         "annotator_b_id": "...",
#         "split": "dev",
#     },
# }
#
# REPORT_CONFIG = M3_..._REPORT_CONFIG
M3_LLM_JUDGE_SMOKE_DEV_REPORT_CONFIG: dict[str, Any] = {
    "report_id": "m3-llm-judge-smoke-dev-001",
    "status": {
        "dataset_id": "qualitative-llm-judge-smoke-v1",
        "judge_eval_id": "m3-llm-judge-smoke-dev-001",
    },
    "judge_agreement": {
        "dataset_id": "qualitative-llm-judge-smoke-v1",
        "judge_eval_id": "m3-llm-judge-smoke-dev-001",
        "annotator_id": "bruno",
    },
}


M3_LLM_JUDGE_SMOKE_HOLDOUT_REPORT_CONFIG: dict[str, Any] = {
    "report_id": "m3-llm-judge-smoke-holdout-001",
    "status": {
        "dataset_id": "qualitative-llm-judge-smoke-v1",
        "judge_eval_id": "m3-llm-judge-smoke-holdout-001",
    },
    "judge_agreement": {
        "dataset_id": "qualitative-llm-judge-smoke-v1",
        "judge_eval_id": "m3-llm-judge-smoke-holdout-001",
        "annotator_id": "bruno",
    },
}


REPORT_CONFIG = M3_LLM_JUDGE_SMOKE_DEV_REPORT_CONFIG
"""Configuraciones de reportes cualitativos y de calibración."""

from __future__ import annotations

from typing import Any


# Se mantiene intencionalmente sin configurar hasta definir el dataset
# de calibración, las evaluaciones del judge y los anotadores reales.
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
REPORT_CONFIG: dict[str, Any] | None = None
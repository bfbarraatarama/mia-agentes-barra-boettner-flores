"""Registro de análisis disponibles para evaluaciones M3."""

from __future__ import annotations

from eval.error_analysis import analyze_errors


ANALYSES = {
    "error_analysis": analyze_errors,
}
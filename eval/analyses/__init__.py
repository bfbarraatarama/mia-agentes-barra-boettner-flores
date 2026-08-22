"""Registro de análisis disponibles para evaluaciones M3."""

from __future__ import annotations

from eval.analyses.context_analysis import analyze_context
from eval.analyses.error_analysis import analyze_errors
from eval.analyses.tool_call_repair_analysis import (
    analyze_tool_call_repair,
)


ANALYSES = {
    "error_analysis": analyze_errors,
    "tool_call_repair_analysis": analyze_tool_call_repair,
    "context_analysis": analyze_context,
}
"""Configuraciones de evaluación para M3."""

from __future__ import annotations

from typing import Any


M3_EVALUATION_CONFIG: dict[str, Any] = {
    "metrics": [
        "success_rate",
    ],
    "analyses": [
        "error_analysis",
        "tool_call_repair_analysis",
        # "cost_analysis",
        # "qualitative_analysis",
    ],
}
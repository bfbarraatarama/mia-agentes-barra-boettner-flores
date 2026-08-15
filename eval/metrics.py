"""Métricas para la evaluación de M3."""

from __future__ import annotations

from typing import Any


def success_rate(runs: list[dict[str, Any]]) -> float:
    """Calcula la proporción de ejecuciones que alcanzaron el objetivo."""

    if not runs:
        raise ValueError("success_rate requiere al menos una ejecución.")

    successful_runs = sum(
        1 for run in runs if run["goal_achieved"]
    )

    return successful_runs / len(runs)


METRICS = {
    "success_rate": success_rate,
}
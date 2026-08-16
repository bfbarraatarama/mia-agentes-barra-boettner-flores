"""Métricas para la evaluación de M3."""

from __future__ import annotations

from typing import Any


def success_rate(trials: list[dict[str, Any]]) -> float:
    """Calcula la proporción de trials que alcanzaron el objetivo."""

    if not trials:
        raise ValueError("success_rate requiere al menos un trial.")

    successful_trials = sum(
        1 for trial in trials if trial["goal_achieved"]
    )

    return successful_trials / len(trials)


METRICS = {
    "success_rate": success_rate,
}
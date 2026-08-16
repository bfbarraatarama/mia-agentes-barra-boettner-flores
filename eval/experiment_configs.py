"""Configuraciones de experimentación para M3."""

from __future__ import annotations

from typing import Any


CONTINUATION_MESSAGE = "El desafío todavía no está completado. Continuá."


SINGLE_ATTEMPT_CONFIG: dict[str, Any] = {
    "max_attempts": 1,
    "continuation_message": CONTINUATION_MESSAGE,
}


SINGLE_CONTINUATION_CONFIG: dict[str, Any] = {
    "max_attempts": 2,
    "continuation_message": CONTINUATION_MESSAGE,
}


EXPERIMENT_CONFIGS: dict[str, dict[str, Any]] = {
    "single_attempt": SINGLE_ATTEMPT_CONFIG,
    "single_continuation": SINGLE_CONTINUATION_CONFIG,
}

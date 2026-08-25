"""Configuraciones de trials para M3."""

from __future__ import annotations

from typing import Any


CONTINUATION_MESSAGE = "El desafío todavía no está completado. Continuá."


MAX_ITERATIONS_RECOVERY_MESSAGE = (
    "El intento anterior terminó porque alcanzó el límite externo de "
    "iteraciones. Esto no implica que la última acción haya fallado. "
    "El estado alcanzado hasta ese momento se conserva."
)


CONTEXT_OVERFLOW_RECOVERY_MESSAGE = (
    "El intento anterior terminó porque la ronda solicitada no cabía "
    "completa dentro del presupuesto de historial configurado. "
    "La ronda fue rechazada completa y sus acciones no se ejecutaron. "
    "Esto no implica que las acciones solicitadas fueran inválidas. "
    "El estado alcanzado hasta ese momento se conserva."
)


DEFAULT_ATTEMPT_RECOVERY_MESSAGES: dict[str, str] = {
    "max_iterations": MAX_ITERATIONS_RECOVERY_MESSAGE,
    "context_overflow": CONTEXT_OVERFLOW_RECOVERY_MESSAGE,
}


SINGLE_ATTEMPT_CONFIG: dict[str, Any] = {
    "max_attempts": 1,
    "continuation_message": CONTINUATION_MESSAGE,
}


SINGLE_CONTINUATION_CONFIG: dict[str, Any] = {
    "max_attempts": 2,
    "continuation_message": CONTINUATION_MESSAGE,
}


MULTI_ATTEMPT_CONFIG: dict[str, Any] = {
    "max_attempts": 10,
    "continuation_message": CONTINUATION_MESSAGE,
}


MULTI_ATTEMPT_RECOVERY_CONFIG: dict[str, Any] = {
    "max_attempts": 10,
    "continuation_message": CONTINUATION_MESSAGE,
    "recoverable_attempt_terminations": {
        "max_iterations": MAX_ITERATIONS_RECOVERY_MESSAGE,
        "context_overflow": CONTEXT_OVERFLOW_RECOVERY_MESSAGE,
    },
    "attempt_recovery_max_recoveries": {
        "max_iterations": 1,
    },
}


TRIAL_CONFIGS: dict[str, dict[str, Any]] = {
    "single_attempt": SINGLE_ATTEMPT_CONFIG,
    "single_continuation": SINGLE_CONTINUATION_CONFIG,
    "multi_attempt": MULTI_ATTEMPT_CONFIG,
    "multi_attempt_recovery": MULTI_ATTEMPT_RECOVERY_CONFIG,
}

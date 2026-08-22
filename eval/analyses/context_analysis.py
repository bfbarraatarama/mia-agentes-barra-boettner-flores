"""Análisis de presión de contexto en corridas M3 (issue #26).

Caracteriza, a partir de artefactos ya persistidos, cuánto limita el
presupuesto de historial y si el consumo de contexto es genuino o
producto de comportamiento redundante:

- terminaciones por presupuesto insuficiente, en qué attempt y tras
  cuántas iteraciones;
- distribución de tool calls por iteración (presión estructural: cada
  iteración agrega 1 + tool_calls mensajes);
- acciones repetidas dentro del trial (misma herramienta + argumentos +
  observación), con la misma semántica de clave que
  eval/llm_judge/cases.py::_action_key;
- re-derivación entre attempts: cuántas acciones del attempt N ya se
  habían ejecutado en attempts anteriores;
- ocupación de la ventana observada en cada llamada al LLM;
- costo del compactor de historial cuando está activo
  (purpose="history_compaction").
"""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Any


_BUDGET_ERROR_MARKER = "no cabe en max_history_messages"


def _new_system_stats() -> dict[str, Any]:
    return {
        "trials": 0,
        "attempts": 0,
        "budget_terminated_trials": 0,
        "budget_terminated_attempts": 0,
        "budget_termination_by_attempt_index": defaultdict(int),
        "iterations_at_budget_termination": [],
        "tool_calls_per_iteration": defaultdict(int),
        "max_messages_seen": 0,
        "llm_calls_at_window_limit": 0,
        "agent_llm_calls": 0,
        "total_actions": 0,
        "repeated_actions": 0,
        "trials_with_repetition": 0,
        "cross_attempt_actions": 0,
        "cross_attempt_repeated": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "compaction_events": 0,
        "compaction_failures": 0,
        "compaction_llm_calls": 0,
        "compaction_input_tokens": 0,
        "compaction_output_tokens": 0,
    }


def _action_key(
    step: dict[str, Any],
) -> tuple[str | None, str | None, str | None, str | None]:
    """Clave estable de una acción ejecutada.

    Misma semántica que eval/llm_judge/cases.py::_action_key
    (herramienta, argumentos normalizados, observación, error), pero
    sobre los AgentStep persistidos en agent_result.steps.
    """

    tool_input = step.get("tool_input")

    if tool_input:
        try:
            arguments_key = json.dumps(
                json.loads(tool_input),
                sort_keys=True,
                ensure_ascii=False,
                separators=(",", ":"),
            )
        except (json.JSONDecodeError, TypeError):
            arguments_key = tool_input
    else:
        arguments_key = tool_input

    return (
        step.get("tool_name"),
        arguments_key,
        step.get("tool_output"),
        step.get("error"),
    )


def _is_budget_termination(agent_result: dict[str, Any]) -> bool:
    error = agent_result.get("error") or ""

    return _BUDGET_ERROR_MARKER in error


def _window_limit_for(
    manifest: dict[str, Any] | None,
    agent_config_name: str,
) -> int | None:
    if manifest is None:
        return None

    agent_config = manifest.get("agent_configs", {}).get(
        agent_config_name,
        {},
    )

    return agent_config.get("max_history_messages")


def _accumulate_attempt(
    system: dict[str, Any],
    attempt: dict[str, Any],
    window_limit: int | None,
) -> None:
    """Vuelca las métricas de traza y de terminación de un attempt."""

    agent_result = attempt.get("agent_result", {})

    input_tokens = agent_result.get("input_tokens")
    output_tokens = agent_result.get("output_tokens")

    if input_tokens is not None:
        system["input_tokens"] += input_tokens

    if output_tokens is not None:
        system["output_tokens"] += output_tokens

    agent_iterations = 0

    for event in attempt.get("trace", []):
        event_type = event.get("type")

        if event_type == "history_compaction":
            system["compaction_events"] += 1

            if event.get("error") is not None:
                system["compaction_failures"] += 1

            continue

        if event_type != "llm_call":
            continue

        purpose = event.get("purpose")
        response = event.get("response")

        if purpose == "history_compaction":
            system["compaction_llm_calls"] += 1

            if response is not None:
                system["compaction_input_tokens"] += (
                    response.get("input_tokens") or 0
                )
                system["compaction_output_tokens"] += (
                    response.get("output_tokens") or 0
                )

            continue

        if purpose != "agent":
            continue

        system["agent_llm_calls"] += 1

        messages = event.get("messages")

        if messages is not None:
            message_count = len(messages)
            system["max_messages_seen"] = max(
                system["max_messages_seen"],
                message_count,
            )

            if (
                window_limit is not None
                and message_count >= window_limit
            ):
                system["llm_calls_at_window_limit"] += 1

        if response is not None:
            agent_iterations += 1
            tool_call_count = len(response.get("tool_calls") or [])
            system["tool_calls_per_iteration"][tool_call_count] += 1

    if _is_budget_termination(agent_result):
        system["budget_terminated_attempts"] += 1
        system["budget_termination_by_attempt_index"][
            attempt.get("attempt_index")
        ] += 1
        system["iterations_at_budget_termination"].append(
            agent_iterations
        )


def _accumulate_trial_actions(
    system: dict[str, Any],
    trial: dict[str, Any],
) -> None:
    """Mide repetición intra-trial y re-derivación entre attempts."""

    seen_in_trial: set[Any] = set()
    seen_in_previous_attempts: set[Any] = set()
    trial_actions = 0
    trial_repeated = 0

    for attempt in trial.get("attempts", []):
        attempt_keys = []

        for step in attempt.get("agent_result", {}).get("steps", []):
            key = _action_key(step)
            attempt_keys.append(key)

            trial_actions += 1

            if key in seen_in_trial:
                trial_repeated += 1
            else:
                seen_in_trial.add(key)

            if attempt.get("attempt_index", 1) > 1:
                system["cross_attempt_actions"] += 1

                if key in seen_in_previous_attempts:
                    system["cross_attempt_repeated"] += 1

        seen_in_previous_attempts.update(attempt_keys)

    system["total_actions"] += trial_actions
    system["repeated_actions"] += trial_repeated

    if trial_repeated > 0:
        system["trials_with_repetition"] += 1


def _finalize_stats(stats: dict[str, Any]) -> dict[str, Any]:
    """Convierte acumuladores en un dict serializable con derivados."""

    iterations = stats["iterations_at_budget_termination"]

    finalized = dict(stats)
    finalized["budget_termination_by_attempt_index"] = dict(
        sorted(stats["budget_termination_by_attempt_index"].items())
    )
    finalized["tool_calls_per_iteration"] = dict(
        sorted(stats["tool_calls_per_iteration"].items())
    )
    finalized["iterations_at_budget_termination"] = {
        "min": min(iterations) if iterations else None,
        "mean": (
            round(sum(iterations) / len(iterations), 2)
            if iterations
            else None
        ),
        "max": max(iterations) if iterations else None,
    }
    finalized["repeated_action_ratio"] = (
        round(stats["repeated_actions"] / stats["total_actions"], 4)
        if stats["total_actions"]
        else None
    )
    finalized["cross_attempt_repeated_ratio"] = (
        round(
            stats["cross_attempt_repeated"]
            / stats["cross_attempt_actions"],
            4,
        )
        if stats["cross_attempt_actions"]
        else None
    )

    return finalized


def analyze_context(
    run_sources: list[dict[str, Any]],
) -> dict[str, Any]:
    """Caracteriza la presión de contexto de una o más corridas."""

    if not run_sources:
        raise ValueError(
            "run_sources debe contener al menos una fuente de run."
        )

    run_ids = [
        source["run_id"]
        for source in run_sources
    ]

    systems: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    totals = _new_system_stats()

    for source in run_sources:
        manifest = source.get("manifest")

        for result in source["result"]["results"]:
            agent_config = result["agent_config"]
            model = result["llm_config"]

            window_limit = _window_limit_for(
                manifest,
                agent_config,
            )

            system = systems[agent_config].setdefault(
                model,
                _new_system_stats(),
            )
            system["max_history_messages"] = window_limit

            for trial in result["trials"]:
                for stats in (system, totals):
                    stats["trials"] += 1

                trial_budget_terminated = False

                for attempt in trial["attempts"]:
                    for stats in (system, totals):
                        stats["attempts"] += 1
                        _accumulate_attempt(
                            stats,
                            attempt,
                            window_limit,
                        )

                    if _is_budget_termination(
                        attempt.get("agent_result", {})
                    ):
                        trial_budget_terminated = True

                if trial_budget_terminated:
                    system["budget_terminated_trials"] += 1
                    totals["budget_terminated_trials"] += 1

                _accumulate_trial_actions(system, trial)
                _accumulate_trial_actions(totals, trial)

    analysis = {
        "run_ids": run_ids,
        "totals": _finalize_stats(totals),
        "systems": {
            agent_config: {
                model: _finalize_stats(values)
                for model, values in models.items()
            }
            for agent_config, models in systems.items()
        },
    }

    if len(run_ids) == 1:
        analysis["run_id"] = run_ids[0]

    return analysis


def _format_ratio(value: float | None) -> str:
    if value is None:
        return "n/a"

    return f"{value:.2%}"


def _stats_table_lines(values: dict[str, Any]) -> list[str]:
    iterations = values["iterations_at_budget_termination"]

    lines = [
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Trials | {values['trials']} |",
        f"| Attempts | {values['attempts']} |",
        (
            "| Trials terminados por presupuesto | "
            f"{values['budget_terminated_trials']} |"
        ),
        (
            "| Attempts terminados por presupuesto | "
            f"{values['budget_terminated_attempts']} |"
        ),
        (
            "| Terminaciones por attempt_index | "
            f"{values['budget_termination_by_attempt_index'] or '—'} |"
        ),
        (
            "| Iteraciones al morir (min/media/max) | "
            f"{iterations['min']} / {iterations['mean']} / "
            f"{iterations['max']} |"
        ),
        (
            "| Tool calls por iteración | "
            f"{values['tool_calls_per_iteration'] or '—'} |"
        ),
        (
            "| Máximo de mensajes enviados | "
            f"{values['max_messages_seen']} |"
        ),
        (
            "| Llamadas con la ventana llena | "
            f"{values['llm_calls_at_window_limit']} |"
        ),
        f"| Acciones ejecutadas | {values['total_actions']} |",
        (
            "| Acciones repetidas (intra-trial) | "
            f"{values['repeated_actions']} "
            f"({_format_ratio(values['repeated_action_ratio'])}) |"
        ),
        (
            "| Trials con repetición | "
            f"{values['trials_with_repetition']} |"
        ),
        (
            "| Acciones re-derivadas entre attempts | "
            f"{values['cross_attempt_repeated']} de "
            f"{values['cross_attempt_actions']} "
            f"({_format_ratio(values['cross_attempt_repeated_ratio'])}) |"
        ),
        (
            "| Tokens entrada / salida | "
            f"{values['input_tokens']} / {values['output_tokens']} |"
        ),
        (
            "| Compactaciones (eventos / fallas) | "
            f"{values['compaction_events']} / "
            f"{values['compaction_failures']} |"
        ),
        (
            "| Tokens del compactor (in / out) | "
            f"{values['compaction_input_tokens']} / "
            f"{values['compaction_output_tokens']} |"
        ),
    ]

    return lines


def render_markdown(analysis: dict[str, Any]) -> str:
    """Renderiza el análisis de contexto como Markdown."""

    lines = ["# Análisis de presión de contexto — M3\n"]

    run_ids = analysis.get("run_ids") or [analysis["run_id"]]

    if len(run_ids) == 1:
        lines.append(f"**Run:** `{run_ids[0]}`\n")
    else:
        runs = ", ".join(f"`{run_id}`" for run_id in run_ids)
        lines.append(f"**Runs:** {runs}\n")

    lines.append("## Totales\n")
    lines.extend(_stats_table_lines(analysis["totals"]))
    lines.append("")

    lines.append("## Por sistema\n")

    for agent_config, models in analysis["systems"].items():
        for model, values in models.items():
            window = values.get("max_history_messages")
            lines.append(
                f"### `{agent_config}` / `{model}` "
                f"(ventana: {window})\n"
            )
            lines.extend(_stats_table_lines(values))
            lines.append("")

    return "\n".join(lines)

"""Análisis de actividad y costo de reparación de tool calls en M3."""

from __future__ import annotations

from collections import defaultdict
from typing import Any


def analyze_tool_call_repair(
    run_manifest: dict[str, Any],
    run_result: dict[str, Any],
) -> dict[str, Any]:
    """Resume las llamadas al LLM dedicadas a reparar tool calls."""

    systems: dict[
        str,
        dict[str, dict[str, int]],
    ] = defaultdict(
        lambda: defaultdict(
            lambda: {
                "trials": 0,
                "trials_with_repair": 0,
                "repair_llm_calls": 0,
                "repair_llm_responses": 0,
                "repair_llm_errors": 0,
                "repair_llm_calls_with_token_usage": 0,
                "repair_llm_calls_without_token_usage": 0,
                "repair_input_tokens": 0,
                "repair_output_tokens": 0,
            }
        )
    )

    total_trials = 0
    trials_with_repair = 0
    repair_llm_calls = 0
    repair_llm_responses = 0
    repair_llm_errors = 0
    repair_llm_calls_with_token_usage = 0
    repair_llm_calls_without_token_usage = 0
    repair_input_tokens = 0
    repair_output_tokens = 0

    for result in run_result["results"]:
        agent_config = result["agent_config"]
        model = result["llm_config"]
        system = systems[agent_config][model]

        for trial in result["trials"]:
            total_trials += 1
            system["trials"] += 1

            trial_repair_calls = 0

            for attempt in trial["attempts"]:
                for event in attempt.get("trace", []):
                    if (
                        event.get("type") != "llm_call"
                        or event.get("purpose") != "tool_call_repair"
                    ):
                        continue

                    trial_repair_calls += 1
                    repair_llm_calls += 1
                    system["repair_llm_calls"] += 1

                    if event.get("error") is not None:
                        repair_llm_errors += 1
                        system["repair_llm_errors"] += 1

                    response = event.get("response")

                    if response is not None:
                        repair_llm_responses += 1
                        system["repair_llm_responses"] += 1

                    input_tokens = (
                        response.get("input_tokens")
                        if response is not None
                        else None
                    )
                    output_tokens = (
                        response.get("output_tokens")
                        if response is not None
                        else None
                    )

                    if input_tokens is not None:
                        repair_input_tokens += input_tokens
                        system["repair_input_tokens"] += input_tokens

                    if output_tokens is not None:
                        repair_output_tokens += output_tokens
                        system["repair_output_tokens"] += output_tokens

                    if (
                        input_tokens is not None
                        and output_tokens is not None
                    ):
                        repair_llm_calls_with_token_usage += 1
                        system[
                            "repair_llm_calls_with_token_usage"
                        ] += 1
                    else:
                        repair_llm_calls_without_token_usage += 1
                        system[
                            "repair_llm_calls_without_token_usage"
                        ] += 1

            if trial_repair_calls > 0:
                trials_with_repair += 1
                system["trials_with_repair"] += 1

    return {
        "run_id": run_manifest["run_id"],
        "total_trials": total_trials,
        "trials_with_repair": trials_with_repair,
        "repair_llm_calls": repair_llm_calls,
        "repair_llm_responses": repair_llm_responses,
        "repair_llm_errors": repair_llm_errors,
        "repair_llm_calls_with_token_usage": (
            repair_llm_calls_with_token_usage
        ),
        "repair_llm_calls_without_token_usage": (
            repair_llm_calls_without_token_usage
        ),
        "repair_input_tokens": repair_input_tokens,
        "repair_output_tokens": repair_output_tokens,
        "token_usage_complete": (
            repair_llm_calls_without_token_usage == 0
        ),
        "systems": {
            agent_config: {
                model: {
                    **values,
                    "token_usage_complete": (
                        values[
                            "repair_llm_calls_without_token_usage"
                        ]
                        == 0
                    ),
                }
                for model, values in models.items()
            }
            for agent_config, models in systems.items()
        },
    }


def render_markdown(
    analysis: dict[str, Any],
) -> str:
    """Renderiza el análisis de reparación como Markdown."""

    lines = []

    token_usage_complete = (
        "sí"
        if analysis["token_usage_complete"]
        else "no"
    )

    lines.append(
        "# Análisis de reparación de tool calls — M3\n"
    )
    lines.append(
        f"**Run:** `{analysis['run_id']}`\n"
    )

    lines.append("## Resumen\n")
    lines.append("| Métrica | Valor |")
    lines.append("|---|---:|")
    lines.append(
        f"| Trials totales | {analysis['total_trials']} |"
    )
    lines.append(
        "| Trials con reparación | "
        f"{analysis['trials_with_repair']} |"
    )
    lines.append(
        "| Llamadas físicas de reparación | "
        f"{analysis['repair_llm_calls']} |"
    )
    lines.append(
        "| Respuestas del LLM | "
        f"{analysis['repair_llm_responses']} |"
    )
    lines.append(
        "| Errores de llamada | "
        f"{analysis['repair_llm_errors']} |"
    )
    lines.append(
        "| Llamadas con usage completo | "
        f"{analysis['repair_llm_calls_with_token_usage']} |"
    )
    lines.append(
        "| Llamadas sin usage completo | "
        f"{analysis['repair_llm_calls_without_token_usage']} |"
    )
    lines.append(
        "| Tokens de entrada reportados | "
        f"{analysis['repair_input_tokens']} |"
    )
    lines.append(
        "| Tokens de salida reportados | "
        f"{analysis['repair_output_tokens']} |"
    )
    lines.append(
        "| Cobertura de tokens completa | "
        f"{token_usage_complete} |"
    )
    lines.append("")

    lines.append("## Por sistema\n")

    for agent_config, models in analysis["systems"].items():
        for model, values in models.items():
            system_usage_complete = (
                "sí"
                if values["token_usage_complete"]
                else "no"
            )

            lines.append(
                f"### `{agent_config}` / `{model}`\n"
            )
            lines.append("| Métrica | Valor |")
            lines.append("|---|---:|")
            lines.append(
                f"| Trials | {values['trials']} |"
            )
            lines.append(
                "| Trials con reparación | "
                f"{values['trials_with_repair']} |"
            )
            lines.append(
                "| Llamadas físicas de reparación | "
                f"{values['repair_llm_calls']} |"
            )
            lines.append(
                "| Respuestas del LLM | "
                f"{values['repair_llm_responses']} |"
            )
            lines.append(
                "| Errores de llamada | "
                f"{values['repair_llm_errors']} |"
            )
            lines.append(
                "| Llamadas con usage completo | "
                f"{values['repair_llm_calls_with_token_usage']} |"
            )
            lines.append(
                "| Llamadas sin usage completo | "
                f"{values['repair_llm_calls_without_token_usage']} |"
            )
            lines.append(
                "| Tokens de entrada reportados | "
                f"{values['repair_input_tokens']} |"
            )
            lines.append(
                "| Tokens de salida reportados | "
                f"{values['repair_output_tokens']} |"
            )
            lines.append(
                "| Cobertura de tokens completa | "
                f"{system_usage_complete} |"
            )
            lines.append("")

    return "\n".join(lines)

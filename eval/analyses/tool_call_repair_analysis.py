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
                "repair_input_tokens": 0,
                "repair_output_tokens": 0,
            }
        )
    )

    total_trials = 0
    trials_with_repair = 0
    repair_llm_calls = 0
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

                    response = event.get("response")
                    if response is None:
                        continue

                    input_tokens = response.get("input_tokens", 0)
                    output_tokens = response.get("output_tokens", 0)

                    repair_input_tokens += input_tokens
                    repair_output_tokens += output_tokens
                    system["repair_input_tokens"] += input_tokens
                    system["repair_output_tokens"] += output_tokens

            if trial_repair_calls > 0:
                trials_with_repair += 1
                system["trials_with_repair"] += 1

    return {
        "run_id": run_manifest["run_id"],
        "total_trials": total_trials,
        "trials_with_repair": trials_with_repair,
        "repair_llm_calls": repair_llm_calls,
        "repair_input_tokens": repair_input_tokens,
        "repair_output_tokens": repair_output_tokens,
        "systems": {
            agent_config: {
                model: dict(values)
                for model, values in models.items()
            }
            for agent_config, models in systems.items()
        },
    }
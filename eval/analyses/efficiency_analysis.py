"""Análisis de consumo y eficiencia de configuraciones en M3."""

from __future__ import annotations

from collections import defaultdict
from typing import Any


def _empty_metrics() -> dict[str, Any]:
    return {
        "trials": 0,
        "successful_trials": 0,
        "attempts_total": 0,
        "retries_total": 0,
        "llm_calls_total": 0,
        "llm_calls_by_purpose": defaultdict(int),
        "tool_executions_total": 0,
        "tool_executions_by_tool": defaultdict(int),
        "steps_total": 0,
        "input_tokens_total": 0,
        "output_tokens_total": 0,
        "input_tokens_by_purpose": defaultdict(int),
        "output_tokens_by_purpose": defaultdict(int),
    }


def _accumulate_trial(
    metrics: dict[str, Any],
    trial: dict[str, Any],
) -> None:
    metrics["trials"] += 1
    if trial.get("goal_achieved"):
        metrics["successful_trials"] += 1

    attempts = trial.get("attempts", [])
    metrics["attempts_total"] += len(attempts)

    for attempt in attempts:
        agent_result = attempt.get("agent_result") or {}
        metrics["steps_total"] += len(agent_result.get("steps") or [])

        for event in attempt.get("trace", []):
            event_type = event.get("type")
            purpose = event.get("purpose")

            if event_type == "llm_call":
                if event.get("retry_index", 0) > 0:
                    metrics["retries_total"] += 1

                metrics["llm_calls_total"] += 1
                metrics["llm_calls_by_purpose"][purpose] += 1

                response = event.get("response") or {}
                input_tokens = response.get("input_tokens") or 0
                output_tokens = response.get("output_tokens") or 0

                metrics["input_tokens_total"] += input_tokens
                metrics["output_tokens_total"] += output_tokens
                metrics["input_tokens_by_purpose"][purpose] += input_tokens
                metrics["output_tokens_by_purpose"][purpose] += output_tokens

            elif event_type == "tool_execution":
                tool_name = event.get("tool_name", "unknown")
                metrics["tool_executions_total"] += 1
                metrics["tool_executions_by_tool"][tool_name] += 1


def _averages(metrics: dict[str, Any]) -> dict[str, Any]:
    n = metrics["trials"]
    if n == 0:
        return {}

    successes = metrics["successful_trials"]
    success_rate = successes / n

    def per_trial(value: int) -> float:
        return round(value / n, 2)

    def per_success(value: int) -> float | None:
        return round(value / successes, 2) if successes > 0 else None

    total_tokens = (
        metrics["input_tokens_total"] + metrics["output_tokens_total"]
    )

    purposes = set(metrics["llm_calls_by_purpose"]) | set(
        metrics["input_tokens_by_purpose"]
    )

    by_purpose = {}
    for purpose in sorted(purposes, key=lambda x: (x is None, x)):
        key = purpose if purpose is not None else "unknown"
        by_purpose[key] = {
            "llm_calls_per_trial": per_trial(
                metrics["llm_calls_by_purpose"][purpose]
            ),
            "input_tokens_per_trial": per_trial(
                metrics["input_tokens_by_purpose"][purpose]
            ),
            "output_tokens_per_trial": per_trial(
                metrics["output_tokens_by_purpose"][purpose]
            ),
            "total_tokens_per_trial": per_trial(
                metrics["input_tokens_by_purpose"][purpose]
                + metrics["output_tokens_by_purpose"][purpose]
            ),
        }

    by_tool = {
        tool: per_trial(count)
        for tool, count in sorted(
            metrics["tool_executions_by_tool"].items(),
            key=lambda x: -x[1],
        )
    }

    return {
        "trials": n,
        "successful_trials": successes,
        "success_rate": round(success_rate, 4),
        "attempts_per_trial": per_trial(metrics["attempts_total"]),
        "attempts_per_success": per_success(metrics["attempts_total"]),
        "retries_per_trial": per_trial(metrics["retries_total"]),
        "llm_calls_per_trial": per_trial(metrics["llm_calls_total"]),
        "tool_executions_per_trial": per_trial(
            metrics["tool_executions_total"]
        ),
        "steps_per_trial": per_trial(metrics["steps_total"]),
        "input_tokens_per_trial": per_trial(metrics["input_tokens_total"]),
        "output_tokens_per_trial": per_trial(metrics["output_tokens_total"]),
        "total_tokens_per_trial": per_trial(total_tokens),
        "llm_calls_per_success": per_success(metrics["llm_calls_total"]),
        "tool_executions_per_success": per_success(
            metrics["tool_executions_total"]
        ),
        "steps_per_success": per_success(metrics["steps_total"]),
        "total_tokens_per_success": per_success(total_tokens),
        "by_purpose": by_purpose,
        "by_tool": by_tool,
    }


def analyze_efficiency(
    run_sources: list[dict[str, Any]],
) -> dict[str, Any]:
    """Analiza consumo y eficiencia por configuración y escenario."""

    if not run_sources:
        raise ValueError(
            "run_sources debe contener al menos una fuente de run."
        )

    run_ids = [source["run_id"] for source in run_sources]

    # (agent_config, llm_config, trial_config) -> scenario -> metrics
    systems: dict[
        tuple[str, str, str],
        dict[str, dict[str, Any]],
    ] = defaultdict(lambda: defaultdict(_empty_metrics))

    # (agent_config, llm_config, trial_config) -> global metrics
    global_metrics: dict[tuple[str, str, str], dict[str, Any]] = defaultdict(
        _empty_metrics
    )

    for source in run_sources:
        for case in source["result"]["results"]:
            agent_config = case["agent_config"]
            llm_config = case["llm_config"]
            trial_config = case["trial_config"]
            scenario = case["scenario"]
            key = (agent_config, llm_config, trial_config)

            for trial in case["trials"]:
                _accumulate_trial(systems[key][scenario], trial)
                _accumulate_trial(global_metrics[key], trial)

    results = {}
    for (agent_config, llm_config, trial_config), scenarios in systems.items():
        key = (agent_config, llm_config, trial_config)
        system_key = f"{agent_config} / {llm_config} / {trial_config}"
        results[system_key] = {
            "agent_config": agent_config,
            "llm_config": llm_config,
            "trial_config": trial_config,
            "by_scenario": {
                scenario: _averages(metrics)
                for scenario, metrics in scenarios.items()
            },
            "global": _averages(global_metrics[key]),
        }

    return {
        "run_ids": run_ids,
        "systems": results,
    }


def _fmt(value: float | None, decimals: int = 1) -> str:
    if value is None:
        return "N/A"
    if decimals == 0:
        return f"{value:,.0f}"
    return f"{value:,.{decimals}f}"


def render_markdown(analysis: dict[str, Any]) -> str:
    """Renderiza el análisis de eficiencia como Markdown."""

    lines: list[str] = []

    run_ids = analysis["run_ids"]
    if len(run_ids) == 1:
        lines.append("# Análisis de consumo y eficiencia — M3\n")
        lines.append(f"**Run:** `{run_ids[0]}`\n")
    else:
        runs = ", ".join(f"`{r}`" for r in run_ids)
        lines.append("# Análisis de consumo y eficiencia — M3\n")
        lines.append(f"**Runs:** {runs}\n")

    for system_key, system in analysis["systems"].items():
        lines.append(f"## {system_key}\n")

        by_scenario = system["by_scenario"]
        g = system["global"]

        # Tabla 1 — Consumo por escenario
        lines.append("### Consumo por escenario\n")
        lines.append(
            "*Valores promedio por trial. "
            "**Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. "
            "**Retries**: número de intentos adicionales de llamadas al LLM "
            "debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*\n"
        )
        lines.append(
            "| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps "
            "| Input tokens | Output tokens | Total tokens |"
        )
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")

        for scenario, m in by_scenario.items():
            lines.append(
                f"| {scenario} "
                f"| {m['trials']} "
                f"| {_fmt(m['attempts_per_trial'])} "
                f"| {_fmt(m['retries_per_trial'])} "
                f"| {_fmt(m['llm_calls_per_trial'])} "
                f"| {_fmt(m['tool_executions_per_trial'])} "
                f"| {_fmt(m['steps_per_trial'])} "
                f"| {_fmt(m['input_tokens_per_trial'], 0)} "
                f"| {_fmt(m['output_tokens_per_trial'], 0)} "
                f"| {_fmt(m['total_tokens_per_trial'], 0)} |"
            )

        lines.append(
            f"| **Global** "
            f"| {g['trials']} "
            f"| {_fmt(g['attempts_per_trial'])} "
            f"| {_fmt(g['retries_per_trial'])} "
            f"| {_fmt(g['llm_calls_per_trial'])} "
            f"| {_fmt(g['tool_executions_per_trial'])} "
            f"| {_fmt(g['steps_per_trial'])} "
            f"| {_fmt(g['input_tokens_per_trial'], 0)} "
            f"| {_fmt(g['output_tokens_per_trial'], 0)} "
            f"| {_fmt(g['total_tokens_per_trial'], 0)} |"
        )
        lines.append("")

        # Tabla 2 — Eficiencia por escenario
        lines.append("### Eficiencia por escenario\n")
        lines.append(
            "*Las métricas por éxito se calculan como el consumo total "
            "de todos los trials dividido por la cantidad de trials exitosos.*\n"
        )
        lines.append(
            "| Escenario | Trials | Successes | Success rate "
            "| Attempts / success | Tokens / success | LLM calls / success "
            "| Tools / success | Steps / success |"
        )
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")

        for scenario, m in by_scenario.items():
            lines.append(
                f"| {scenario} "
                f"| {m['trials']} "
                f"| {m['successful_trials']} "
                f"| {m['success_rate']:.0%} "
                f"| {_fmt(m['attempts_per_success'])} "
                f"| {_fmt(m['total_tokens_per_success'], 0)} "
                f"| {_fmt(m['llm_calls_per_success'])} "
                f"| {_fmt(m['tool_executions_per_success'])} "
                f"| {_fmt(m['steps_per_success'])} |"
            )

        lines.append(
            f"| **Global** "
            f"| {g['trials']} "
            f"| {g['successful_trials']} "
            f"| {g['success_rate']:.0%} "
            f"| {_fmt(g['attempts_per_success'])} "
            f"| {_fmt(g['total_tokens_per_success'], 0)} "
            f"| {_fmt(g['llm_calls_per_success'])} "
            f"| {_fmt(g['tool_executions_per_success'])} "
            f"| {_fmt(g['steps_per_success'])} |"
        )
        lines.append("")

        # Tabla 3 — Consumo LLM por purpose
        lines.append("### Consumo LLM por purpose\n")
        lines.append("*Valores promedio por trial, global.*\n")
        lines.append(
            "| Purpose | LLM calls | Input tokens "
            "| Output tokens | Total tokens |"
        )
        lines.append("|---|---:|---:|---:|---:|")

        total_llm_calls = 0.0
        total_input = 0.0
        total_output = 0.0
        total_tokens = 0.0

        for purpose, pm in g["by_purpose"].items():
            lines.append(
                f"| {purpose} "
                f"| {_fmt(pm['llm_calls_per_trial'])} "
                f"| {_fmt(pm['input_tokens_per_trial'], 0)} "
                f"| {_fmt(pm['output_tokens_per_trial'], 0)} "
                f"| {_fmt(pm['total_tokens_per_trial'], 0)} |"
            )
            total_llm_calls += pm["llm_calls_per_trial"]
            total_input += pm["input_tokens_per_trial"]
            total_output += pm["output_tokens_per_trial"]
            total_tokens += pm["total_tokens_per_trial"]

        lines.append(
            f"| **Total** "
            f"| {_fmt(total_llm_calls)} "
            f"| {_fmt(total_input, 0)} "
            f"| {_fmt(total_output, 0)} "
            f"| {_fmt(total_tokens, 0)} |"
        )
        lines.append("")

        # Tabla 4 — Uso de herramientas por escenario
        lines.append("### Uso de herramientas por escenario\n")
        lines.append("*Executions promedio por trial.*\n")

        all_tools = sorted(
            {
                tool
                for m in by_scenario.values()
                for tool in m["by_tool"]
            }
        )

        header = "| Escenario | " + " | ".join(all_tools) + " | Total |"
        separator = "|---|" + "---:|" * (len(all_tools) + 1)
        lines.append(header)
        lines.append(separator)

        for scenario, m in by_scenario.items():
            tool_counts = [
                _fmt(m["by_tool"].get(tool, 0.0)) for tool in all_tools
            ]
            total = _fmt(m["tool_executions_per_trial"])
            lines.append(
                f"| {scenario} | "
                + " | ".join(tool_counts)
                + f" | {total} |"
            )

        global_tool_counts = [
            _fmt(g["by_tool"].get(tool, 0.0)) for tool in all_tools
        ]
        lines.append(
            f"| **Global** | "
            + " | ".join(global_tool_counts)
            + f" | {_fmt(g['tool_executions_per_trial'])} |"
        )
        lines.append("")

    return "\n".join(lines)

"""Análisis de recuperación entre attempts en M3."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any


def _new_reason_stats() -> dict[str, Any]:
    return {
        "termination_events": 0,
        "trials_with_termination": 0,
        "configured_termination_events": 0,
        "goal_already_achieved_events": 0,
        "recovery_events": 0,
        "recovered_trials": 0,
        "recovered_trials_succeeded": 0,
        "recovered_trials_failed": 0,
        "configured_events_without_recovery": 0,
        "fatal_events": 0,
        "unexpected_recovery_events": 0,
        "trials_with_repeated_reason": 0,
        "events_by_attempt_index": defaultdict(int),
    }


def _new_stats() -> dict[str, Any]:
    return {
        "trials": 0,
        "trials_with_termination": 0,
        "termination_events": 0,
        "configured_termination_events": 0,
        "goal_already_achieved_events": 0,
        "recovery_events": 0,
        "trials_with_recovery": 0,
        "recovered_trials_succeeded": 0,
        "recovered_trials_failed": 0,
        "configured_events_without_recovery": 0,
        "fatal_events": 0,
        "unexpected_recovery_events": 0,
        "trials_with_multiple_termination_events": 0,
        "reasons": defaultdict(_new_reason_stats),
    }


def _termination_reason(
    attempt: dict[str, Any],
) -> str | None:
    """Obtiene la causa estructurada de terminación de un attempt."""

    return next(
        (
            event.get("reason")
            for event in reversed(attempt.get("trace", []))
            if event.get("type") == "run_termination"
        ),
        None,
    )


def _accumulate_trial(
    stats: dict[str, Any],
    trial: dict[str, Any],
    recovery_policy: dict[str, Any],
) -> None:
    """Acumula las terminaciones y recuperaciones de un trial."""

    stats["trials"] += 1

    attempts = trial.get("attempts", [])
    events = []

    for position, attempt in enumerate(attempts):
        reason = _termination_reason(attempt)

        if reason is None:
            continue

        events.append({
            "reason": reason,
            "attempt_index": attempt.get(
                "attempt_index",
                position + 1,
            ),
            "goal_achieved": bool(
                attempt.get("goal_achieved")
            ),
            "has_next_attempt": position + 1 < len(attempts),
            "configured": reason in recovery_policy,
        })

    if not events:
        return

    stats["trials_with_termination"] += 1

    reason_counts = Counter(
        event["reason"]
        for event in events
    )

    if len(events) > 1:
        stats[
            "trials_with_multiple_termination_events"
        ] += 1

    for reason, count in reason_counts.items():
        reason_stats = stats["reasons"][reason]
        reason_stats["trials_with_termination"] += 1

        if count > 1:
            reason_stats[
                "trials_with_repeated_reason"
            ] += 1

    for event in events:
        reason = event["reason"]
        reason_stats = stats["reasons"][reason]

        stats["termination_events"] += 1
        reason_stats["termination_events"] += 1
        reason_stats["events_by_attempt_index"][
            event["attempt_index"]
        ] += 1

        if event["configured"]:
            stats["configured_termination_events"] += 1
            reason_stats[
                "configured_termination_events"
            ] += 1

        if event["goal_achieved"]:
            stats["goal_already_achieved_events"] += 1
            reason_stats[
                "goal_already_achieved_events"
            ] += 1
            continue

        if event["has_next_attempt"]:
            stats["recovery_events"] += 1
            reason_stats["recovery_events"] += 1

            if not event["configured"]:
                stats["unexpected_recovery_events"] += 1
                reason_stats[
                    "unexpected_recovery_events"
                ] += 1

            continue

        if event["configured"]:
            stats[
                "configured_events_without_recovery"
            ] += 1
            reason_stats[
                "configured_events_without_recovery"
            ] += 1
        else:
            stats["fatal_events"] += 1
            reason_stats["fatal_events"] += 1

    recovery_reasons = {
        event["reason"]
        for event in events
        if (
            event["has_next_attempt"]
            and not event["goal_achieved"]
        )
    }

    if not recovery_reasons:
        return

    stats["trials_with_recovery"] += 1

    final_success = bool(trial.get("goal_achieved"))

    if final_success:
        stats["recovered_trials_succeeded"] += 1
    else:
        stats["recovered_trials_failed"] += 1

    for reason in recovery_reasons:
        reason_stats = stats["reasons"][reason]
        reason_stats["recovered_trials"] += 1

        if final_success:
            reason_stats[
                "recovered_trials_succeeded"
            ] += 1
        else:
            reason_stats[
                "recovered_trials_failed"
            ] += 1


def _success_rate(
    successes: int,
    total: int,
) -> float | None:
    if total == 0:
        return None

    return round(successes / total, 4)


def _finalize_reason_stats(
    stats: dict[str, Any],
) -> dict[str, Any]:
    finalized = dict(stats)

    finalized["events_by_attempt_index"] = dict(
        sorted(stats["events_by_attempt_index"].items())
    )
    finalized["recovered_trial_success_rate"] = _success_rate(
        stats["recovered_trials_succeeded"],
        stats["recovered_trials"],
    )

    return finalized


def _finalize_stats(
    stats: dict[str, Any],
) -> dict[str, Any]:
    finalized = dict(stats)

    finalized["recovered_trial_success_rate"] = _success_rate(
        stats["recovered_trials_succeeded"],
        stats["trials_with_recovery"],
    )
    finalized["reasons"] = {
        reason: _finalize_reason_stats(values)
        for reason, values in sorted(
            stats["reasons"].items()
        )
    }

    return finalized


def analyze_attempt_recovery(
    run_sources: list[dict[str, Any]],
) -> dict[str, Any]:
    """Analiza las terminaciones y recuperaciones entre attempts."""

    if not run_sources:
        raise ValueError(
            "run_sources debe contener al menos una fuente de run."
        )

    run_ids = [
        source["run_id"]
        for source in run_sources
    ]

    totals = _new_stats()
    ignored_trials_without_recovery_policy = 0

    conditions: dict[
        tuple[str, str, str],
        dict[str, Any],
    ] = {}
    cases: dict[
        tuple[str, str, str, str],
        dict[str, Any],
    ] = {}

    for source in run_sources:
        manifest = source["manifest"]
        trial_configs = manifest.get(
            "trial_configs",
            {},
        )

        for result in source["result"]["results"]:
            agent_config = result["agent_config"]
            model = result["llm_config"]
            trial_config = result["trial_config"]
            scenario = result["scenario"]

            persisted_trial_config = trial_configs.get(
                trial_config,
                {},
            )
            recovery_policy = persisted_trial_config.get(
                "recoverable_attempt_terminations"
            )

            if not recovery_policy:
                ignored_trials_without_recovery_policy += len(
                    result["trials"]
                )
                continue

            condition_key = (
                agent_config,
                model,
                trial_config,
            )
            condition = conditions.setdefault(
                condition_key,
                _new_stats(),
            )

            case_key = (
                agent_config,
                model,
                trial_config,
                scenario,
            )
            case = cases.setdefault(
                case_key,
                _new_stats(),
            )

            for trial in result["trials"]:
                for stats in (
                    totals,
                    condition,
                    case,
                ):
                    _accumulate_trial(
                        stats,
                        trial,
                        recovery_policy,
                    )

    analysis = {
        "run_ids": run_ids,
        "ignored_trials_without_recovery_policy": (
            ignored_trials_without_recovery_policy
        ),
        "totals": _finalize_stats(totals),
        "conditions": [
            {
                "agent_config": agent_config,
                "llm_config": model,
                "trial_config": trial_config,
                "stats": _finalize_stats(values),
            }
            for (
                agent_config,
                model,
                trial_config,
            ), values in conditions.items()
        ],
        "cases": [
            {
                "agent_config": agent_config,
                "llm_config": model,
                "trial_config": trial_config,
                "scenario": scenario,
                "stats": _finalize_stats(values),
            }
            for (
                agent_config,
                model,
                trial_config,
                scenario,
            ), values in cases.items()
        ],
    }

    if len(run_ids) == 1:
        analysis["run_id"] = run_ids[0]

    return analysis


def _format_rate(value: float | None) -> str:
    if value is None:
        return "n/a"

    return f"{value:.1%}"


def _summary_lines(
    stats: dict[str, Any],
) -> list[str]:
    return [
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Trials analizados | {stats['trials']} |",
        (
            "| Trials con terminación estructurada | "
            f"{stats['trials_with_termination']} |"
        ),
        (
            "| Eventos de terminación | "
            f"{stats['termination_events']} |"
        ),
        (
            "| Eventos configurados como recuperables | "
            f"{stats['configured_termination_events']} |"
        ),
        (
            "| Eventos con goal ya cumplido | "
            f"{stats['goal_already_achieved_events']} |"
        ),
        (
            "| Recuperaciones que abrieron otro attempt | "
            f"{stats['recovery_events']} |"
        ),
        (
            "| Trials con recuperación | "
            f"{stats['trials_with_recovery']} |"
        ),
        (
            "| Trials recuperados con éxito final | "
            f"{stats['recovered_trials_succeeded']} |"
        ),
        (
            "| Trials recuperados con fallo final | "
            f"{stats['recovered_trials_failed']} |"
        ),
        (
            "| Éxito final entre trials recuperados | "
            f"{_format_rate(stats['recovered_trial_success_rate'])} |"
        ),
        (
            "| Eventos recuperables sin siguiente attempt | "
            f"{stats['configured_events_without_recovery']} |"
        ),
        (
            "| Terminaciones fatales no configuradas | "
            f"{stats['fatal_events']} |"
        ),
        (
            "| Recuperaciones inesperadas | "
            f"{stats['unexpected_recovery_events']} |"
        ),
        (
            "| Trials con múltiples terminaciones | "
            f"{stats['trials_with_multiple_termination_events']} |"
        ),
    ]


def _reason_table_lines(
    stats: dict[str, Any],
) -> list[str]:
    lines = [
        (
            "| Causa | Eventos | Trials | Recuperaciones | "
            "Trials recuperados | Éxito final | Fallo final | "
            "Goal ya cumplido | Sin siguiente attempt | Repetición |"
        ),
        (
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"
        ),
    ]

    for reason, values in stats["reasons"].items():
        lines.append(
            f"| `{reason}` "
            f"| {values['termination_events']} "
            f"| {values['trials_with_termination']} "
            f"| {values['recovery_events']} "
            f"| {values['recovered_trials']} "
            f"| {values['recovered_trials_succeeded']} "
            f"| {values['recovered_trials_failed']} "
            f"| {values['goal_already_achieved_events']} "
            f"| {values['configured_events_without_recovery']} "
            f"| {values['trials_with_repeated_reason']} |"
        )

    return lines


def render_markdown(
    analysis: dict[str, Any],
) -> str:
    """Renderiza el análisis de recovery como Markdown."""

    lines = [
        "# Análisis de recuperación entre attempts — M3\n"
    ]

    run_ids = analysis.get("run_ids") or [
        analysis["run_id"]
    ]

    if len(run_ids) == 1:
        lines.append(f"**Run:** `{run_ids[0]}`\n")
    else:
        runs = ", ".join(
            f"`{run_id}`"
            for run_id in run_ids
        )
        lines.append(f"**Runs:** {runs}\n")

    lines.append(
        "Sólo se incluyen condiciones cuyo manifest declara una "
        "política `recoverable_attempt_terminations`.\n"
    )
    lines.append(
        "**Trials ignorados sin política de recovery:** "
        f"{analysis['ignored_trials_without_recovery_policy']}\n"
    )

    lines.append("## Resumen\n")
    lines.extend(_summary_lines(analysis["totals"]))
    lines.append("")

    lines.append("## Por causa\n")
    lines.extend(_reason_table_lines(analysis["totals"]))
    lines.append("")

    lines.append("## Por sistema y configuración de trial\n")
    lines.extend([
        (
            "| Agente | Modelo | Trial config | Trials | "
            "Terminaciones | Recuperaciones | Éxitos | Fallos | "
            "Éxito tras recovery |"
        ),
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ])

    for condition in analysis["conditions"]:
        stats = condition["stats"]
        lines.append(
            f"| `{condition['agent_config']}` "
            f"| `{condition['llm_config']}` "
            f"| `{condition['trial_config']}` "
            f"| {stats['trials']} "
            f"| {stats['termination_events']} "
            f"| {stats['recovery_events']} "
            f"| {stats['recovered_trials_succeeded']} "
            f"| {stats['recovered_trials_failed']} "
            f"| {_format_rate(stats['recovered_trial_success_rate'])} |"
        )

    lines.append("")
    lines.append("## Por caso\n")
    lines.extend([
        (
            "| Agente | Modelo | Trial config | Escenario | "
            "Trials | Terminaciones | Recuperaciones | Éxitos | Fallos |"
        ),
        "|---|---|---|---|---:|---:|---:|---:|---:|",
    ])

    for case in analysis["cases"]:
        stats = case["stats"]
        lines.append(
            f"| `{case['agent_config']}` "
            f"| `{case['llm_config']}` "
            f"| `{case['trial_config']}` "
            f"| `{case['scenario']}` "
            f"| {stats['trials']} "
            f"| {stats['termination_events']} "
            f"| {stats['recovery_events']} "
            f"| {stats['recovered_trials_succeeded']} "
            f"| {stats['recovered_trials_failed']} |"
        )

    return "\n".join(lines)
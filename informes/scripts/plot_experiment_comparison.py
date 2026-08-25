from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter

SCENARIOS = [
    "study-with-key",
    "color-locks",
    "apartment-keys",
    "library-search",
    "office-sequence",
    "extreme-archive",
    "vault-combination",
    "backtracking-vault",
]

SYSTEMS = [
    "baseline",
    "planner",
    "summary",
    "planner_summary",
]

SYSTEM_COLORS = {
    "baseline": "#4C78A8",
    "planner": "#F58518",
    "summary": "#54A24B",
    "planner_summary": "#B279A2",
}

SYSTEM_LABELS = {
    "baseline": "baseline",
    "planner": "planner",
    "summary": "summary",
    "planner_summary": "planner_summary",
}


def _load_run(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _trial_total_tokens(trial: dict[str, Any]) -> int:
    total = 0

    for attempt in trial.get("attempts", []):
        result = attempt.get("agent_result", {})
        total += (result.get("input_tokens") or 0)
        total += (result.get("output_tokens") or 0)

    return total


def _summarize_run(
    run_data: dict[str, Any],
) -> dict[tuple[str, str], dict[str, float]]:
    """Resume métricas por (system, scenario)."""

    summary: dict[tuple[str, str], dict[str, float]] = {}

    for case in run_data["results"]:
        system = case["agent_config"]
        scenario = case["scenario"]
        trials = case.get("trials", [])

        successes = sum(
            1
            for trial in trials
            if trial.get("goal_achieved")
        )
        total_trials = len(trials)
        total_tokens = sum(
            _trial_total_tokens(trial)
            for trial in trials
        )

        summary[(system, scenario)] = {
            "success_rate": (
                successes / total_trials
                if total_trials > 0
                else 0.0
            ),
            "avg_total_tokens_per_trial": (
                total_tokens / total_trials
                if total_trials > 0
                else 0.0
            ),
        }

    return summary


def _panel_values(
    summary: dict[tuple[str, str], dict[str, float]],
    metric_key: str,
    scenario: str | None,
    systems: list[str],
) -> list[float]:
    if scenario is not None:
        return [
            summary[(system, scenario)][metric_key]
            for system in systems
        ]

    return [
        sum(
            summary[(system, scenario_name)][metric_key]
            for scenario_name in SCENARIOS
        )
        / len(SCENARIOS)
        for system in systems
    ]


def _max_metric_value(
    reference_summary: dict[tuple[str, str], dict[str, float]],
    candidate_summary: dict[tuple[str, str], dict[str, float]],
    metric_key: str,
    reference_systems: list[str],
    candidate_systems: list[str],
) -> float:
    max_value = 0.0

    for scenario in SCENARIOS + [None]:
        reference_values = _panel_values(
            reference_summary,
            metric_key,
            scenario,
            reference_systems,
        )
        candidate_values = _panel_values(
            candidate_summary,
            metric_key,
            scenario,
            candidate_systems,
        )
        max_value = max(
            max_value,
            max(reference_values),
            max(candidate_values),
        )

    return max_value


def _apply_common_panel_style(
    ax: plt.Axes,
    title: str,
) -> None:
    ax.set_title(title, fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)


def _plot_grouped_bars(
    ax: plt.Axes,
    baseline_values: list[float],
    recovery_values: list[float],
) -> None:
    bar_width = 0.34
    x_positions = list(range(len(SYSTEMS)))

    for index, system in enumerate(SYSTEMS):
        color = SYSTEM_COLORS[system]

        ax.bar(
            index - bar_width / 2,
            baseline_values[index],
            width=bar_width,
            color=color,
            alpha=0.35,
            edgecolor="black",
            linewidth=0.8,
        )
        ax.bar(
            index + bar_width / 2,
            recovery_values[index],
            width=bar_width,
            color=color,
            alpha=0.95,
            edgecolor="black",
            linewidth=0.8,
            hatch="//",
        )

    baseline_mean = sum(baseline_values) / len(baseline_values)
    recovery_mean = sum(recovery_values) / len(recovery_values)

    ax.axhline(
        baseline_mean,
        color="black",
        linestyle="--",
        linewidth=1.3,
    )
    ax.axhline(
        recovery_mean,
        color="red",
        linestyle="--",
        linewidth=1.3,
    )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(
        [SYSTEM_LABELS[system] for system in SYSTEMS],
        rotation=20,
        ha="right",
    )


def _add_legends(
    fig: plt.Figure,
    reference_label: str,
    candidate_label: str,
) -> None:
    system_handles = [
        Patch(
            facecolor=SYSTEM_COLORS[system],
            edgecolor="black",
            label=SYSTEM_LABELS[system],
        )
        for system in SYSTEMS
    ]

    condition_handles = [
        Patch(
            facecolor="#999999",
            edgecolor="black",
            alpha=0.35,
            label=reference_label,
        ),
        Patch(
            facecolor="#999999",
            edgecolor="black",
            alpha=0.95,
            hatch="//",
            label=candidate_label,
        ),
        Line2D(
            [0],
            [0],
            color="black",
            linestyle="--",
            linewidth=1.3,
            label=f"media {reference_label}",
        ),
        Line2D(
            [0],
            [0],
            color="red",
            linestyle="--",
            linewidth=1.3,
            label=f"media {candidate_label}",
        ),
    ]

    fig.legend(
        handles=system_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.98),
        ncol=4,
        frameon=False,
        title="Sistema",
    )
    fig.legend(
        handles=condition_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.92),
        ncol=4,
        frameon=False,
        title="Condición",
    )


def plot_success_comparison(
    reference_summary: dict[tuple[str, str], dict[str, float]],
    candidate_summary: dict[tuple[str, str], dict[str, float]],
    reference_systems: list[str],
    candidate_systems: list[str],
    reference_label: str,
    candidate_label: str,
    output_path: Path,
) -> None:
    fig, axes = plt.subplots(
        3,
        3,
        figsize=(18, 12),
        sharey=True,
    )
    axes_flat = axes.flatten()

    panel_titles = SCENARIOS + ["Global"]

    for ax, panel_title in zip(axes_flat, panel_titles):
        scenario = None if panel_title == "Global" else panel_title

        baseline_values = _panel_values(
            reference_summary,
            "success_rate",
            scenario,
            reference_systems,
        )
        recovery_values = _panel_values(
            candidate_summary,
            "success_rate",
            scenario,
            candidate_systems,
        )

        _plot_grouped_bars(
            ax,
            baseline_values,
            recovery_values,
        )
        _apply_common_panel_style(ax, panel_title)
        ax.set_ylim(0.0, 1.05)
        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda value, _: f"{value:.0%}")
        )

    for ax in axes[:, 0]:
        ax.set_ylabel("success rate")

    fig.suptitle(
        f"Comparación de success rate: "
        f"{reference_label} vs {candidate_label}",
        fontsize=15,
        y=0.995,
    )
    _add_legends(
        fig,
        reference_label,
        candidate_label,
    )

    plt.subplots_adjust(
        top=0.82,
        bottom=0.08,
        left=0.06,
        right=0.98,
        hspace=0.45,
        wspace=0.22,
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )
    plt.close(fig)


def _tokens_formatter(
    value: float,
    _: int,
) -> str:
    return f"{int(value):,}"


def plot_cost_comparison(
    reference_summary: dict[tuple[str, str], dict[str, float]],
    candidate_summary: dict[tuple[str, str], dict[str, float]],
    reference_systems: list[str],
    candidate_systems: list[str],
    reference_label: str,
    candidate_label: str,
    output_path: Path,
) -> None:
    fig, axes = plt.subplots(
        3,
        3,
        figsize=(18, 12),
        sharey=True,
    )
    axes_flat = axes.flatten()

    max_value = _max_metric_value(
        reference_summary,
        candidate_summary,
        "avg_total_tokens_per_trial",
        reference_systems,
        candidate_systems,
    )
    upper_limit = max_value * 1.12 if max_value > 0 else 1.0

    panel_titles = SCENARIOS + ["Global"]

    for ax, panel_title in zip(axes_flat, panel_titles):
        scenario = None if panel_title == "Global" else panel_title

        baseline_values = _panel_values(
            reference_summary,
            "avg_total_tokens_per_trial",
            scenario,
            reference_systems,
        )
        recovery_values = _panel_values(
            candidate_summary,
            "avg_total_tokens_per_trial",
            scenario,
            candidate_systems,
        )
        _plot_grouped_bars(
            ax,
            baseline_values,
            recovery_values,
        )
        _apply_common_panel_style(ax, panel_title)
        ax.set_ylim(0.0, upper_limit)
        ax.yaxis.set_major_formatter(
            FuncFormatter(_tokens_formatter)
        )

    for ax in axes[:, 0]:
        ax.set_ylabel("tokens promedio por trial")

    fig.suptitle(
        "Comparación de costo: tokens promedio por trial",
        fontsize=15,
        y=0.995,
    )
    _add_legends(
        fig,
        reference_label,
        candidate_label,
    )

    plt.subplots_adjust(
        top=0.82,
        bottom=0.08,
        left=0.06,
        right=0.98,
        hspace=0.45,
        wspace=0.22,
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Genera figuras comparativas entre "
            "dos condiciones experimentales."
        )
    )
    parser.add_argument(
        "--reference-run",
        required=True,
        help="Path al run usado como referencia.",
    )
    parser.add_argument(
        "--candidate-run",
        required=True,
        help="Path al run de la nueva intervención.",
    )
    parser.add_argument(
        "--reference-label",
        required=True,
        help="Etiqueta visible para la condición de referencia.",
    )
    parser.add_argument(
        "--candidate-label",
        required=True,
        help="Etiqueta visible para la nueva condición.",
    )
    parser.add_argument(
        "--reference-systems",
        nargs=len(SYSTEMS),
        default=SYSTEMS,
        metavar="SYSTEM",
        help=(
            "Configs del run de referencia, en el orden "
            "baseline planner summary planner_summary."
        ),
    )
    parser.add_argument(
        "--candidate-systems",
        nargs=len(SYSTEMS),
        default=SYSTEMS,
        metavar="SYSTEM",
        help=(
            "Configs del run candidato homologadas con "
            "baseline planner summary planner_summary."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default="informes/recursos",
        help="Directorio de salida para las figuras.",
    )
    parser.add_argument(
        "--output-prefix",
        required=True,
        help="Prefijo común de los archivos generados.",
    )
    args = parser.parse_args()

    reference_run = _load_run(Path(args.reference_run))
    candidate_run = _load_run(Path(args.candidate_run))

    reference_summary = _summarize_run(reference_run)
    candidate_summary = _summarize_run(candidate_run)

    output_dir = Path(args.output_dir)

    success_path = (
        output_dir
        / f"{args.output_prefix}_success.png"
    )
    cost_path = (
        output_dir
        / f"{args.output_prefix}_cost.png"
    )

    plot_success_comparison(
        reference_summary,
        candidate_summary,
        args.reference_systems,
        args.candidate_systems,
        args.reference_label,
        args.candidate_label,
        success_path,
    )
    plot_cost_comparison(
        reference_summary,
        candidate_summary,
        args.reference_systems,
        args.candidate_systems,
        args.reference_label,
        args.candidate_label,
        cost_path,
    )

    print(f"Figura de success rate: {success_path}")
    print(f"Figura de costo: {cost_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
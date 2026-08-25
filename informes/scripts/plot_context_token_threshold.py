from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
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
]

SYSTEM_COLORS = {
    "baseline": "#4C78A8",
    "planner": "#F58518",
}

REFERENCE_CONTEXT_TOKENS = 16_000


def _load_run(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _percentile(
    values: list[int],
    quantile: float,
) -> float:
    """Percentil con interpolación lineal."""

    if not values:
        raise ValueError("No se puede calcular un percentil sin valores.")

    ordered = sorted(values)
    position = (len(ordered) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)

    if lower == upper:
        return float(ordered[lower])

    fraction = position - lower

    return (
        ordered[lower]
        + fraction * (ordered[upper] - ordered[lower])
    )


def _trial_peak_input_tokens(
    trial: dict[str, Any],
) -> int | None:
    """Máximo input_tokens de llamadas del agente dentro del trial."""

    values: list[int] = []

    for attempt in trial.get("attempts", []):
        for event in attempt.get("trace", []):
            if (
                event.get("type") != "llm_call"
                or event.get("purpose") != "agent"
            ):
                continue

            response = event.get("response")
            if not isinstance(response, dict):
                continue

            input_tokens = response.get("input_tokens")
            if isinstance(input_tokens, int):
                values.append(input_tokens)

    return max(values) if values else None


def _collect_trial_peaks(
    run_data: dict[str, Any],
) -> dict[tuple[str, str], list[int]]:
    peaks: dict[tuple[str, str], list[int]] = {}

    for case in run_data["results"]:
        system = case["agent_config"]
        scenario = case["scenario"]

        if system not in SYSTEMS:
            continue

        case_peaks: list[int] = []

        for trial in case.get("trials", []):
            peak = _trial_peak_input_tokens(trial)

            if peak is not None:
                case_peaks.append(peak)

        peaks.setdefault(
            (system, scenario),
            [],
        ).extend(case_peaks)

    return peaks


def _panel_peaks(
    peaks: dict[tuple[str, str], list[int]],
    system: str,
    scenario: str | None,
) -> list[int]:
    if scenario is not None:
        return peaks.get(
            (system, scenario),
            [],
        )

    return [
        value
        for scenario_name in SCENARIOS
        for value in peaks.get(
            (system, scenario_name),
            [],
        )
    ]


def _tokens_formatter(
    value: float,
    _: int,
) -> str:
    return f"{int(value):,}"


def _threshold_formatter(
    value: float,
    _: int,
) -> str:
    return f"{value / 1000:g}k"


def _apply_panel_style(
    ax: plt.Axes,
    title: str,
) -> None:
    ax.set_title(title, fontsize=11)
    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.35,
    )
    ax.grid(
        axis="x",
        linestyle=":",
        alpha=0.45,
    )
    ax.set_axisbelow(True)


def plot_peak_percentiles(
    peaks: dict[tuple[str, str], list[int]],
    output_path: Path,
) -> None:
    panel_titles = SCENARIOS + ["Global"]
    x_positions = list(range(len(panel_titles)))
    offsets = {
        "baseline": -0.16,
        "planner": 0.16,
    }

    fig, ax = plt.subplots(
        figsize=(16, 7),
    )

    for system in SYSTEMS:
        color = SYSTEM_COLORS[system]

        for index, panel_title in enumerate(panel_titles):
            scenario = (
                None
                if panel_title == "Global"
                else panel_title
            )
            values = _panel_peaks(
                peaks,
                system,
                scenario,
            )

            if not values:
                continue

            p25 = _percentile(values, 0.25)
            p50 = _percentile(values, 0.50)
            p75 = _percentile(values, 0.75)
            p100 = max(values)

            x = index + offsets[system]

            ax.vlines(
                x,
                p25,
                p75,
                color=color,
                linewidth=8,
                alpha=0.30,
            )

            ax.scatter(
                x,
                p25,
                color=color,
                marker="v",
                s=55,
                zorder=3,
            )
            ax.scatter(
                x,
                p50,
                color=color,
                marker="o",
                s=55,
                zorder=3,
            )
            ax.scatter(
                x,
                p75,
                color=color,
                marker="s",
                s=48,
                zorder=3,
            )
            ax.scatter(
                x,
                p100,
                color=color,
                marker="^",
                s=65,
                zorder=3,
            )

    ax.axhline(
        REFERENCE_CONTEXT_TOKENS,
        color="black",
        linestyle="--",
        linewidth=1.1,
        alpha=0.65,
    )

    for boundary in x_positions[:-1]:
        ax.axvline(
            boundary + 0.5,
            color="gray",
            linestyle="-",
            linewidth=1.2,
            alpha=0.75,
            zorder=0,
        )

    ax.set_xticks(
        x_positions,
        panel_titles,
        rotation=20,
        ha="right",
    )
    ax.set_ylabel(
        "máximo input tokens por trial"
    )
    ax.yaxis.set_major_formatter(
        FuncFormatter(_tokens_formatter)
    )
    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.35,
    )
    ax.set_axisbelow(True)

    legend_handles = [
        Line2D(
            [0],
            [0],
            color=SYSTEM_COLORS["baseline"],
            linewidth=5,
            label="baseline",
        ),
        Line2D(
            [0],
            [0],
            color=SYSTEM_COLORS["planner"],
            linewidth=5,
            label="planner",
        ),
        Line2D(
            [0],
            [0],
            marker="v",
            linestyle="none",
            color="gray",
            label="P25",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            linestyle="none",
            color="gray",
            label="P50",
        ),
        Line2D(
            [0],
            [0],
            marker="s",
            linestyle="none",
            color="gray",
            label="P75",
        ),
        Line2D(
            [0],
            [0],
            marker="^",
            linestyle="none",
            color="gray",
            label="P100",
        ),
        Line2D(
            [0],
            [0],
            color="black",
            linestyle="--",
            linewidth=1.1,
            label="referencia ~16k extreme-archive",
        ),
    ]

    ax.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.16),
        ncol=7,
        frameon=False,
    )

    ax.set_title(
        "Distribución del pico de contexto por trial",
        fontsize=15,
        pad=58,
    )

    fig.tight_layout()

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


def _activation_rate(
    values: list[int],
    threshold: int,
) -> float:
    if not values:
        return 0.0

    return (
        100.0
        * sum(
            value > threshold
            for value in values
        )
        / len(values)
    )


def plot_threshold_activation(
    peaks: dict[tuple[str, str], list[int]],
    output_path: Path,
) -> None:
    thresholds = list(
        range(
            4_000,
            20_001,
            500,
        )
    )

    fig, axes = plt.subplots(
        3,
        3,
        figsize=(18, 12),
        sharex=True,
        sharey=True,
    )
    axes_flat = axes.flatten()

    panel_titles = SCENARIOS + ["Global"]

    for ax, panel_title in zip(
        axes_flat,
        panel_titles,
    ):
        scenario = (
            None
            if panel_title == "Global"
            else panel_title
        )

        for system in SYSTEMS:
            values = _panel_peaks(
                peaks,
                system,
                scenario,
            )

            activation = [
                _activation_rate(
                    values,
                    threshold,
                )
                for threshold in thresholds
            ]

            ax.plot(
                thresholds,
                activation,
                linewidth=2.0,
                color=SYSTEM_COLORS[system],
                label=system,
            )

        ax.axvline(
            REFERENCE_CONTEXT_TOKENS,
            color="black",
            linestyle="--",
            linewidth=1.1,
            alpha=0.65,
        )

        _apply_panel_style(
            ax,
            panel_title,
        )
        ax.set_ylim(
            -2,
            102,
        )
        ax.set_xticks(
            [4_000, 8_000, 12_000, 16_000, 20_000]
        )
        ax.xaxis.set_major_formatter(
            FuncFormatter(_threshold_formatter)
        )
        ax.yaxis.set_major_formatter(
            FuncFormatter(
                lambda value, _: f"{value:.0f}%"
            )
        )

    for ax in axes[:, 0]:
        ax.set_ylabel(
            "trials que superarían el threshold\n"
            "al menos una vez"
        )

    for ax in axes[-1, :]:
        ax.set_xlabel(
            "threshold de input tokens"
        )

    legend_handles = [
        Line2D(
            [0],
            [0],
            color=SYSTEM_COLORS[system],
            linewidth=2.0,
            label=system,
        )
        for system in SYSTEMS
    ]
    legend_handles.append(
        Line2D(
            [0],
            [0],
            color="black",
            linestyle="--",
            linewidth=1.1,
            label="referencia ~16k extreme-archive",
        )
    )

    fig.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.94),
        ncol=3,
        frameon=False,
    )

    fig.suptitle(
        "Cobertura potencial del trigger según el threshold de contexto",
        fontsize=15,
        y=0.985,
    )

    plt.subplots_adjust(
        top=0.86,
        bottom=0.07,
        left=0.07,
        right=0.98,
        hspace=0.38,
        wspace=0.20,
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
            "Analiza el pico de input tokens por trial para "
            "fundamentar el trigger de compactación."
        )
    )
    parser.add_argument(
        "--run",
        required=True,
        help=(
            "Run con sistemas sin compactación y "
            "max_history_messages amplio."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default="informes/recursos",
        help="Directorio de salida para las figuras.",
    )
    parser.add_argument(
        "--output-prefix",
        default="m3_context_threshold",
        help="Prefijo común de los archivos generados.",
    )
    args = parser.parse_args()

    run_data = _load_run(
        Path(args.run)
    )
    peaks = _collect_trial_peaks(
        run_data
    )

    for system in SYSTEMS:
        for scenario in SCENARIOS:
            values = peaks.get(
                (system, scenario),
                [],
            )

            if not values:
                raise ValueError(
                    "Faltan trials para "
                    f"{system} / {scenario}."
                )

    output_dir = Path(
        args.output_dir
    )

    plot_peak_percentiles(
        peaks,
        output_dir
        / f"{args.output_prefix}_peak_percentiles.png",
    )
    plot_threshold_activation(
        peaks,
        output_dir
        / f"{args.output_prefix}_activation.png",
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
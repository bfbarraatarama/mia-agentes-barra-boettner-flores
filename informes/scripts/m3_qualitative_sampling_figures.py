#!/usr/bin/env python3
"""Genera figuras para analizar el sampling cualitativo final de M3."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


REPO_ROOT = Path(__file__).resolve().parents[2]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from eval.llm_judge.cases import build_qualitative_case
from eval.llm_judge.presentation import build_case_presentation
from eval.llm_judge.sampling import TrialCandidate, collect_trial_candidates
from eval.persistence import load_run_results


OUTPUT_DIR = REPO_ROOT / "informes" / "recursos"

FINAL_RUN = "m3-final-run-001"

SCENARIOS = [
    ("study-with-key", "easy"),
    ("color-locks", "medium"),
    ("apartment-keys", "medium"),
    ("library-search", "hard"),
    ("office-sequence", "hard"),
    ("extreme-archive", "extreme"),
    ("vault-combination", "extreme"),
    ("backtracking-vault", "extreme"),
]

FINAL_SYSTEMS = [
    "baseline",
    "planner",
    "summary",
    "planner_summary",
]

PERCENTILE_COUNTS = [
    ("P25 (3 casos)", 3),
    ("P50 (5 casos)", 5),
    ("P75 (8 casos)", 8),
    ("P100 (10 casos)", 10),
]

TEXT = "#22262b"
MUTED = "#6b7177"


@dataclass(frozen=True)
class TrialLength:
    candidate: TrialCandidate
    words: int
    success: bool


def save(fig, name: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / name

    fig.savefig(
        path,
        format="svg",
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)

    print(f"escrito: {path.relative_to(REPO_ROOT)}")


def load_trial_lengths() -> list[TrialLength]:
    run_result = load_run_results(FINAL_RUN)
    candidates = collect_trial_candidates({
        FINAL_RUN: run_result,
    })

    trials = []

    for index, candidate in enumerate(candidates, start=1):
        case = build_qualitative_case(
            candidate.trial,
            case_id=f"sampling-{index:03d}",
        )
        presentation = build_case_presentation(case)

        trials.append(TrialLength(
            candidate=candidate,
            words=len(presentation.text.split()),
            success=bool(candidate.trial["goal_achieved"]),
        ))

    return trials


def group_trials(
    trials: list[TrialLength],
) -> dict[tuple[str, str], list[TrialLength]]:
    groups = defaultdict(list)

    for trial in trials:
        key = (
            trial.candidate.agent_config,
            trial.candidate.scenario,
        )
        groups[key].append(trial)

    expected_scenarios = {
        scenario
        for scenario, _ in SCENARIOS
    }

    for system in FINAL_SYSTEMS:
        for scenario in expected_scenarios:
            key = (system, scenario)
            group = groups[key]

            if len(group) != 10:
                raise ValueError(
                    "Se esperaban 10 trials para "
                    f"{system} / {scenario}, pero hay {len(group)}."
                )

            group.sort(
                key=lambda trial: (
                    trial.words,
                    trial.candidate.identity,
                )
            )

    return dict(groups)


def summarize(
    trials: list[TrialLength],
) -> tuple[float, float]:
    if not trials:
        raise ValueError("No se puede resumir un conjunto vacío.")

    success_rate = (
        sum(trial.success for trial in trials)
        / len(trials)
    )
    mean_words = (
        sum(trial.words for trial in trials)
        / len(trials)
    )

    return success_rate, mean_words


def percentile_matrices(
    groups: dict[tuple[str, str], list[TrialLength]],
    count: int,
) -> tuple[list[list[float]], list[list[float]]]:
    success_matrix = []
    words_matrix = []

    for system in FINAL_SYSTEMS:
        system_success = []
        system_words = []
        global_trials = []

        for scenario, _ in SCENARIOS:
            selected = groups[(system, scenario)][:count]
            success_rate, mean_words = summarize(selected)

            system_success.append(success_rate)
            system_words.append(mean_words)
            global_trials.extend(selected)

        global_success, global_words = summarize(global_trials)

        system_success.append(global_success)
        system_words.append(global_words)

        success_matrix.append(system_success)
        words_matrix.append(system_words)

    return success_matrix, words_matrix


def draw_heatmap(
    ax,
    *,
    success_matrix: list[list[float]],
    words_matrix: list[list[float]],
    title: str,
    colormap,
    show_ylabels: bool,
):
    heatmap = ax.imshow(
        success_matrix,
        cmap=colormap,
        vmin=0,
        vmax=1,
        aspect="auto",
    )

    for row, system in enumerate(FINAL_SYSTEMS):
        for column, value in enumerate(success_matrix[row]):
            ax.text(
                column,
                row,
                f"{words_matrix[row][column]:,.0f}".replace(",", "."),
                ha="center",
                va="center",
                fontsize=9,
                color="white" if value >= 0.65 else TEXT,
                fontweight="bold" if value >= 0.65 else "normal",
            )

    labels = [
        f"{scenario} ({difficulty})"
        for scenario, difficulty in SCENARIOS
    ]
    labels.append("Global")

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(
        labels,
        fontsize=7.5,
        rotation=22,
        ha="right",
        rotation_mode="anchor",
    )
    ax.set_yticks(range(len(FINAL_SYSTEMS)))

    if show_ylabels:
        ax.set_yticklabels(FINAL_SYSTEMS, fontsize=9)
    else:
        ax.set_yticklabels([])

    ax.set_xticks(
        [x - 0.5 for x in range(1, len(labels))],
        minor=True,
    )
    ax.set_yticks(
        [y - 0.5 for y in range(1, len(FINAL_SYSTEMS))],
        minor=True,
    )
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", length=0)
    ax.tick_params(colors=MUTED, length=0)

    for side in ax.spines.values():
        side.set_visible(False)

    ax.axvline(
        len(SCENARIOS) - 0.5,
        color="#c8ccd0",
        linewidth=2.5,
    )

    ax.set_title(
        title,
        fontsize=11,
        color=TEXT,
        pad=12,
        loc="left",
    )

    return heatmap


def figure_sampling_percentiles() -> None:
    trials = load_trial_lengths()
    groups = group_trials(trials)

    colormap = LinearSegmentedColormap.from_list(
        "exito",
        ["#f7f3ee", "#f0d9b5", "#8fbf9f", "#2f7f5f"],
    )

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(16, 8.5),
    )

    heatmap = None

    for index, (ax, (title, count)) in enumerate(
        zip(axes.flat, PERCENTILE_COUNTS)
    ):
        success_matrix, words_matrix = percentile_matrices(
            groups,
            count,
        )

        heatmap = draw_heatmap(
            ax,
            success_matrix=success_matrix,
            words_matrix=words_matrix,
            title=title,
            colormap=colormap,
            show_ylabels=(index % 2 == 0),
        )

    fig.suptitle(
        "Tasa de éxito según longitud de la trayectoria",
        fontsize=13,
        color=TEXT,
        x=0.08,
        ha="left",
    )
    fig.text(
        0.08,
        0.945,
        (
            "Color: success rate · texto: promedio de palabras · "
            "subconjuntos acumulados por longitud dentro de cada "
            "sistema y escenario"
        ),
        fontsize=8.5,
        color=MUTED,
    )

    fig.subplots_adjust(
        left=0.08,
        right=0.90,
        top=0.88,
        bottom=0.11,
        hspace=0.48,
        wspace=0.14,
    )

    colorbar_ax = fig.add_axes([0.915, 0.16, 0.012, 0.68])
    colorbar = fig.colorbar(
        heatmap,
        cax=colorbar_ax,
    )
    colorbar.set_label(
        "Success rate",
        color=TEXT,
        fontsize=9,
    )
    colorbar.ax.tick_params(
        colors=MUTED,
        labelsize=8.5,
    )

    save(
        fig,
        "m3_qualitative_sampling_percentiles.svg",
    )


def main() -> int:
    figure_sampling_percentiles()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
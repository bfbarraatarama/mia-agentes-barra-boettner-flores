#!/usr/bin/env python3
"""Genera las figuras del informe M3 a partir de la evidencia persistida.

Las figuras son artefactos derivados: se regeneran enteras desde los
`results.json` de las evaluaciones, sin volver a ejecutar los modelos.

    python scripts/informe_m3_figures.py

Salida: informes/recursos/m3_*.svg
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


REPO_ROOT = Path(__file__).resolve().parents[1]
EVALUATIONS = REPO_ROOT / "eval" / "results" / "evaluations"
HISTORIC = REPO_ROOT / "eval" / "results" / "historic" / "evaluations"
OUTPUT_DIR = REPO_ROOT / "informes" / "recursos"

FINAL_EVAL = "m3-final-eval-001"
MODELS_EVAL = "m3-three-model-repair-comparison-eval-003"
CONTEXT_EVAL = "m3-context-comparison-eval-008"

RANKING_SOURCES = [
    ("m3-final-eval-002", "baseline", "multi_attempt"),
    ("m3-final-eval-002", "planner", "multi_attempt"),
    ("m3-final-eval-002", "summary", "multi_attempt"),
    ("m3-final-eval-002", "planner_summary", "multi_attempt"),
    ("m3-final-eval-002", "baseline", "multi_attempt_recovery"),
    ("m3-final-eval-002", "planner", "multi_attempt_recovery"),
    ("m3-final-eval-002", "summary", "multi_attempt_recovery"),
    ("m3-final-eval-002", "planner_summary", "multi_attempt_recovery"),
    (
        "m3-final-eval-003",
        "baseline_incremental",
        "multi_attempt_recovery",
    ),
    (
        "m3-final-eval-003",
        "planner_incremental",
        "multi_attempt_recovery",
    ),
    (
        "m3-final-eval-003",
        "summary_incremental",
        "multi_attempt_recovery",
    ),
    (
        "m3-final-eval-003",
        "planner_summary_incremental",
        "multi_attempt_recovery",
    ),
    (
        "m3-final-eval-006",
        "summary_token_trigger",
        "multi_attempt_recovery",
    ),
    (
        "m3-final-eval-006",
        "planner_summary_token_trigger",
        "multi_attempt_recovery",
    ),
    (
        "m3-final-eval-007",
        "summary_strategic",
        "multi_attempt_recovery",
    ),
    (
        "m3-final-eval-007",
        "planner_summary_strategic",
        "multi_attempt_recovery",
    ),
]

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

SYSTEM_COLORS = {
    "baseline": "#2f6f9f",
    "planner": "#3f8f6f",
    "summary": "#d1863a",
    "planner_summary": "#9a5f96",
}

OUTCOME_COLORS = {
    "éxito": "#3f8f6f",
    "max_iterations": "#e0a23c",
    "context_overflow": "#c1543f",
    "gave_up_early": "#9aa0a6",
}

TEXT = "#22262b"
MUTED = "#6b7177"


def load_evaluation(eval_id: str, *, historic: bool = False) -> dict:
    base = HISTORIC if historic else EVALUATIONS
    path = base / eval_id / "results.json"

    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def success_by_system_and_scenario(
    evaluation: dict,
    *,
    key: str = "agent_config",
) -> dict[tuple[str, str], float]:
    return {
        (case[key], case["scenario"]): case["metrics"]["success_rate"]
        for case in evaluation["results"]
    }


def style_axes(ax) -> None:
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    for side in ("left", "bottom"):
        ax.spines[side].set_color("#c8ccd0")

    ax.tick_params(colors=MUTED, labelsize=9, length=3)
    ax.set_axisbelow(True)


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


def figure_success_heatmap() -> None:
    """Éxito por sistema y escenario, run final."""

    evaluation = load_evaluation(FINAL_EVAL)
    rates = success_by_system_and_scenario(evaluation)

    colormap = LinearSegmentedColormap.from_list(
        "exito",
        ["#f7f3ee", "#f0d9b5", "#8fbf9f", "#2f7f5f"],
    )

    fig, ax = plt.subplots(figsize=(10, 3.9))

    matrix = [
        [rates[(system, scenario)] for scenario, _ in SCENARIOS]
        for system in FINAL_SYSTEMS
    ]

    ax.imshow(matrix, cmap=colormap, vmin=0, vmax=1, aspect="auto")

    for row, system in enumerate(FINAL_SYSTEMS):
        for column, (scenario, _) in enumerate(SCENARIOS):
            value = rates[(system, scenario)]

            ax.text(
                column,
                row,
                f"{value:.0%}",
                ha="center",
                va="center",
                fontsize=10,
                color="white" if value >= 0.65 else TEXT,
                fontweight="bold" if value >= 0.65 else "normal",
            )

    ax.set_xticks(range(len(SCENARIOS)))
    ax.set_xticklabels(
        [
            f"{scenario} ({difficulty})"
            for scenario, difficulty in SCENARIOS
        ],
        fontsize=8.5,
        rotation=22,
        ha="right",
        rotation_mode="anchor",
    )
    ax.set_yticks(range(len(FINAL_SYSTEMS)))
    ax.set_yticklabels(FINAL_SYSTEMS, fontsize=10)

    ax.set_xticks(
        [x - 0.5 for x in range(1, len(SCENARIOS))],
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

    ax.set_title(
        "Tasa de éxito por sistema y escenario",
        fontsize=12,
        color=TEXT,
        pad=30,
        loc="left",
    )
    ax.text(
        0,
        1.07,
        "nova-lite · multi_attempt · 10 trials por celda · run m3-final-run-001",
        transform=ax.transAxes,
        fontsize=8.5,
        color=MUTED,
    )

    save(fig, "m3_success_heatmap.svg")


def figure_outcomes_by_system() -> None:
    """Composición de los 80 trials de cada sistema, run final."""

    evaluation = load_evaluation(FINAL_EVAL)
    by_system = evaluation["analyses"]["error_analysis"]["failures_by_system"]

    modes = ["max_iterations", "context_overflow", "gave_up_early"]

    fig, ax = plt.subplots(figsize=(9.5, 3.2))

    positions = list(range(len(FINAL_SYSTEMS)))[::-1]

    for position, system in zip(positions, FINAL_SYSTEMS):
        failures = by_system[system]["nova-lite"]
        total = 80
        successes = total - sum(failures.values())

        segments = [("éxito", successes)] + [
            (mode, failures.get(mode, 0)) for mode in modes
        ]

        left = 0

        for label, value in segments:
            if value == 0:
                continue

            ax.barh(
                position,
                value,
                left=left,
                height=0.62,
                color=OUTCOME_COLORS[label],
                edgecolor="white",
                linewidth=1.2,
            )

            if value >= 5:
                ax.text(
                    left + value / 2,
                    position,
                    str(value),
                    ha="center",
                    va="center",
                    fontsize=9.5,
                    color="white",
                    fontweight="bold",
                )

            left += value

        ax.text(
            81.5,
            position,
            f"{successes / total:.0%}",
            ha="left",
            va="center",
            fontsize=10,
            color=TEXT,
            fontweight="bold",
        )

    ax.set_yticks(positions)
    ax.set_yticklabels(FINAL_SYSTEMS, fontsize=10)
    ax.set_xlim(0, 88)
    ax.set_xticks([0, 20, 40, 60, 80])
    ax.set_xlabel("trials (80 por sistema)", fontsize=9, color=MUTED)

    style_axes(ax)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x", color="#e6e8ea", linewidth=0.8)

    handles = [
        plt.Rectangle((0, 0), 1, 1, color=color)
        for color in OUTCOME_COLORS.values()
    ]
    ax.legend(
        handles,
        list(OUTCOME_COLORS),
        loc="upper center",
        bbox_to_anchor=(0.5, -0.28),
        ncol=4,
        frameon=False,
        fontsize=9,
        labelcolor=MUTED,
    )

    ax.set_title(
        "Composición de los trials: éxito y modo de fallo",
        fontsize=12,
        color=TEXT,
        pad=12,
        loc="left",
    )

    save(fig, "m3_outcomes_by_system.svg")


def figure_cost_vs_success() -> None:
    """Costo efectivo por éxito frente a tasa de éxito, run final."""

    evaluation = load_evaluation(FINAL_EVAL)
    systems = evaluation["analyses"]["efficiency_analysis"]["systems"]

    fig, ax = plt.subplots(figsize=(7.2, 4.4))

    points = {}

    for payload in systems.values():
        name = payload["agent_config"]
        totals = payload["global"]
        points[name] = (
            totals["total_tokens_per_success"] / 1000,
            totals["success_rate"],
            totals["total_tokens_per_trial"] / 1000,
        )

    label_offsets = {
        "baseline": (0, 26),
        "planner": (0, 26),
        "summary": (0, -40),
        "planner_summary": (0, 26),
    }

    for name, (tokens_per_success, rate, tokens_per_trial) in points.items():
        ax.scatter(
            tokens_per_success,
            rate,
            s=tokens_per_trial * 3.2,
            color=SYSTEM_COLORS[name],
            alpha=0.8,
            edgecolor="white",
            linewidth=1.5,
            zorder=3,
        )
        ax.annotate(
            f"{name}\n{tokens_per_success:.0f}k / éxito · "
            f"{tokens_per_trial:.0f}k / trial",
            (tokens_per_success, rate),
            textcoords="offset points",
            xytext=label_offsets[name],
            ha="center",
            va="center",
            fontsize=8.8,
            color=TEXT,
            linespacing=1.5,
        )

    ax.set_xlabel(
        "tokens por éxito (miles) — menos es mejor",
        fontsize=9.5,
        color=MUTED,
    )
    ax.set_ylabel("tasa de éxito", fontsize=9.5, color=MUTED)
    ax.set_ylim(0.18, 0.92)
    ax.set_xlim(126, 180)
    ax.set_yticks([0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    ax.set_yticklabels(["30%", "40%", "50%", "60%", "70%", "80%"])

    style_axes(ax)
    ax.grid(color="#eceef0", linewidth=0.8)

    ax.set_title(
        "Costo efectivo por éxito",
        fontsize=12,
        color=TEXT,
        pad=30,
        loc="left",
    )
    ax.text(
        0,
        1.06,
        "el área del círculo es el consumo por trial · esquina superior "
        "izquierda = mejor",
        transform=ax.transAxes,
        fontsize=8.5,
        color=MUTED,
    )

    save(fig, "m3_cost_vs_success.svg")


def figure_experiments() -> None:
    """Comparación de modelos y de estrategias de contexto."""

    models_evaluation = load_evaluation(MODELS_EVAL, historic=True)
    context_evaluation = load_evaluation(CONTEXT_EVAL, historic=True)

    fig, (left_axes, right_axes) = plt.subplots(
        1,
        2,
        figsize=(12, 4),
        gridspec_kw={"width_ratios": [1, 1.25], "wspace": 0.28},
    )

    # --- Panel A: modelos ---
    model_rates: dict[str, list[float]] = {}

    for case in models_evaluation["results"]:
        if case["agent_config"] != "minimal":
            continue

        model_rates.setdefault(case["llm_config"], []).append(
            case["metrics"]["success_rate"]
        )

    models = ["llama3.1", "qwen2.5:7b", "nova-lite"]
    values = [
        sum(model_rates[model]) / len(model_rates[model]) for model in models
    ]

    bars = left_axes.bar(
        models,
        values,
        width=0.55,
        color=["#c1543f", "#e0a23c", "#2f6f9f"],
        edgecolor="white",
        linewidth=1.2,
    )

    for bar, value in zip(bars, values):
        left_axes.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.025,
            f"{value:.0%}",
            ha="center",
            fontsize=10.5,
            color=TEXT,
            fontweight="bold",
        )

    left_axes.set_ylim(0, 1)
    left_axes.set_yticks([0, 0.25, 0.5, 0.75, 1])
    left_axes.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
    left_axes.set_title(
        "A · El modelo domina el resultado",
        fontsize=11,
        color=TEXT,
        pad=26,
        loc="left",
    )
    left_axes.text(
        0,
        1.045,
        "agente idéntico · single_attempt · 80 trials por modelo",
        transform=left_axes.transAxes,
        fontsize=8.5,
        color=MUTED,
    )

    style_axes(left_axes)
    left_axes.grid(axis="y", color="#eceef0", linewidth=0.8)

    # --- Panel B: estrategias de contexto ---
    context_systems = [
        ("minimal", "sin compactar\n(ventana 100)", "#9aa0a6", 0),
        ("minimal_history_200", "sin compactar\n(ventana 200)", "#2f6f9f", 0),
        ("minimal_compaction", "determinística\n(ventana 100)", "#3f8f6f", 8),
        ("minimal_summary", "resumen LLM\n(ventana 100)", "#d1863a", 13),
    ]

    context_rates: dict[str, list[float]] = {}

    for case in context_evaluation["results"]:
        context_rates.setdefault(case["agent_config"], []).append(
            case["metrics"]["success_rate"]
        )

    labels = []
    values = []
    colors = []
    activations = []

    for system, label, color, activation in context_systems:
        rates = context_rates[system]
        labels.append(f"{label}\n{activation} compactaciones")
        values.append(sum(rates) / len(rates))
        colors.append(color)
        activations.append(activation)

    bars = right_axes.bar(
        labels,
        values,
        width=0.6,
        color=colors,
        edgecolor="white",
        linewidth=1.2,
    )

    for bar, value in zip(bars, values):
        right_axes.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.025,
            f"{value:.0%}",
            ha="center",
            fontsize=10.5,
            color=TEXT,
            fontweight="bold",
        )

    right_axes.set_ylim(0, 1)
    right_axes.set_yticks([0, 0.25, 0.5, 0.75, 1])
    right_axes.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
    right_axes.set_title(
        "B · A ventana 100 el compactor casi no se dispara",
        fontsize=11,
        color=TEXT,
        pad=26,
        loc="left",
    )
    right_axes.text(
        0,
        1.045,
        "nova-lite · multi_attempt · 80 trials por sistema",
        transform=right_axes.transAxes,
        fontsize=8.5,
        color=MUTED,
    )

    style_axes(right_axes)
    right_axes.tick_params(axis="x", labelsize=8)
    right_axes.grid(axis="y", color="#eceef0", linewidth=0.8)

    save(fig, "m3_experiments.svg")


def _aggregate_system_success(
    evaluation: dict,
    *,
    agent_config: str,
    trial_config: str,
) -> tuple[int, int]:
    """Agrega success sobre los escenarios de una condición."""

    cases = [
        case
        for case in evaluation["results"]
        if (
            case["agent_config"] == agent_config
            and case["llm_config"] == "nova-lite"
            and case["trial_config"] == trial_config
        )
    ]

    if not cases:
        raise ValueError(
            "No se encontró la condición del ranking: "
            f"{agent_config} / nova-lite / {trial_config}."
        )

    total_trials = sum(
        case["trial_count"]
        for case in cases
    )
    successful_trials = round(sum(
        case["trial_count"]
        * case["metrics"]["success_rate"]
        for case in cases
    ))

    return successful_trials, total_trials


def figure_system_ranking() -> None:
    """Top 5 de sistemas observados en la línea experimental final."""

    evaluations = {
        eval_id: load_evaluation(eval_id)
        for eval_id, _, _ in RANKING_SOURCES
    }

    ranking = []

    for eval_id, agent_config, trial_config in RANKING_SOURCES:
        successes, trials = _aggregate_system_success(
            evaluations[eval_id],
            agent_config=agent_config,
            trial_config=trial_config,
        )
        has_recovery = (
            trial_config == "multi_attempt_recovery"
        )
        label = agent_config.replace("_", " ")

        if has_recovery:
            label = f"{label} + recovery"

        ranking.append({
            "label": label,
            "successes": successes,
            "trials": trials,
            "success_rate": successes / trials,
            "has_recovery": has_recovery,
        })

    top_five = sorted(
        ranking,
        key=lambda item: (
            item["success_rate"],
            item["label"],
        ),
    )[-5:]

    fig, ax = plt.subplots(figsize=(10.5, 4.8))

    positions = list(range(len(top_five)))
    colors = [
        "#3f8f6f"
        if item["has_recovery"]
        else "#9aa0a6"
        for item in top_five
    ]

    bars = ax.barh(
        positions,
        [
            item["success_rate"]
            for item in top_five
        ],
        height=0.62,
        color=colors,
        edgecolor="white",
        linewidth=1.2,
    )

    for bar, item in zip(bars, top_five):
        ax.text(
            item["success_rate"] + 0.012,
            bar.get_y() + bar.get_height() / 2,
            (
                f"{item['successes']}/{item['trials']} · "
                f"{item['success_rate']:.1%}"
            ),
            ha="left",
            va="center",
            fontsize=9.5,
            color=TEXT,
            fontweight="bold",
        )

    ax.set_yticks(positions)
    ax.set_yticklabels(
        [
            item["label"]
            for item in top_five
        ],
        fontsize=9.5,
    )
    ax.set_xlim(0, 0.9)
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8])
    ax.set_xticklabels(["0%", "20%", "40%", "60%", "80%"])
    ax.set_xlabel("tasa de éxito", fontsize=9.5, color=MUTED)

    style_axes(ax)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x", color="#eceef0", linewidth=0.8)

    handles = [
        plt.Rectangle((0, 0), 1, 1, color="#3f8f6f"),
        plt.Rectangle((0, 0), 1, 1, color="#9aa0a6"),
    ]
    ax.legend(
        handles,
        ["con recovery", "sin recovery"],
        loc="upper right",
        bbox_to_anchor=(1.0, 1.08),
        ncol=2,
        frameon=False,
        fontsize=9,
        labelcolor=MUTED,
    )

    ax.set_title(
        "Cinco mejores sistemas observados",
        fontsize=12,
        color=TEXT,
        pad=28,
        loc="left",
    )
    ax.text(
        0,
        1.04,
        "línea experimental final · nova-lite · 80 trials por sistema",
        transform=ax.transAxes,
        fontsize=8.5,
        color=MUTED,
    )

    save(fig, "m3_system_ranking.svg")


def main() -> int:
    figure_success_heatmap()
    figure_outcomes_by_system()
    figure_cost_vs_success()
    figure_experiments()
    figure_system_ranking()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

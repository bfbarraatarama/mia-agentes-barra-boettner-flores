"""Presentación y persistencia de resultados de evaluación para M3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def save_evaluation_result(
    evaluation_result: dict[str, Any],
    output_path: Path,
) -> None:
    """Guarda el resultado completo de una evaluación en JSON."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(
            evaluation_result,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def print_success_rate_summary(
    evaluation_result: dict[str, Any],
) -> None:
    """Muestra el success rate por sistema y escenario."""

    print("Success rate por sistema y escenario:")

    for result in evaluation_result["results"]:
        agent_config = result["agent_config"]
        llm_config = result["llm_config"]
        scenario = result["scenario"]
        success_rate = result["metrics"]["success_rate"]

        print(
            f"- {agent_config} / {llm_config} / "
            f"{scenario}: {success_rate:.3f}"
        )


def plot_success_rate(
    evaluation_result: dict[str, Any],
    output_path: Path,
) -> None:
    """Grafica el success rate por sistema y escenario."""

    results = evaluation_result["results"]

    systems = []
    scenarios = []

    for result in results:
        system = (
            result["agent_config"],
            result["llm_config"],
        )

        if system not in systems:
            systems.append(system)

        if result["scenario"] not in scenarios:
            scenarios.append(result["scenario"])

    rates = {
        (
            (result["agent_config"], result["llm_config"]),
            result["scenario"],
        ): result["metrics"]["success_rate"]
        for result in results
    }

    x_positions = list(range(len(scenarios)))
    bar_width = 0.8 / len(systems)

    fig, ax = plt.subplots(figsize=(12, 6))

    for system_index, system in enumerate(systems):
        positions = [
            x
            - 0.4
            + bar_width / 2
            + system_index * bar_width
            for x in x_positions
        ]

        values = [
            rates[(system, scenario)]
            for scenario in scenarios
        ]

        label = f"{system[0]} / {system[1]}"

        ax.bar(
            positions,
            values,
            width=bar_width,
            label=label,
        )

    ax.set_xlabel("Escenario")
    ax.set_ylabel("Success rate")
    ax.set_title("Success rate por escenario")
    ax.set_ylim(0.0, 1.0)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(
        scenarios,
        rotation=30,
        ha="right",
    )
    ax.legend(title="Sistema")

    fig.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)

    plt.close(fig)
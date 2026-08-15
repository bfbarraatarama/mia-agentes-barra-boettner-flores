"""Ejecución de evaluaciones para M3."""

from __future__ import annotations
from collections.abc import Callable

from typing import Any

from eval.experiment import run_experiment
from eval.metrics import METRICS


def run_evaluation(
    config: dict[str, Any],
    progress_callback: Callable[
        [int, int, str, str, str, int, int, bool],
        None,
    ] | None = None,
) -> dict[str, Any]:
    """Ejecuta una configuración de evaluación y calcula sus métricas."""

    results = []
    completed_runs = 0
    total_runs = (
        len(config["systems"])
        * len(config["scenarios"])
        * config["runs_per_case"]
    )

    for system in config["systems"]:
        for scenario_spec in config["scenarios"]:
            def on_run_complete(
                run_index: int,
                runs_count: int,
                achieved: bool,
            ) -> None:
                nonlocal completed_runs

                completed_runs += 1

                if progress_callback is not None:
                    progress_callback(
                        completed_runs,
                        total_runs,
                        system["agent_config"],
                        system["llm_config"],
                        scenario_spec,
                        run_index,
                        runs_count,
                        achieved,
                    )

            experiment = run_experiment(
                scenario_spec=scenario_spec,
                agent_config_name=system["agent_config"],
                llm_config_name=system["llm_config"],
                runs_count=config["runs_per_case"],
                progress_callback=on_run_complete,
            )

            metric_results = {
                metric_name: METRICS[metric_name](experiment["runs"])
                for metric_name in config["metrics"]
            }

            evaluated_experiment = dict(experiment)
            evaluated_experiment["metrics"] = metric_results

            results.append(evaluated_experiment)

    return {
        "evaluation_config": config,
        "results": results,
    }
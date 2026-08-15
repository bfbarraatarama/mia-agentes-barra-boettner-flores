"""Ejecución de evaluaciones para M3."""

from __future__ import annotations
from collections.abc import Callable

from typing import Any

from eval.experiment import run_experiment
from eval.experiment_configs import EXPERIMENT_CONFIGS
from eval.metrics import METRICS


def run_evaluation(
    config: dict[str, Any],
    progress_callback: Callable[
        [int, int, str, str, str, str, int, int, bool],
        None,
    ] | None = None,
) -> dict[str, Any]:
    """Ejecuta una configuración de evaluación y calcula sus métricas."""

    results = []
    completed_trials = 0
    total_trials = (
        len(config["systems"])
        * len(config["experiment_configs"])
        * len(config["scenarios"])
        * config["trials_per_case"]
    )

    for system in config["systems"]:
        for experiment_config_name in config["experiment_configs"]:
            for scenario_spec in config["scenarios"]:
                def on_trial_complete(
                    trial_index: int,
                    trials_count: int,
                    achieved: bool,
                ) -> None:
                    nonlocal completed_trials

                    completed_trials += 1

                    if progress_callback is not None:
                        progress_callback(
                            completed_trials,
                            total_trials,
                            system["agent_config"],
                            system["llm_config"],
                            experiment_config_name,
                            scenario_spec,
                            trial_index,
                            trials_count,
                            achieved,
                        )

                experiment = run_experiment(
                    scenario_spec=scenario_spec,
                    agent_config_name=system["agent_config"],
                    llm_config_name=system["llm_config"],
                    experiment_config=EXPERIMENT_CONFIGS[
                        experiment_config_name
                    ],
                    trials_count=config["trials_per_case"],
                    progress_callback=on_trial_complete,
                )

                metric_results = {
                    metric_name: METRICS[metric_name](
                        experiment["trials"]
                    )
                    for metric_name in config["metrics"]
                }

                evaluated_experiment = dict(experiment)
                evaluated_experiment[
                    "experiment_config_name"
                ] = experiment_config_name
                evaluated_experiment["metrics"] = metric_results

                results.append(evaluated_experiment)

    return {
        "evaluation_config": config,
        "results": results,
    }
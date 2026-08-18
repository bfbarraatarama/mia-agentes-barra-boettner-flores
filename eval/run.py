"""Evaluación reproducible de M3."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Permite ejecutar exactamente:
#     python eval/run.py
REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from eval.evaluation import start_evaluation
from eval.evaluation_configs import M3_EVALUATION_CONFIG
from eval.persistence import EVALUATIONS_DIR, RUNS_DIR
from eval.run_configs import M3_BASELINE_RUN_CONFIG, M3_TOOL_REPAIR_COMPARISON_RUN_CONFIG
from eval.run_execution import resume_run, start_run
from eval.report import (
    plot_success_rate,
    print_success_rate_summary,
    write_error_analysis_report,
)


RUN_ID = "m3-tool-repair-comparison-run-001"
EVAL_ID = "m3-tool-repair-comparison-eval-001"

RUN_CONFIG = M3_TOOL_REPAIR_COMPARISON_RUN_CONFIG
EVALUATION_CONFIG = M3_EVALUATION_CONFIG


def print_progress(
    completed_trials: int,
    total_trials: int,
    case: dict[str, str],
    trial: dict[str, Any],
) -> None:
    """Muestra el progreso de la corrida."""

    percentage = 100 * completed_trials / total_trials
    status = "SUCCESS" if trial["goal_achieved"] else "FAIL"

    print(
        f"[{completed_trials}/{total_trials} | {percentage:5.1f}%] "
        f"[{status}] "
        f"{case['agent_config']} / {case['llm_config']} / "
        f"{case['trial_config']} / {case['scenario']} "
        f"(trial {trial['trial_index']})",
        flush=True,
    )


def main() -> int:
    # Para crear una corrida nueva:
    #
    start_run(
        run_id=RUN_ID,
        run_config=RUN_CONFIG,
        progress_callback=print_progress,
    )
    #
    # Para reanudar una corrida interrumpida:
    #
    # resume_run(
    #     run_id=RUN_ID,
    #     progress_callback=print_progress,
    # )
    #
    # Si el run ya existe y está completo, no ejecutar ninguna de
    # las dos funciones anteriores y evaluar directamente.

    evaluation_result = start_evaluation(
        eval_id=EVAL_ID,
        run_id=RUN_ID,
        evaluation_config=EVALUATION_CONFIG,
    )

    success_rate_plot_path = (
        EVALUATIONS_DIR / f"{EVAL_ID}.success_rate.png"
    )

    error_analysis_path = (
        EVALUATIONS_DIR / f"{EVAL_ID}.error_analysis.md"
    )

    print_success_rate_summary(
        evaluation_result
    )
    plot_success_rate(
        evaluation_result,
        success_rate_plot_path,
    )

    write_error_analysis_report(
        evaluation_result,
        error_analysis_path,
    )

    print()
    print(
        "Manifest del run: "
        f"{RUNS_DIR / f'{RUN_ID}.manifest.json'}"
    )
    print(
        "Resultados del run: "
        f"{RUNS_DIR / f'{RUN_ID}.json'}"
    )
    print(
        "Manifest de la evaluación: "
        f"{EVALUATIONS_DIR / f'{EVAL_ID}.manifest.json'}"
    )
    print(
        "Resultados de la evaluación: "
        f"{EVALUATIONS_DIR / f'{EVAL_ID}.json'}"
    )
    print(
        f"Gráfico de success rate: {success_rate_plot_path}"
    )
    print(
        f"Análisis de errores: {error_analysis_path}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
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
from eval.persistence import RUNS_DIR, evaluation_dir
from eval.configs.evaluation_configs import M3_EVALUATION_CONFIG
from eval.configs.run_configs import (
    M3_PLANNER_RUN_CONFIG,
)
from eval.run_execution import resume_run, start_run
from eval.report import (
    plot_success_rate,
    print_success_rate_summary,
    write_error_analysis_report,
)
from eval.analyses.tool_call_repair_analysis import (
    render_markdown as render_tool_call_repair_markdown,
)

RUN_ID = "m3-planner-run-001"
EVALUATION_RUN_IDS = [
    "m3-nova-tool-repair-comparison-run-003",
    RUN_ID,
]
EVAL_ID = "m3-planner-comparison-eval-001"

RUN_CONFIG = M3_PLANNER_RUN_CONFIG
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
    run_manifest_path = (
        RUNS_DIR / f"{RUN_ID}.manifest.json"
    )
    run_results_path = (
        RUNS_DIR / f"{RUN_ID}.json"
    )

    if (
        not run_manifest_path.exists()
        and not run_results_path.exists()
    ):
        start_run(
            run_id=RUN_ID,
            run_config=RUN_CONFIG,
            progress_callback=print_progress,
        )
    else:
        resume_run(
            run_id=RUN_ID,
            progress_callback=print_progress,
        )


    evaluation_result = start_evaluation(
        eval_id=EVAL_ID,
        run_ids=EVALUATION_RUN_IDS,
        evaluation_config=EVALUATION_CONFIG,
    )

    evaluation_output_dir = evaluation_dir(EVAL_ID)

    success_rate_plot_path = (
        evaluation_output_dir / "success_rate.png"
    )

    error_analysis_path = (
        evaluation_output_dir / "error_analysis.md"
    )

    tool_call_repair_analysis_path = (
        evaluation_output_dir
        / "tool_call_repair_analysis.md"
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

    tool_call_repair_analysis = (
        evaluation_result["analyses"][
            "tool_call_repair_analysis"
        ]
    )

    tool_call_repair_analysis_path.write_text(
        render_tool_call_repair_markdown(
            tool_call_repair_analysis
        ),
        encoding="utf-8",
    )

    print()

    for run_id in EVALUATION_RUN_IDS:
        print(
            "Manifest del run: "
            f"{RUNS_DIR / f'{run_id}.manifest.json'}"
        )
        print(
            "Resultados del run: "
            f"{RUNS_DIR / f'{run_id}.json'}"
        )
    print(
        "Manifest de la evaluación: "
        f"{evaluation_output_dir / 'manifest.json'}"
    )
    print(
        "Resultados de la evaluación: "
        f"{evaluation_output_dir / 'results.json'}"
    )
    print(
        f"Gráfico de success rate: {success_rate_plot_path}"
    )
    print(
        f"Análisis de errores: {error_analysis_path}"
    )
    print(
        "Análisis de reparación de tool calls: "
        f"{tool_call_repair_analysis_path}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
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
    M3_FINAL_INCREMENTAL_RUN_CONFIG,
    M3_FINAL_RECOVERY_RUN_CONFIG,
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
from eval.analyses.attempt_recovery_analysis import (
    render_markdown as render_attempt_recovery_markdown,
)
from eval.analyses.efficiency_analysis import (
    render_markdown as render_efficiency_markdown,
)
from eval.analyses.context_analysis import (
    render_markdown as render_context_markdown,
)

RUNS = [
    (
        "m3-final-run-002",
        M3_FINAL_RECOVERY_RUN_CONFIG,
    ),
    (
        "m3-final-run-003",
        M3_FINAL_INCREMENTAL_RUN_CONFIG,
    ),
]

EVALUATION_RUN_IDS = [
    run_id
    for run_id, _ in RUNS
]
EVAL_ID = "m3-final-eval-003"

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
    for run_id, run_config in RUNS:
        run_manifest_path = (
            RUNS_DIR / f"{run_id}.manifest.json"
        )
        run_results_path = (
            RUNS_DIR / f"{run_id}.json"
        )

        if (
            not run_manifest_path.exists()
            and not run_results_path.exists()
        ):
            start_run(
                run_id=run_id,
                run_config=run_config,
                progress_callback=print_progress,
            )
        else:
            resume_run(
                run_id=run_id,
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

    attempt_recovery_analysis_path = (
        evaluation_output_dir
        / "attempt_recovery_analysis.md"
    )

    tool_call_repair_analysis_path = (
        evaluation_output_dir
        / "tool_call_repair_analysis.md"
    )

    efficiency_analysis_path = (
        evaluation_output_dir
        / "efficiency_analysis.md"
    )

    context_analysis_path = (
        evaluation_output_dir / "context_analysis.md"
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

    attempt_recovery_analysis = (
        evaluation_result["analyses"][
            "attempt_recovery_analysis"
        ]
    )

    attempt_recovery_analysis_path.write_text(
        render_attempt_recovery_markdown(
            attempt_recovery_analysis
        ),
        encoding="utf-8",
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

    efficiency_analysis_path.write_text(
        render_efficiency_markdown(
            evaluation_result["analyses"]["efficiency_analysis"]
        ),
        encoding="utf-8",
    )

    context_analysis = (
        evaluation_result["analyses"]["context_analysis"]
    )

    context_analysis_path.write_text(
        render_context_markdown(context_analysis),
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
        "Análisis de recuperación entre attempts: "
        f"{attempt_recovery_analysis_path}"
    )
    print(
        "Análisis de reparación de tool calls: "
        f"{tool_call_repair_analysis_path}"
    )
    print(
        f"Análisis de eficiencia: {efficiency_analysis_path}"
    )
    print(
        "Análisis de presión de contexto: "
        f"{context_analysis_path}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
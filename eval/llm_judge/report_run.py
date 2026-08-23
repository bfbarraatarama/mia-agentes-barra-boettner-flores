"""Generación reproducible de reportes cualitativos desde código."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Permite ejecutar exactamente:
#     python eval/llm_judge/report_run.py
REPO_ROOT = Path(__file__).resolve().parents[2]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from eval.llm_judge.comparison import (
    compare_human_and_judge,
    compare_human_annotators,
)
from eval.llm_judge.configs.report_configs import REPORT_CONFIG
from eval.llm_judge.persistence import RESULTS_DIR
from eval.llm_judge.report import (
    build_judge_evaluation_status,
    render_human_agreement_report,
    render_judge_agreement_report,
    render_judge_evaluation_status,
)


def execute_report_config(
    report_config: dict[str, Any],
    *,
    results_dir: Path = RESULTS_DIR,
) -> str:
    """Construye las secciones solicitadas desde los artefactos persistidos."""

    sections = []

    status_config = report_config.get(
        "status"
    )

    if status_config is not None:
        status = build_judge_evaluation_status(
            status_config["dataset_id"],
            status_config["judge_eval_id"],
            results_dir=results_dir,
        )
        sections.append(
            render_judge_evaluation_status(
                status
            )
        )

    judge_agreement_config = (
        report_config.get(
            "judge_agreement"
        )
    )

    if judge_agreement_config is not None:
        report = compare_human_and_judge(
            judge_agreement_config[
                "dataset_id"
            ],
            judge_agreement_config[
                "judge_eval_id"
            ],
            judge_agreement_config[
                "annotator_id"
            ],
            results_dir=results_dir,
        )
        sections.append(
            render_judge_agreement_report(
                report
            )
        )

    human_agreement_config = (
        report_config.get(
            "human_agreement"
        )
    )

    if human_agreement_config is not None:
        report = compare_human_annotators(
            human_agreement_config[
                "dataset_id"
            ],
            human_agreement_config[
                "annotator_a_id"
            ],
            human_agreement_config[
                "annotator_b_id"
            ],
            split=human_agreement_config[
                "split"
            ],
            results_dir=results_dir,
        )
        sections.append(
            render_human_agreement_report(
                report
            )
        )

    if not sections:
        raise ValueError(
            "La configuración de reporte no selecciona "
            "ninguna sección."
        )

    return "\n\n".join(
        sections
    )


def main() -> int:
    if REPORT_CONFIG is None:
        print(
            "No hay una REPORT_CONFIG activa. "
            "Definí explícitamente la configuración del reporte "
            "en eval/llm_judge/configs/report_configs.py.",
            file=sys.stderr,
        )
        return 1

    print(
        execute_report_config(
            REPORT_CONFIG
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
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


from eval.llm_judge.annotations import load_human_annotations
from eval.llm_judge.comparison import (
    compare_human_and_judge,
    compare_human_annotators,
)
from eval.llm_judge.configs.report_configs import REPORT_CONFIG
from eval.llm_judge.persistence import (
    RESULTS_DIR,
    load_judge_case_predictions,
)
from eval.llm_judge.rubric import CRITERION_IDS
from eval.llm_judge.report import (
    build_judge_evaluation_status,
    render_human_agreement_report,
    render_judge_agreement_report,
    render_judge_evaluation_status,
)

def render_judge_agreement_details(
    dataset_id: str,
    judge_eval_id: str,
    annotator_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> str:
    """Renderiza las decisiones humano ↔ judge por caso y criterio."""

    human_annotations = load_human_annotations(
        dataset_id,
        annotator_id,
        results_dir=results_dir,
    )
    judge_predictions = load_judge_case_predictions(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )

    human_by_case = {
        annotation.case_id: annotation
        for annotation in human_annotations
    }

    lines = [
        "## Detalle por caso y criterio",
    ]

    for prediction in sorted(
        judge_predictions,
        key=lambda item: item.case_id,
    ):
        human_annotation = human_by_case.get(
            prediction.case_id
        )

        if human_annotation is None:
            raise ValueError(
                "No existe anotación humana para "
                f"{prediction.case_id!r}."
            )

        lines.extend([
            "",
            f"### {prediction.case_id}",
        ])

        for criterion_id in CRITERION_IDS:
            judge_decision = prediction.criteria.get(
                criterion_id
            )

            if judge_decision is None:
                continue

            human_decision = (
                human_annotation.criteria.get(
                    criterion_id
                )
            )

            if human_decision is None:
                raise ValueError(
                    "Falta la decisión humana para "
                    f"{prediction.case_id!r} / {criterion_id}."
                )

            agrees = (
                human_decision.verdict
                == judge_decision.verdict
            )

            lines.extend([
                "",
                f"#### {criterion_id}",
                "",
                f"- Acuerdo: {'SÍ' if agrees else 'NO'}",
                f"- Humano: `{human_decision.verdict}`",
                f"- LLM judge: `{judge_decision.verdict}`",
                "",
                "**Humano — justificación**",
                "",
                human_decision.reason,
                "",
                "**Humano — evidencia**",
                "",
                *[
                    f"- `{evidence_ref}`"
                    for evidence_ref
                    in human_decision.evidence_refs
                ],
                "",
                "**LLM judge — justificación**",
                "",
                judge_decision.reason,
                "",
                "**LLM judge — evidencia**",
                "",
                *[
                    f"- `{evidence_ref}`"
                    for evidence_ref
                    in judge_decision.evidence_refs
                ],
            ])

    return "\n".join(
        lines
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
            "\n\n".join([
                render_judge_agreement_report(
                    report
                ),
                render_judge_agreement_details(
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
                ),
            ])
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

    rendered = execute_report_config(
        REPORT_CONFIG
    )

    report_id = REPORT_CONFIG.get(
        "report_id"
    )

    if not isinstance(report_id, str) or not report_id.strip():
        raise ValueError(
            "La configuración activa debe definir un report_id."
        )

    if Path(report_id).name != report_id:
        raise ValueError(
            "report_id debe ser un nombre simple, sin directorios."
        )

    dataset_ids = {
        section["dataset_id"]
        for section_name in (
            "status",
            "judge_agreement",
            "human_agreement",
        )
        if (
            section := REPORT_CONFIG.get(
                section_name
            )
        ) is not None
    }

    if len(dataset_ids) != 1:
        raise ValueError(
            "Todas las secciones del reporte deben pertenecer "
            "al mismo dataset."
        )

    dataset_id = next(
        iter(dataset_ids)
    )
    reports_dir = (
        RESULTS_DIR
        / dataset_id
        / "reports"
    )
    reports_dir.mkdir(
        parents=True,
        exist_ok=True,
    )
    report_path = (
        reports_dir
        / f"{report_id}.md"
    )

    report_path.write_text(
        rendered + "\n",
        encoding="utf-8",
    )

    print(
        rendered
    )
    print()
    print(
        f"Reporte: {report_path}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
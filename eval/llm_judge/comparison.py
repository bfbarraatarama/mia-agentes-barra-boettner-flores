"""Comparación entre anotaciones humanas y predicciones del LLM judge."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from eval.llm_judge.annotations import (
    load_human_annotations,
    validate_human_annotation,
)
from eval.llm_judge.models import (
    CaseSplit,
    HumanAnnotation,
    HumanVerdict,
    JudgeCasePrediction,
    JudgeVerdict,
)
from eval.llm_judge.persistence import (
    RESULTS_DIR,
    load_dataset_manifest,
    load_judge_case_predictions,
    load_judge_evaluation_manifest,
    load_qualitative_cases,
)
from eval.llm_judge.rubric import (
    CRITERION_IDS,
    CriterionId,
)


@dataclass(frozen=True)
class ConfusionMatrix:
    """Conteos con el primer evaluador en filas y el segundo en columnas."""

    first_pass_second_pass: int
    first_pass_second_fail: int
    first_fail_second_pass: int
    first_fail_second_fail: int


@dataclass(frozen=True)
class AgreementStats:
    """Métricas de acuerdo para un conjunto de pares de veredictos."""

    n: int
    agreement: float | None
    cohen_kappa: float | None
    confusion: ConfusionMatrix


@dataclass(frozen=True)
class JudgeAgreementReport:
    """Comparación completa de un judge contra un anotador humano."""

    dataset_id: str
    judge_eval_id: str
    annotator_id: str
    split: CaseSplit
    case_ids: tuple[str, ...]
    overall: AgreementStats
    by_criterion: dict[
        CriterionId,
        AgreementStats,
    ]


@dataclass(frozen=True)
class HumanAgreementReport:
    """Comparación independiente entre dos anotadores humanos."""

    dataset_id: str
    annotator_a_id: str
    annotator_b_id: str
    split: CaseSplit
    case_ids: tuple[str, ...]
    overall: AgreementStats
    by_criterion: dict[
        CriterionId,
        AgreementStats,
    ]


def compute_agreement_stats(
    pairs: list[
        tuple[
            HumanVerdict,
            JudgeVerdict,
        ]
    ],
) -> AgreementStats:
    """Calcula acuerdo, confusión y Cohen's kappa."""

    first_pass_second_pass = sum(
        first == "PASS"
        and second == "PASS"
        for first, second in pairs
    )
    first_pass_second_fail = sum(
        first == "PASS"
        and second == "FAIL"
        for first, second in pairs
    )
    first_fail_second_pass = sum(
        first == "FAIL"
        and second == "PASS"
        for first, second in pairs
    )
    first_fail_second_fail = sum(
        first == "FAIL"
        and second == "FAIL"
        for first, second in pairs
    )

    confusion = ConfusionMatrix(
        first_pass_second_pass=first_pass_second_pass,
        first_pass_second_fail=first_pass_second_fail,
        first_fail_second_pass=first_fail_second_pass,
        first_fail_second_fail=first_fail_second_fail,
    )

    n = len(pairs)

    if n == 0:
        return AgreementStats(
            n=0,
            agreement=None,
            cohen_kappa=None,
            confusion=confusion,
        )

    agreement = (
        first_pass_second_pass
        + first_fail_second_fail
    ) / n

    first_pass = (
        first_pass_second_pass
        + first_pass_second_fail
    )
    first_fail = (
        first_fail_second_pass
        + first_fail_second_fail
    )
    second_pass = (
        first_pass_second_pass
        + first_fail_second_pass
    )
    second_fail = (
        first_pass_second_fail
        + first_fail_second_fail
    )

    expected_agreement = (
        first_pass * second_pass
        + first_fail * second_fail
    ) / (n * n)

    cohen_kappa = (
        None
        if expected_agreement == 1.0
        else (
            agreement
            - expected_agreement
        ) / (
            1.0
            - expected_agreement
        )
    )

    return AgreementStats(
        n=n,
        agreement=agreement,
        cohen_kappa=cohen_kappa,
        confusion=confusion,
    )


def _load_complete_human_annotations(
    dataset_id: str,
    annotator_id: str,
    case_ids: tuple[str, ...],
    cases_by_id: dict[str, object],
    *,
    results_dir: Path,
) -> dict[str, HumanAnnotation]:
    """Carga anotaciones completas para los casos que se van a comparar."""

    annotations = load_human_annotations(
        dataset_id,
        annotator_id,
        results_dir=results_dir,
    )
    annotations_by_id = {
        annotation.case_id: annotation
        for annotation in annotations
    }

    missing_annotations = sorted(
        set(case_ids)
        - set(annotations_by_id)
    )

    if missing_annotations:
        raise ValueError(
            f"Faltan anotaciones humanas de {annotator_id!r} "
            f"para los casos evaluados: {missing_annotations}."
        )

    selected_annotations = {}

    for case_id in case_ids:
        case = cases_by_id[
            case_id
        ]
        annotation = annotations_by_id[
            case_id
        ]

        if annotation.annotator_id != annotator_id:
            raise ValueError(
                f"La anotación de {case_id!r} declara "
                f"annotator_id={annotation.annotator_id!r}, "
                f"pero se solicitó {annotator_id!r}."
            )

        validate_human_annotation(
            case,
            annotation,
        )

        applicable_criteria = {
            criterion_id
            for criterion_id, applicability
            in case.criteria_applicability.items()
            if applicability.applicable
        }
        annotated_criteria = set(
            annotation.criteria
        )

        if annotated_criteria != applicable_criteria:
            missing = sorted(
                applicable_criteria
                - annotated_criteria
            )
            unexpected = sorted(
                annotated_criteria
                - applicable_criteria
            )

            raise ValueError(
                f"La anotación humana de {annotator_id!r} "
                f"para {case_id!r} debe estar completa "
                "para comparar. "
                f"Faltantes: {missing}; "
                f"no aplicables: {unexpected}."
            )

        selected_annotations[
            case_id
        ] = annotation

    return selected_annotations


def _validate_judge_prediction_against_manifest(
    prediction: JudgeCasePrediction,
    manifest: dict,
) -> None:
    """Valida que una predicción pertenezca a la política persistida."""

    manifest_versions = manifest[
        "versions"
    ]
    prediction_versions = {
        "prediction_schema_version": (
            prediction.schema_version
        ),
        "case_schema_version": (
            prediction.case_schema_version
        ),
        "case_view_version": (
            prediction.case_view_version
        ),
        "presentation_version": (
            prediction.presentation_version
        ),
        "rubric_version": (
            prediction.rubric_version
        ),
        "judge_prompt_version": (
            prediction.judge_prompt_version
        ),
    }

    mismatched_versions = {
        key: (
            prediction_versions[key],
            manifest_versions.get(key),
        )
        for key in prediction_versions
        if (
            prediction_versions[key]
            != manifest_versions.get(key)
        )
    }

    if mismatched_versions:
        raise ValueError(
            f"La predicción del judge para "
            f"{prediction.case_id!r} no corresponde "
            "al manifest de su evaluación. "
            f"Diferencias: {mismatched_versions}."
        )


def compare_human_and_judge(
    dataset_id: str,
    judge_eval_id: str,
    annotator_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> JudgeAgreementReport:
    """Compara una evaluación completa del judge con un anotador."""

    manifest = load_judge_evaluation_manifest(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )
    case_ids = tuple(
        manifest[
            "case_ids"
        ]
    )

    cases = load_qualitative_cases(
        dataset_id,
        results_dir=results_dir,
    )
    cases_by_id = {
        case.case_id: case
        for case in cases
    }

    missing_cases = [
        case_id
        for case_id in case_ids
        if case_id not in cases_by_id
    ]

    if missing_cases:
        raise ValueError(
            "La evaluación referencia casos inexistentes: "
            f"{missing_cases}."
        )

    predictions = load_judge_case_predictions(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )
    predictions_by_id = {
        prediction.case_id: prediction
        for prediction in predictions
    }

    expected_case_ids = set(
        case_ids
    )
    predicted_case_ids = set(
        predictions_by_id
    )

    if predicted_case_ids != expected_case_ids:
        missing = sorted(
            expected_case_ids
            - predicted_case_ids
        )
        unexpected = sorted(
            predicted_case_ids
            - expected_case_ids
        )

        raise ValueError(
            "La evaluación del judge debe estar completa antes "
            "de calcular acuerdo. "
            f"Faltantes: {missing}; "
            f"inesperados: {unexpected}."
        )

    annotations_by_id = (
        _load_complete_human_annotations(
            dataset_id,
            annotator_id,
            case_ids,
            cases_by_id,
            results_dir=results_dir,
        )
    )

    pairs_by_criterion: dict[
        CriterionId,
        list[
            tuple[
                HumanVerdict,
                JudgeVerdict,
            ]
        ],
    ] = {
        criterion_id: []
        for criterion_id in CRITERION_IDS
    }
    all_pairs: list[
        tuple[
            HumanVerdict,
            JudgeVerdict,
        ]
    ] = []

    for case_id in case_ids:
        case = cases_by_id[
            case_id
        ]
        annotation = annotations_by_id[
            case_id
        ]
        prediction = predictions_by_id[
            case_id
        ]

        applicable_criteria = {
            criterion_id
            for criterion_id, applicability
            in case.criteria_applicability.items()
            if applicability.applicable
        }

        _validate_judge_prediction_against_manifest(
            prediction,
            manifest,
        )

        predicted_criteria = set(
            prediction.criteria
        )

        if predicted_criteria != applicable_criteria:
            missing = sorted(
                applicable_criteria
                - predicted_criteria
            )
            unexpected = sorted(
                predicted_criteria
                - applicable_criteria
            )

            raise ValueError(
                f"La predicción del judge para {case_id!r} "
                "debe contener exactamente los criterios "
                "aplicables. "
                f"Faltantes: {missing}; "
                f"no aplicables: {unexpected}."
            )

        for criterion_id in CRITERION_IDS:
            if criterion_id not in applicable_criteria:
                continue

            pair = (
                annotation.criteria[
                    criterion_id
                ].verdict,
                prediction.criteria[
                    criterion_id
                ].verdict,
            )

            pairs_by_criterion[
                criterion_id
            ].append(
                pair
            )
            all_pairs.append(
                pair
            )

    return JudgeAgreementReport(
        dataset_id=dataset_id,
        judge_eval_id=judge_eval_id,
        annotator_id=annotator_id,
        split=manifest["split"],
        case_ids=case_ids,
        overall=compute_agreement_stats(
            all_pairs
        ),
        by_criterion={
            criterion_id: compute_agreement_stats(
                pairs_by_criterion[
                    criterion_id
                ]
            )
            for criterion_id in CRITERION_IDS
        },
    )


def compare_human_annotators(
    dataset_id: str,
    annotator_a_id: str,
    annotator_b_id: str,
    *,
    split: CaseSplit,
    results_dir: Path = RESULTS_DIR,
) -> HumanAgreementReport:
    """Compara dos anotadores independientes sobre un mismo split."""

    if annotator_a_id == annotator_b_id:
        raise ValueError(
            "Los dos annotator_id deben ser distintos."
        )

    if split not in {
        "dev",
        "holdout",
    }:
        raise ValueError(
            f"Split cualitativo desconocido: {split!r}."
        )

    manifest = load_dataset_manifest(
        dataset_id,
        results_dir=results_dir,
    )
    case_ids = tuple(
        manifest[
            "splits"
        ][
            split
        ]
    )

    if not case_ids:
        raise ValueError(
            f"El split {split!r} no contiene casos."
        )

    cases = load_qualitative_cases(
        dataset_id,
        results_dir=results_dir,
    )
    cases_by_id = {
        case.case_id: case
        for case in cases
    }

    missing_cases = [
        case_id
        for case_id in case_ids
        if case_id not in cases_by_id
    ]

    if missing_cases:
        raise ValueError(
            "El split referencia casos inexistentes: "
            f"{missing_cases}."
        )

    annotations_a = (
        _load_complete_human_annotations(
            dataset_id,
            annotator_a_id,
            case_ids,
            cases_by_id,
            results_dir=results_dir,
        )
    )
    annotations_b = (
        _load_complete_human_annotations(
            dataset_id,
            annotator_b_id,
            case_ids,
            cases_by_id,
            results_dir=results_dir,
        )
    )

    pairs_by_criterion: dict[
        CriterionId,
        list[
            tuple[
                HumanVerdict,
                HumanVerdict,
            ]
        ],
    ] = {
        criterion_id: []
        for criterion_id in CRITERION_IDS
    }
    all_pairs: list[
        tuple[
            HumanVerdict,
            HumanVerdict,
        ]
    ] = []

    for case_id in case_ids:
        case = cases_by_id[
            case_id
        ]
        annotation_a = annotations_a[
            case_id
        ]
        annotation_b = annotations_b[
            case_id
        ]

        for criterion_id in CRITERION_IDS:
            if not case.criteria_applicability[
                criterion_id
            ].applicable:
                continue

            pair = (
                annotation_a.criteria[
                    criterion_id
                ].verdict,
                annotation_b.criteria[
                    criterion_id
                ].verdict,
            )

            pairs_by_criterion[
                criterion_id
            ].append(
                pair
            )
            all_pairs.append(
                pair
            )

    return HumanAgreementReport(
        dataset_id=dataset_id,
        annotator_a_id=annotator_a_id,
        annotator_b_id=annotator_b_id,
        split=split,
        case_ids=case_ids,
        overall=compute_agreement_stats(
            all_pairs
        ),
        by_criterion={
            criterion_id: compute_agreement_stats(
                pairs_by_criterion[
                    criterion_id
                ]
            )
            for criterion_id in CRITERION_IDS
        },
    )
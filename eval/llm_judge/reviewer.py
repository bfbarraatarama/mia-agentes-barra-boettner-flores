"""Estado de revisión humana de datasets cualitativos."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from eval.llm_judge.annotations import (
    load_human_annotations,
)
from eval.llm_judge.models import (
    CaseSplit,
    HumanAnnotation,
    QualitativeCase,
)
from eval.llm_judge.persistence import (
    RESULTS_DIR,
    load_dataset_manifest,
    load_qualitative_cases,
)
from eval.llm_judge.presentation import (
    CasePresentation,
    build_case_presentation,
)


@dataclass(frozen=True)
class ReviewCase:
    """Caso preparado para su revisión humana."""

    case: QualitativeCase
    split: CaseSplit
    presentation: CasePresentation
    annotation: HumanAnnotation | None

    @property
    def case_id(self) -> str:
        return self.case.case_id

    @property
    def annotated(self) -> bool:
        """Indica si existe alguna anotación persistida."""

        return self.annotation is not None

    @property
    def completed(self) -> bool:
        """Indica si están anotados todos los criterios aplicables."""

        if self.annotation is None:
            return False

        applicable_criteria = {
            criterion_id
            for criterion_id, applicability
            in self.case.criteria_applicability.items()
            if applicability.applicable
        }

        return (
            set(self.annotation.criteria)
            == applicable_criteria
        )

    @property
    def in_progress(self) -> bool:
        """Indica si existe una anotación todavía incompleta."""

        return (
            self.annotated
            and not self.completed
        )


def load_review_cases(
    dataset_id: str,
    annotator_id: str,
    *,
    split: CaseSplit | None = None,
    results_dir: Path = RESULTS_DIR,
) -> list[ReviewCase]:
    """Carga casos ciegos y su estado de revisión para un anotador."""

    manifest = load_dataset_manifest(
        dataset_id,
        results_dir=results_dir,
    )
    cases = load_qualitative_cases(
        dataset_id,
        results_dir=results_dir,
    )
    annotations = load_human_annotations(
        dataset_id,
        annotator_id,
        results_dir=results_dir,
    )

    splits_by_case_id = {
        case_id: split_name
        for split_name, case_ids in manifest["splits"].items()
        for case_id in case_ids
    }

    cases_by_id = {
        case.case_id: case
        for case in cases
    }

    if set(splits_by_case_id) != set(cases_by_id):
        raise ValueError(
            "Los splits del manifest no corresponden exactamente "
            "a los casos del dataset."
        )

    annotations_by_case_id = {
        annotation.case_id: annotation
        for annotation in annotations
    }

    unknown_annotation_ids = (
        set(annotations_by_case_id)
        - set(cases_by_id)
    )

    if unknown_annotation_ids:
        raise ValueError(
            "Existen anotaciones para casos que no pertenecen "
            "al dataset."
        )

    review_cases = []

    for case in cases:
        case_split = splits_by_case_id[case.case_id]

        if split is not None and case_split != split:
            continue

        review_cases.append(ReviewCase(
            case=case,
            split=case_split,
            presentation=build_case_presentation(case),
            annotation=annotations_by_case_id.get(
                case.case_id
            ),
        ))

    return review_cases
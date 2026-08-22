"""Validación de anotaciones humanas para evaluación cualitativa."""

from __future__ import annotations
from pathlib import Path

from eval.llm_judge.models import (
    HumanAnnotation,
    QualitativeCase,
)
from eval.llm_judge.persistence import (
    RESULTS_DIR,
    load_dataset_manifest,
    load_qualitative_cases,
)
from eval.llm_judge.rubric import RUBRIC_VERSION
from eval.llm_judge.presentation import (
    PRESENTATION_VERSION,
    build_case_presentation,
)


HUMAN_ANNOTATION_SCHEMA_VERSION = 1


def _validate_annotator_id(annotator_id: str) -> None:
    """Valida un identificador utilizable como nombre de archivo."""

    if not annotator_id:
        raise ValueError(
            "annotator_id no puede estar vacío."
        )

    if (
        annotator_id in {".", ".."}
        or "/" in annotator_id
        or "\\" in annotator_id
    ):
        raise ValueError(
            "annotator_id no puede contener separadores de ruta."
        )


def _annotation_path(
    dataset_id: str,
    annotator_id: str,
    results_dir: Path,
) -> Path:
    """Devuelve la ruta de las anotaciones de un anotador."""

    _validate_annotator_id(annotator_id)

    return (
        results_dir
        / dataset_id
        / "annotations"
        / f"{annotator_id}.jsonl"
    )


def validate_human_annotation(
    case: QualitativeCase,
    annotation: HumanAnnotation,
) -> None:
    """Valida que una anotación corresponda exactamente al caso evaluado."""

    if annotation.schema_version != HUMAN_ANNOTATION_SCHEMA_VERSION:
        raise ValueError(
            "La versión del schema de anotación no es compatible."
        )

    if annotation.case_id != case.case_id:
        raise ValueError(
            "La anotación no corresponde al case_id evaluado."
        )

    if annotation.case_schema_version != case.schema_version:
        raise ValueError(
            "La anotación no corresponde al schema del caso evaluado."
        )

    if annotation.case_view_version != case.case_view_version:
        raise ValueError(
            "La anotación no corresponde a la vista del caso evaluado."
        )

    if annotation.presentation_version != PRESENTATION_VERSION:
        raise ValueError(
            "La anotación no corresponde a la versión vigente "
            "de la presentación."
        )

    if annotation.rubric_version != RUBRIC_VERSION:
        raise ValueError(
            "La anotación no corresponde a la versión vigente de la rúbrica."
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

    if not annotated_criteria:
        raise ValueError(
            "La anotación debe contener al menos un criterio "
            "completado."
        )

    non_applicable_criteria = (
        annotated_criteria
        - applicable_criteria
    )

    if non_applicable_criteria:
        raise ValueError(
            "La anotación contiene criterios no aplicables "
            f"al caso: {sorted(non_applicable_criteria)}."
        )

    valid_evidence_refs = set(
        build_case_presentation(case).evidence_refs
    )

    for criterion_id, criterion_annotation in annotation.criteria.items():
        invalid_refs = (
            set(criterion_annotation.evidence_refs)
            - valid_evidence_refs
        )

        if invalid_refs:
            raise ValueError(
                f"El criterio {criterion_id} contiene referencias "
                f"de evidencia inexistentes: {sorted(invalid_refs)}."
            )


def load_human_annotations(
    dataset_id: str,
    annotator_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> list[HumanAnnotation]:
    """Carga las anotaciones persistidas de un anotador."""

    load_dataset_manifest(
        dataset_id,
        results_dir=results_dir,
    )

    input_path = _annotation_path(
        dataset_id,
        annotator_id,
        results_dir,
    )

    if not input_path.exists():
        return []

    annotations = [
        HumanAnnotation.model_validate_json(line)
        for line in input_path.read_text(
            encoding="utf-8",
        ).splitlines()
        if line.strip()
    ]

    case_ids = [
        annotation.case_id
        for annotation in annotations
    ]

    if len(case_ids) != len(set(case_ids)):
        raise ValueError(
            "Las anotaciones de un mismo anotador contienen "
            "case_id duplicados."
        )

    return annotations


def save_human_annotation(
    dataset_id: str,
    annotation: HumanAnnotation,
    *,
    results_dir: Path = RESULTS_DIR,
) -> None:
    """Valida y persiste una nueva anotación sin sobrescribir casos."""

    cases = load_qualitative_cases(
        dataset_id,
        results_dir=results_dir,
    )
    cases_by_id = {
        case.case_id: case
        for case in cases
    }

    case = cases_by_id.get(annotation.case_id)

    if case is None:
        raise ValueError(
            f"El case_id {annotation.case_id!r} no pertenece "
            f"al dataset {dataset_id!r}."
        )

    validate_human_annotation(
        case,
        annotation,
    )

    existing_annotations = load_human_annotations(
        dataset_id,
        annotation.annotator_id,
        results_dir=results_dir,
    )

    if any(
        existing.case_id == annotation.case_id
        for existing in existing_annotations
    ):
        raise FileExistsError(
            f"El anotador {annotation.annotator_id!r} ya tiene "
            f"una anotación para {annotation.case_id!r}."
        )

    output_path = _annotation_path(
        dataset_id,
        annotation.annotator_id,
        results_dir,
    )
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "a",
        encoding="utf-8",
    ) as output_file:
        output_file.write(
            annotation.model_dump_json()
            + "\n"
        )


def list_annotators(
    dataset_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> list[str]:
    """Lista los anotadores registrados para un dataset."""

    load_dataset_manifest(
        dataset_id,
        results_dir=results_dir,
    )

    annotations_dir = (
        results_dir
        / dataset_id
        / "annotations"
    )

    if not annotations_dir.exists():
        return []

    return sorted(
        path.name.removesuffix(".jsonl")
        for path in annotations_dir.glob("*.jsonl")
        if path.is_file()
    )


def create_annotator(
    dataset_id: str,
    annotator_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> None:
    """Registra un anotador sin crear anotaciones."""

    load_dataset_manifest(
        dataset_id,
        results_dir=results_dir,
    )

    output_path = _annotation_path(
        dataset_id,
        annotator_id,
        results_dir,
    )

    if output_path.exists():
        raise FileExistsError(
            f"El anotador {annotator_id!r} ya existe."
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    output_path.touch()


def update_human_annotation(
    dataset_id: str,
    annotation: HumanAnnotation,
    *,
    results_dir: Path = RESULTS_DIR,
) -> None:
    """Actualiza explícitamente una anotación existente."""

    cases = load_qualitative_cases(
        dataset_id,
        results_dir=results_dir,
    )
    cases_by_id = {
        case.case_id: case
        for case in cases
    }

    case = cases_by_id.get(annotation.case_id)

    if case is None:
        raise ValueError(
            f"El case_id {annotation.case_id!r} no pertenece "
            f"al dataset {dataset_id!r}."
        )

    validate_human_annotation(
        case,
        annotation,
    )

    annotations = load_human_annotations(
        dataset_id,
        annotation.annotator_id,
        results_dir=results_dir,
    )

    matching_indexes = [
        index
        for index, existing in enumerate(annotations)
        if existing.case_id == annotation.case_id
    ]

    if not matching_indexes:
        raise FileNotFoundError(
            f"El anotador {annotation.annotator_id!r} no tiene "
            f"una anotación para {annotation.case_id!r}."
        )

    annotations[matching_indexes[0]] = annotation

    output_path = _annotation_path(
        dataset_id,
        annotation.annotator_id,
        results_dir,
    )
    output_path.write_text(
        "".join(
            existing.model_dump_json() + "\n"
            for existing in annotations
        ),
        encoding="utf-8",
    )


def delete_human_annotation(
    dataset_id: str,
    annotator_id: str,
    case_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> None:
    """Elimina explícitamente una anotación de un caso."""

    annotations = load_human_annotations(
        dataset_id,
        annotator_id,
        results_dir=results_dir,
    )

    remaining = [
        annotation
        for annotation in annotations
        if annotation.case_id != case_id
    ]

    if len(remaining) == len(annotations):
        raise FileNotFoundError(
            f"El anotador {annotator_id!r} no tiene "
            f"una anotación para {case_id!r}."
        )

    output_path = _annotation_path(
        dataset_id,
        annotator_id,
        results_dir,
    )
    output_path.write_text(
        "".join(
            annotation.model_dump_json() + "\n"
            for annotation in remaining
        ),
        encoding="utf-8",
    )


def delete_annotator(
    dataset_id: str,
    annotator_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> None:
    """Elimina un anotador y todas sus anotaciones."""

    load_dataset_manifest(
        dataset_id,
        results_dir=results_dir,
    )

    annotation_path = _annotation_path(
        dataset_id,
        annotator_id,
        results_dir,
    )

    if not annotation_path.exists():
        raise FileNotFoundError(
            f"El anotador {annotator_id!r} no existe."
        )

    annotation_path.unlink()
"""Persistencia de datasets para evaluación cualitativa."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
from typing import Any

from eval.llm_judge.cases import (
    CASE_VIEW_VERSION,
    QUALITATIVE_CASE_SCHEMA_VERSION,
    build_qualitative_case,
)
from eval.llm_judge.models import (
    CaseSource,
    QualitativeCase,
)
from eval.llm_judge.rubric import RUBRIC_VERSION
from eval.llm_judge.sampling import SampledTrial


REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "eval" / "results" / "llm_judge"

DATASET_MANIFEST_SCHEMA_VERSION = 1


def _validate_dataset_id(dataset_id: str) -> None:
    """Valida un dataset_id que pueda utilizarse como directorio."""

    if not dataset_id:
        raise ValueError("dataset_id no puede estar vacío.")

    if (
        dataset_id in {".", ".."}
        or "/" in dataset_id
        or "\\" in dataset_id
    ):
        raise ValueError(
            "dataset_id no puede contener separadores de ruta."
        )


def _created_at() -> str:
    """Devuelve el instante de creación del dataset en UTC."""

    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _dataset_paths(
    dataset_id: str,
    results_dir: Path,
) -> tuple[Path, Path, Path, Path]:
    """Devuelve las rutas de los artefactos de un dataset."""

    _validate_dataset_id(dataset_id)

    dataset_dir = results_dir / dataset_id

    return (
        dataset_dir,
        dataset_dir / "manifest.json",
        dataset_dir / "cases.jsonl",
        dataset_dir / "case_sources.jsonl",
    )


def _validate_sampled_trials(
    sampled_trials: list[SampledTrial],
) -> None:
    """Valida unicidad y presencia de casos seleccionados."""

    if not sampled_trials:
        raise ValueError(
            "El dataset debe contener al menos un trial seleccionado."
        )

    case_ids = [
        sample.case_id
        for sample in sampled_trials
    ]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError(
            "Los case_id del dataset deben ser únicos."
        )

    identities = [
        sample.candidate.identity
        for sample in sampled_trials
    ]
    if len(identities) != len(set(identities)):
        raise ValueError(
            "Un mismo trial de origen no puede aparecer más de una vez."
        )


def build_dataset_manifest(
    dataset_config: dict[str, Any],
    sampled_trials: list[SampledTrial],
) -> dict[str, Any]:
    """Construye el manifest reproducible de un dataset cualitativo."""

    dataset_id = dataset_config["dataset_id"]

    _validate_dataset_id(dataset_id)
    _validate_sampled_trials(sampled_trials)

    dev_case_ids = sorted(
        sample.case_id
        for sample in sampled_trials
        if sample.split == "dev"
    )
    holdout_case_ids = sorted(
        sample.case_id
        for sample in sampled_trials
        if sample.split == "holdout"
    )

    persisted_config = deepcopy(dataset_config)
    del persisted_config["dataset_id"]

    return {
        "schema_version": DATASET_MANIFEST_SCHEMA_VERSION,
        "dataset_id": dataset_id,
        "created_at": _created_at(),
        "rubric_version": RUBRIC_VERSION,
        "case_schema_version": QUALITATIVE_CASE_SCHEMA_VERSION,
        "case_view_version": CASE_VIEW_VERSION,
        "dataset": persisted_config,
        "counts": {
            "total": len(sampled_trials),
            "dev": len(dev_case_ids),
            "holdout": len(holdout_case_ids),
        },
        "splits": {
            "dev": dev_case_ids,
            "holdout": holdout_case_ids,
        },
    }


def _serialize_jsonl(
    models: list[QualitativeCase] | list[CaseSource],
) -> str:
    """Serializa modelos Pydantic como JSON Lines."""

    return "".join(
        json.dumps(
            model.model_dump(mode="json"),
            ensure_ascii=False,
        ) + "\n"
        for model in models
    )


def create_qualitative_dataset(
    dataset_config: dict[str, Any],
    sampled_trials: list[SampledTrial],
    *,
    results_dir: Path = RESULTS_DIR,
) -> dict[str, Any]:
    """Materializa casos ciegos y su procedencia sin sobrescribir."""

    _validate_sampled_trials(sampled_trials)

    dataset_id = dataset_config["dataset_id"]

    manifest = build_dataset_manifest(
        dataset_config,
        sampled_trials,
    )

    cases = [
        build_qualitative_case(
            sample.candidate.trial,
            case_id=sample.case_id,
        )
        for sample in sampled_trials
    ]
    case_sources = [
        sample.case_source()
        for sample in sampled_trials
    ]

    cases_content = _serialize_jsonl(cases)
    sources_content = _serialize_jsonl(case_sources)
    manifest_content = (
        json.dumps(
            manifest,
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )

    (
        dataset_dir,
        manifest_path,
        cases_path,
        sources_path,
    ) = _dataset_paths(
        dataset_id,
        results_dir,
    )

    if dataset_dir.exists():
        raise FileExistsError(
            f"El dataset_id {dataset_id!r} ya existe."
        )

    dataset_dir.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        dataset_dir.mkdir()

        manifest_path.write_text(
            manifest_content,
            encoding="utf-8",
        )
        cases_path.write_text(
            cases_content,
            encoding="utf-8",
        )
        sources_path.write_text(
            sources_content,
            encoding="utf-8",
        )

    except BaseException:
        shutil.rmtree(
            dataset_dir,
            ignore_errors=True,
        )
        raise

    return manifest


def load_dataset_manifest(
    dataset_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> dict[str, Any]:
    """Carga el manifest de un dataset cualitativo."""

    _, manifest_path, _, _ = _dataset_paths(
        dataset_id,
        results_dir,
    )

    return json.loads(
        manifest_path.read_text(encoding="utf-8")
    )


def _load_jsonl(
    input_path: Path,
) -> list[dict[str, Any]]:
    """Carga registros JSON Lines ignorando líneas vacías."""

    return [
        json.loads(line)
        for line in input_path.read_text(
            encoding="utf-8",
        ).splitlines()
        if line.strip()
    ]


def load_qualitative_cases(
    dataset_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> list[QualitativeCase]:
    """Carga y valida los casos ciegos de un dataset."""

    _, _, cases_path, _ = _dataset_paths(
        dataset_id,
        results_dir,
    )

    return [
        QualitativeCase.model_validate(data)
        for data in _load_jsonl(cases_path)
    ]


def load_case_sources(
    dataset_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> list[CaseSource]:
    """Carga y valida la procedencia separada de los casos."""

    _, _, _, sources_path = _dataset_paths(
        dataset_id,
        results_dir,
    )

    return [
        CaseSource.model_validate(data)
        for data in _load_jsonl(sources_path)
    ]
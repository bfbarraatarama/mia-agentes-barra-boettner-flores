"""Persistencia de datasets para evaluación cualitativa."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile
from typing import Any

from eval.llm_judge.cases import (
    CASE_VIEW_VERSION,
    QUALITATIVE_CASE_SCHEMA_VERSION,
    build_qualitative_case,
)
from eval.llm_judge.models import (
    CaseSource,
    CaseSplit,
    JudgeCasePrediction,
    JudgeCriterionDecision,
    QualitativeCase,
)
from eval.llm_judge.judge import (
    JUDGE_PREDICTION_SCHEMA_VERSION,
    JUDGE_PROMPT_VERSION,
    JUDGE_SYSTEM_PROMPT,
    build_judge_case_prediction,
    judge_prompt_fingerprint,
)
from eval.llm_judge.presentation import (
    PRESENTATION_VERSION,
    build_case_presentation,
)
from eval.llm_judge.rubric import (
    CRITERION_IDS,
    RUBRIC_VERSION,
    CriterionId,
)
from eval.llm_judge.sampling import SampledTrial
from eval.experiment import _serialize_trace_event
from eval.persistence import (
    _effective_llm_config,
    _git_metadata,
    _write_json_atomic,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "eval" / "results" / "llm_judge"

DATASET_MANIFEST_SCHEMA_VERSION = 1
JUDGE_EVALUATION_MANIFEST_SCHEMA_VERSION = 1


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


def _write_jsonl_atomic(
    output_path: Path,
    records: list[dict[str, Any]],
) -> None:
    """Reemplaza un JSONL sólo después de escribirlo completamente."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_path = None

    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as output_file:
            temporary_path = Path(
                output_file.name
            )

            for record in records:
                output_file.write(
                    json.dumps(
                        record,
                        ensure_ascii=False,
                    )
                    + "\n"
                )

        os.replace(
            temporary_path,
            output_path,
        )

    except BaseException:
        if temporary_path is not None:
            temporary_path.unlink(
                missing_ok=True
            )

        raise


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


def _validate_judge_eval_id(
    judge_eval_id: str,
) -> None:
    """Valida un identificador utilizable como directorio de evaluación."""

    if not judge_eval_id:
        raise ValueError(
            "judge_eval_id no puede estar vacío."
        )

    if (
        judge_eval_id in {".", ".."}
        or "/" in judge_eval_id
        or "\\" in judge_eval_id
    ):
        raise ValueError(
            "judge_eval_id no puede contener separadores de ruta."
        )


def _judge_evaluation_paths(
    dataset_id: str,
    judge_eval_id: str,
    results_dir: Path,
) -> tuple[Path, Path, Path]:
    """Devuelve las rutas persistidas de una evaluación del judge."""

    _validate_dataset_id(
        dataset_id
    )
    _validate_judge_eval_id(
        judge_eval_id
    )

    evaluation_dir = (
        results_dir
        / dataset_id
        / "judge_evaluations"
        / judge_eval_id
    )

    return (
        evaluation_dir,
        evaluation_dir / "manifest.json",
        evaluation_dir / "predictions.jsonl",
    )


def _judge_evaluation_progress_path(
    dataset_id: str,
    judge_eval_id: str,
    results_dir: Path,
) -> Path:
    """Devuelve el checkpoint mutable de criterios ya evaluados."""

    evaluation_dir, _, _ = (
        _judge_evaluation_paths(
            dataset_id,
            judge_eval_id,
            results_dir,
        )
    )

    return evaluation_dir / "progress.json"


def _judge_evaluation_trace_path(
    dataset_id: str,
    judge_eval_id: str,
    results_dir: Path,
) -> Path:
    """Devuelve la traza de inferencias de una evaluación del judge."""

    evaluation_dir, _, _ = (
        _judge_evaluation_paths(
            dataset_id,
            judge_eval_id,
            results_dir,
        )
    )

    return evaluation_dir / "trace.jsonl"


def build_judge_evaluation_manifest(
    dataset_id: str,
    judge_eval_id: str,
    *,
    split: CaseSplit,
    judge_llm_config: str,
    max_repair_attempts: int,
    results_dir: Path = RESULTS_DIR,
) -> dict[str, Any]:
    """Construye el manifest reproducible de una evaluación del judge."""

    _validate_judge_eval_id(
        judge_eval_id
    )

    if split not in {
        "dev",
        "holdout",
    }:
        raise ValueError(
            f"Split cualitativo desconocido: {split!r}."
        )

    if max_repair_attempts < 0:
        raise ValueError(
            "max_repair_attempts debe ser no negativo."
        )

    dataset_manifest = load_dataset_manifest(
        dataset_id,
        results_dir=results_dir,
    )

    expected_dataset_versions = {
        "rubric_version": RUBRIC_VERSION,
        "case_schema_version": QUALITATIVE_CASE_SCHEMA_VERSION,
        "case_view_version": CASE_VIEW_VERSION,
    }

    mismatched_versions = {
        key: (
            dataset_manifest.get(key),
            expected,
        )
        for key, expected
        in expected_dataset_versions.items()
        if dataset_manifest.get(key) != expected
    }

    if mismatched_versions:
        raise ValueError(
            "El dataset cualitativo no corresponde a las versiones "
            "vigentes requeridas por el judge: "
            f"{mismatched_versions}."
        )

    case_ids = list(
        dataset_manifest[
            "splits"
        ][split]
    )

    if not case_ids:
        raise ValueError(
            f"El split {split!r} no contiene casos."
        )

    try:
        effective_llm_config = (
            _effective_llm_config(
                judge_llm_config
            )
        )
    except KeyError as exc:
        raise ValueError(
            "Configuración de LLM del judge desconocida: "
            f"{judge_llm_config!r}."
        ) from exc

    return {
        "schema_version": (
            JUDGE_EVALUATION_MANIFEST_SCHEMA_VERSION
        ),
        "judge_eval_id": judge_eval_id,
        "dataset_id": dataset_id,
        "created_at": _created_at(),
        "git": _git_metadata(),
        "split": split,
        "case_ids": case_ids,
        "judge": {
            "llm_config": judge_llm_config,
            "effective_llm_config": effective_llm_config,
            "system_prompt": JUDGE_SYSTEM_PROMPT,
            "prompt_fingerprint_sha256": (
                judge_prompt_fingerprint()
            ),
            "max_repair_attempts": max_repair_attempts,
        },
        "versions": {
            "prediction_schema_version": (
                JUDGE_PREDICTION_SCHEMA_VERSION
            ),
            "case_schema_version": (
                QUALITATIVE_CASE_SCHEMA_VERSION
            ),
            "case_view_version": CASE_VIEW_VERSION,
            "presentation_version": PRESENTATION_VERSION,
            "rubric_version": RUBRIC_VERSION,
            "judge_prompt_version": JUDGE_PROMPT_VERSION,
        },
    }


def create_judge_evaluation(
    dataset_id: str,
    judge_eval_id: str,
    *,
    split: CaseSplit,
    judge_llm_config: str,
    max_repair_attempts: int,
    results_dir: Path = RESULTS_DIR,
) -> dict[str, Any]:
    """Inicializa una evaluación inmutable del judge sin predicciones."""

    manifest = build_judge_evaluation_manifest(
        dataset_id,
        judge_eval_id,
        split=split,
        judge_llm_config=judge_llm_config,
        max_repair_attempts=max_repair_attempts,
        results_dir=results_dir,
    )

    (
        evaluation_dir,
        manifest_path,
        predictions_path,
    ) = _judge_evaluation_paths(
        dataset_id,
        judge_eval_id,
        results_dir,
    )
    progress_path = (
        _judge_evaluation_progress_path(
            dataset_id,
            judge_eval_id,
            results_dir,
        )
    )
    trace_path = (
        _judge_evaluation_trace_path(
            dataset_id,
            judge_eval_id,
            results_dir,
        )
    )

    if evaluation_dir.exists():
        raise FileExistsError(
            f"El judge_eval_id {judge_eval_id!r} ya existe "
            f"para el dataset {dataset_id!r}."
        )

    evaluation_dir.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        evaluation_dir.mkdir()

        manifest_path.write_text(
            json.dumps(
                manifest,
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        predictions_path.write_text(
            "",
            encoding="utf-8",
        )
        _write_json_atomic(
            progress_path,
            {},
        )
        trace_path.write_text(
            "",
            encoding="utf-8",
        )

    except BaseException:
        shutil.rmtree(
            evaluation_dir,
            ignore_errors=True,
        )
        raise

    return manifest


def load_judge_evaluation_manifest(
    dataset_id: str,
    judge_eval_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> dict[str, Any]:
    """Carga el manifest persistido de una evaluación del judge."""

    _, manifest_path, _ = (
        _judge_evaluation_paths(
            dataset_id,
            judge_eval_id,
            results_dir,
        )
    )

    return json.loads(
        manifest_path.read_text(
            encoding="utf-8",
        )
    )


def require_current_judge_evaluation(
    dataset_id: str,
    judge_eval_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> dict[str, Any]:
    """Exige una evaluación compatible con la política vigente."""

    manifest = load_judge_evaluation_manifest(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )

    expected_versions = {
        "prediction_schema_version": (
            JUDGE_PREDICTION_SCHEMA_VERSION
        ),
        "case_schema_version": (
            QUALITATIVE_CASE_SCHEMA_VERSION
        ),
        "case_view_version": CASE_VIEW_VERSION,
        "presentation_version": PRESENTATION_VERSION,
        "rubric_version": RUBRIC_VERSION,
        "judge_prompt_version": JUDGE_PROMPT_VERSION,
    }

    actual_versions = manifest.get(
        "versions",
        {},
    )
    mismatched_versions = {
        key: (
            actual_versions.get(key),
            expected,
        )
        for key, expected in expected_versions.items()
        if actual_versions.get(key) != expected
    }

    persisted_prompt_fingerprint = (
        manifest.get(
            "judge",
            {},
        ).get(
            "prompt_fingerprint_sha256"
        )
    )
    current_prompt_fingerprint = (
        judge_prompt_fingerprint()
    )
    prompt_fingerprint_mismatch = (
        persisted_prompt_fingerprint
        != current_prompt_fingerprint
    )

    if (
        manifest.get("schema_version")
        != JUDGE_EVALUATION_MANIFEST_SCHEMA_VERSION
        or mismatched_versions
        or manifest.get(
            "judge",
            {},
        ).get("system_prompt") != JUDGE_SYSTEM_PROMPT
        or prompt_fingerprint_mismatch
    ):
        raise ValueError(
            "La evaluación del judge no corresponde a las "
            "versiones vigentes requeridas para continuarla. "
            f"Diferencias de versiones: {mismatched_versions}; "
            "huella efectiva del prompt: "
            f"{persisted_prompt_fingerprint!r} -> "
            f"{current_prompt_fingerprint!r}."
        )

    return manifest


def load_judge_evaluation_progress(
    dataset_id: str,
    judge_eval_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> dict[
    str,
    dict[CriterionId, JudgeCriterionDecision],
]:
    """Carga los criterios completados aún no consolidados por caso."""

    manifest = load_judge_evaluation_manifest(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )
    progress_path = (
        _judge_evaluation_progress_path(
            dataset_id,
            judge_eval_id,
            results_dir,
        )
    )
    raw_progress = json.loads(
        progress_path.read_text(
            encoding="utf-8",
        )
    )

    if not isinstance(raw_progress, dict):
        raise ValueError(
            "El checkpoint del judge debe ser un objeto JSON."
        )

    unknown_case_ids = (
        set(raw_progress)
        - set(manifest["case_ids"])
    )

    if unknown_case_ids:
        raise ValueError(
            "El checkpoint del judge contiene case_id "
            f"desconocidos: {sorted(unknown_case_ids)}."
        )

    progress = {}

    for case_id, raw_criteria in raw_progress.items():
        if not isinstance(raw_criteria, dict):
            raise ValueError(
                f"El checkpoint de {case_id!r} debe "
                "contener un objeto de criterios."
            )

        unknown_criteria = (
            set(raw_criteria)
            - set(CRITERION_IDS)
        )

        if unknown_criteria:
            raise ValueError(
                f"El checkpoint de {case_id!r} contiene "
                f"criterios desconocidos: "
                f"{sorted(unknown_criteria)}."
            )

        progress[case_id] = {
            criterion_id: (
                JudgeCriterionDecision.model_validate(
                    raw_decision
                )
            )
            for criterion_id, raw_decision
            in raw_criteria.items()
        }

    return progress


def save_judge_criterion_progress(
    dataset_id: str,
    judge_eval_id: str,
    case_id: str,
    criterion_id: CriterionId,
    decision: JudgeCriterionDecision,
    *,
    results_dir: Path = RESULTS_DIR,
) -> None:
    """Checkpointa atómicamente un criterio ya evaluado."""

    manifest = require_current_judge_evaluation(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )

    if case_id not in set(
        manifest["case_ids"]
    ):
        raise ValueError(
            f"El case_id {case_id!r} no pertenece "
            f"al split {manifest['split']!r} de esta evaluación."
        )

    cases = load_qualitative_cases(
        dataset_id,
        results_dir=results_dir,
    )
    cases_by_id = {
        case.case_id: case
        for case in cases
    }
    case = cases_by_id.get(
        case_id
    )

    if case is None:
        raise ValueError(
            f"El case_id {case_id!r} no pertenece "
            f"al dataset {dataset_id!r}."
        )

    if not case.criteria_applicability[
        criterion_id
    ].applicable:
        raise ValueError(
            f"El criterio {criterion_id} no aplica "
            f"al caso {case_id!r}."
        )

    presentation = build_case_presentation(
        case
    )
    invalid_refs = (
        set(decision.evidence_refs)
        - set(presentation.evidence_refs)
    )

    if invalid_refs:
        raise ValueError(
            f"El criterio {criterion_id} contiene referencias "
            "de evidencia inexistentes: "
            f"{sorted(invalid_refs)}."
        )

    progress = load_judge_evaluation_progress(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )
    case_progress = progress.setdefault(
        case_id,
        {},
    )

    if criterion_id in case_progress:
        raise FileExistsError(
            f"Ya existe un checkpoint para "
            f"{case_id!r} / {criterion_id}."
        )

    case_progress[criterion_id] = decision

    progress_path = (
        _judge_evaluation_progress_path(
            dataset_id,
            judge_eval_id,
            results_dir,
        )
    )
    _write_json_atomic(
        progress_path,
        {
            progress_case_id: {
                progress_criterion_id: (
                    progress_decision.model_dump(
                        mode="json"
                    )
                )
                for (
                    progress_criterion_id,
                    progress_decision,
                ) in criteria.items()
            }
            for progress_case_id, criteria
            in progress.items()
        },
    )


def clear_judge_case_progress(
    dataset_id: str,
    judge_eval_id: str,
    case_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> None:
    """Elimina el checkpoint de un caso ya consolidado."""

    progress = load_judge_evaluation_progress(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )

    if case_id not in progress:
        return

    del progress[case_id]

    progress_path = (
        _judge_evaluation_progress_path(
            dataset_id,
            judge_eval_id,
            results_dir,
        )
    )
    _write_json_atomic(
        progress_path,
        {
            progress_case_id: {
                criterion_id: decision.model_dump(
                    mode="json"
                )
                for criterion_id, decision
                in criteria.items()
            }
            for progress_case_id, criteria
            in progress.items()
        },
    )


def load_judge_trace(
    dataset_id: str,
    judge_eval_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> list[dict[str, Any]]:
    """Carga en orden las llamadas al LLM realizadas por el judge."""

    load_judge_evaluation_manifest(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )
    trace_path = (
        _judge_evaluation_trace_path(
            dataset_id,
            judge_eval_id,
            results_dir,
        )
    )

    return _load_jsonl(
        trace_path
    )


def append_judge_trace_event(
    dataset_id: str,
    judge_eval_id: str,
    case_id: str,
    criterion_id: CriterionId,
    event: dict[str, Any],
    *,
    results_dir: Path = RESULTS_DIR,
) -> None:
    """Persiste inmediatamente un evento de inferencia del judge."""

    manifest = require_current_judge_evaluation(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )

    if case_id not in set(
        manifest["case_ids"]
    ):
        raise ValueError(
            f"El case_id {case_id!r} no pertenece "
            f"al split {manifest['split']!r} de esta evaluación."
        )

    if criterion_id not in CRITERION_IDS:
        raise ValueError(
            f"Criterio desconocido: {criterion_id!r}."
        )

    serialized_event = (
        _serialize_trace_event(
            event
        )
    )
    trace_record = {
        "case_id": case_id,
        "criterion_id": criterion_id,
        **serialized_event,
    }

    trace_path = (
        _judge_evaluation_trace_path(
            dataset_id,
            judge_eval_id,
            results_dir,
        )
    )
    existing_trace = load_judge_trace(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )

    _write_jsonl_atomic(
        trace_path,
        [
            *existing_trace,
            trace_record,
        ],
    )


def load_judge_case_predictions(
    dataset_id: str,
    judge_eval_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> list[JudgeCasePrediction]:
    """Carga las predicciones persistidas de una evaluación del judge."""

    load_judge_evaluation_manifest(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )

    _, _, predictions_path = (
        _judge_evaluation_paths(
            dataset_id,
            judge_eval_id,
            results_dir,
        )
    )

    predictions = [
        JudgeCasePrediction.model_validate(
            data
        )
        for data in _load_jsonl(
            predictions_path
        )
    ]

    case_ids = [
        prediction.case_id
        for prediction in predictions
    ]

    if len(case_ids) != len(set(case_ids)):
        raise ValueError(
            "La evaluación del judge contiene case_id duplicados."
        )

    return predictions


def save_judge_case_prediction(
    dataset_id: str,
    judge_eval_id: str,
    prediction: JudgeCasePrediction,
    *,
    results_dir: Path = RESULTS_DIR,
) -> None:
    """Valida y agrega una predicción sin sobrescribir casos previos."""

    manifest = require_current_judge_evaluation(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )

    if prediction.case_id not in set(
        manifest["case_ids"]
    ):
        raise ValueError(
            f"El case_id {prediction.case_id!r} no pertenece "
            f"al split {manifest['split']!r} de esta evaluación."
        )

    cases = load_qualitative_cases(
        dataset_id,
        results_dir=results_dir,
    )
    cases_by_id = {
        case.case_id: case
        for case in cases
    }

    case = cases_by_id.get(
        prediction.case_id
    )

    if case is None:
        raise ValueError(
            f"El case_id {prediction.case_id!r} no pertenece "
            f"al dataset {dataset_id!r}."
        )

    canonical_prediction = (
        build_judge_case_prediction(
            case,
            dict(prediction.criteria),
        )
    )

    if prediction != canonical_prediction:
        raise ValueError(
            "La predicción no corresponde a las versiones "
            "vigentes del caso, la presentación, la rúbrica "
            "y el prompt del judge."
        )

    existing_predictions = (
        load_judge_case_predictions(
            dataset_id,
            judge_eval_id,
            results_dir=results_dir,
        )
    )

    if any(
        existing.case_id == prediction.case_id
        for existing in existing_predictions
    ):
        raise FileExistsError(
            f"Ya existe una predicción para "
            f"{prediction.case_id!r}."
        )

    _, _, predictions_path = (
        _judge_evaluation_paths(
            dataset_id,
            judge_eval_id,
            results_dir,
        )
    )

    persisted_predictions = [
        *existing_predictions,
        prediction,
    ]

    _write_jsonl_atomic(
        predictions_path,
        [
            persisted_prediction.model_dump(
                mode="json"
            )
            for persisted_prediction
            in persisted_predictions
        ],
    )
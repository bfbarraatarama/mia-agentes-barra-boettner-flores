"""Persistencia y trazabilidad de corridas de evaluación M3."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from inspect import Parameter, signature
import json
import os
from pathlib import Path
import subprocess
from tempfile import NamedTemporaryFile
from typing import Any

from eval.agent_configs import AGENT_CONFIGS
from eval.experiment import _resolve_scenario
from eval.trial_configs import TRIAL_CONFIGS
from eval.llm_configs import LLM_CONFIGS, PROVIDERS


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = REPO_ROOT / "eval" / "results"
RUNS_DIR = RESULTS_DIR / "runs"
EVALUATIONS_DIR = RESULTS_DIR / "evaluations"

MANIFEST_SCHEMA_VERSION = 1
EVALUATION_MANIFEST_SCHEMA_VERSION = 1


def _validate_run_id(run_id: str) -> None:
    """Valida un run_id que pueda utilizarse como nombre base de archivo."""

    if not run_id:
        raise ValueError("run_id no puede estar vacío.")

    if (
        run_id in {".", ".."}
        or "/" in run_id
        or "\\" in run_id
    ):
        raise ValueError(
            "run_id no puede contener separadores de ruta."
        )


def _validate_eval_id(eval_id: str) -> None:
    """Valida un eval_id que pueda utilizarse como nombre base de archivo."""

    if not eval_id:
        raise ValueError("eval_id no puede estar vacío.")

    if (
        eval_id in {".", ".."}
        or "/" in eval_id
        or "\\" in eval_id
    ):
        raise ValueError(
            "eval_id no puede contener separadores de ruta."
        )


def _created_at() -> str:
    """Devuelve el instante de creación del manifest en UTC."""

    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _git_output(*args: str) -> str:
    """Ejecuta un comando Git de consulta sobre el repositorio."""

    result = subprocess.run(
        [
            "git",
            "-C",
            str(REPO_ROOT),
            *args,
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    return result.stdout.strip()


def _git_metadata() -> dict[str, Any]:
    """Obtiene metadata de trazabilidad del estado actual del repositorio."""

    return {
        "commit": _git_output("rev-parse", "HEAD"),
        "branch": _git_output(
            "rev-parse",
            "--abbrev-ref",
            "HEAD",
        ),
        "dirty": bool(
            _git_output(
                "status",
                "--porcelain",
            )
        ),
    }


def _effective_llm_config(
    config_name: str,
) -> dict[str, Any]:
    """Resuelve la configuración efectiva relevante de un LLM."""

    config = dict(LLM_CONFIGS[config_name])
    provider_name = config["provider"]
    provider_class = PROVIDERS[provider_name]

    chat_parameters = signature(provider_class.chat).parameters

    temperature = chat_parameters["temperature"].default
    if temperature is not Parameter.empty:
        config.setdefault("temperature", temperature)

    init_parameters = signature(provider_class.__init__).parameters

    for parameter_name in ("num_ctx", "max_tokens"):
        if parameter_name in config:
            continue

        parameter = init_parameters.get(parameter_name)

        if (
            parameter is not None
            and parameter.default is not Parameter.empty
        ):
            config[parameter_name] = parameter.default

    return config


def build_run_manifest(
    run_id: str,
    run_config: dict[str, Any],
) -> dict[str, Any]:
    """Construye el manifest inmutable de una corrida."""

    _validate_run_id(run_id)

    run = {
        "systems": [
            dict(system)
            for system in run_config["systems"]
        ],
        "trial_configs": list(
            run_config["trial_configs"]
        ),
        "scenarios": list(
            run_config["scenarios"]
        ),
        "trials_per_case": run_config["trials_per_case"],
    }

    agent_config_names = {
        system["agent_config"]
        for system in run["systems"]
    }
    llm_config_names = {
        system["llm_config"]
        for system in run["systems"]
    }

    agent_configs = {
        name: deepcopy(AGENT_CONFIGS[name])
        for name in sorted(agent_config_names)
    }

    llm_configs = {
        name: _effective_llm_config(name)
        for name in sorted(llm_config_names)
    }

    trial_configs = {
        name: deepcopy(TRIAL_CONFIGS[name])
        for name in run["trial_configs"]
    }
    scenario_metadata = {}

    for scenario_spec in run["scenarios"]:
        scenario = _resolve_scenario(scenario_spec)

        scenario_metadata[scenario.id] = {
            "difficulty": scenario.difficulty,
            "goal": deepcopy(scenario.goal),
        }

    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "run_id": run_id,
        "created_at": _created_at(),
        "git": _git_metadata(),
        "run": run,
        "agent_configs": agent_configs,
        "llm_configs": llm_configs,
        "trial_configs": trial_configs,
        "scenario_metadata": scenario_metadata,
    }


def build_evaluation_manifest(
    eval_id: str,
    run_id: str,
    evaluation_config: dict[str, Any],
) -> dict[str, Any]:
    """Construye el manifest inmutable de una evaluación."""

    _validate_eval_id(eval_id)
    _validate_run_id(run_id)

    return {
        "schema_version": EVALUATION_MANIFEST_SCHEMA_VERSION,
        "eval_id": eval_id,
        "run_id": run_id,
        "created_at": _created_at(),
        "git": _git_metadata(),
        "evaluation": deepcopy(evaluation_config),
    }


def _run_paths(
    run_id: str,
    results_dir: Path,
) -> tuple[Path, Path]:
    """Devuelve las rutas del manifest y los resultados de una corrida."""

    _validate_run_id(run_id)

    return (
        results_dir / f"{run_id}.manifest.json",
        results_dir / f"{run_id}.json",
    )


def _evaluation_paths(
    eval_id: str,
    results_dir: Path,
) -> tuple[Path, Path]:
    """Devuelve las rutas del manifest y los resultados de una evaluación."""

    _validate_eval_id(eval_id)

    return (
        results_dir / f"{eval_id}.manifest.json",
        results_dir / f"{eval_id}.json",
    )


def _write_json_new(
    output_path: Path,
    data: dict[str, Any],
) -> None:
    """Crea un JSON nuevo sin permitir sobrescrituras."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        output_file = output_path.open(
            "x",
            encoding="utf-8",
        )
    except FileExistsError:
        raise

    try:
        with output_file:
            json.dump(
                data,
                output_file,
                indent=2,
                ensure_ascii=False,
            )
            output_file.write("\n")
    except BaseException:
        output_path.unlink(missing_ok=True)
        raise

def _read_json(input_path: Path) -> dict[str, Any]:
    """Lee un artefacto JSON persistido."""

    return json.loads(
        input_path.read_text(encoding="utf-8")
    )


def _write_json_atomic(
    output_path: Path,
    data: dict[str, Any],
) -> None:
    """Reemplaza un JSON solo después de escribirlo completamente."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

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
            temporary_path = Path(output_file.name)

            json.dump(
                data,
                output_file,
                indent=2,
                ensure_ascii=False,
            )
            output_file.write("\n")

        os.replace(
            temporary_path,
            output_path,
        )

    except BaseException:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

        raise


def load_run_manifest(
    run_id: str,
    *,
    results_dir: Path = RUNS_DIR,
) -> dict[str, Any]:
    """Carga el manifest persistido de una corrida."""

    manifest_path, _ = _run_paths(
        run_id,
        results_dir,
    )

    return _read_json(manifest_path)


def load_run_results(
    run_id: str,
    *,
    results_dir: Path = RUNS_DIR,
) -> dict[str, Any]:
    """Carga los resultados persistidos de una corrida."""

    _, results_path = _run_paths(
        run_id,
        results_dir,
    )

    return _read_json(results_path)


def require_existing_run(
    run_id: str,
    *,
    results_dir: Path = RUNS_DIR,
) -> None:
    """Exige que existan ambos artefactos de una corrida."""

    manifest_path, results_path = _run_paths(
        run_id,
        results_dir,
    )

    missing_paths = [
        path
        for path in (manifest_path, results_path)
        if not path.exists()
    ]

    if missing_paths:
        missing_names = ", ".join(
            path.name
            for path in missing_paths
        )
        raise FileNotFoundError(
            f"No se puede reanudar el run_id {run_id!r}: "
            f"faltan {missing_names}."
        )


def write_run_results(
    run_id: str,
    data: dict[str, Any],
    *,
    results_dir: Path = RUNS_DIR,
) -> None:
    """Actualiza atómicamente los resultados de una corrida."""

    _, results_path = _run_paths(
        run_id,
        results_dir,
    )

    _write_json_atomic(
        results_path,
        data,
    )


def initialize_run(
    run_id: str,
    run_config: dict[str, Any],
    *,
    results_dir: Path = RUNS_DIR,
) -> None:
    """Inicializa los artefactos persistentes de una corrida nueva."""

    manifest_path, results_path = _run_paths(
        run_id,
        results_dir,
    )

    existing_paths = [
        path
        for path in (manifest_path, results_path)
        if path.exists()
    ]

    if existing_paths:
        existing_names = ", ".join(
            path.name
            for path in existing_paths
        )
        raise FileExistsError(
            f"El run_id {run_id!r} ya existe: {existing_names}."
        )

    manifest = build_run_manifest(
        run_id=run_id,
        run_config=run_config,
    )

    _write_json_new(
        manifest_path,
        manifest,
    )

    _write_json_new(
        results_path,
        {
            "results": [],
        },
    )


def load_evaluation_manifest(
    eval_id: str,
    *,
    results_dir: Path = EVALUATIONS_DIR,
) -> dict[str, Any]:
    """Carga el manifest de una evaluación persistida."""

    manifest_path, _ = _evaluation_paths(
        eval_id,
        results_dir,
    )
    return _read_json(manifest_path)


def load_evaluation_results(
    eval_id: str,
    *,
    results_dir: Path = EVALUATIONS_DIR,
) -> dict[str, Any]:
    """Carga los resultados de una evaluación persistida."""

    _, results_path = _evaluation_paths(
        eval_id,
        results_dir,
    )
    return _read_json(results_path)


def write_evaluation_results(
    eval_id: str,
    evaluation_result: dict[str, Any],
    *,
    results_dir: Path = EVALUATIONS_DIR,
) -> None:
    """Actualiza atómicamente los resultados de una evaluación."""

    _, results_path = _evaluation_paths(
        eval_id,
        results_dir,
    )
    _write_json_atomic(
        results_path,
        evaluation_result,
    )


def initialize_evaluation(
    eval_id: str,
    run_id: str,
    evaluation_config: dict[str, Any],
    *,
    results_dir: Path = EVALUATIONS_DIR,
) -> None:
    """Inicializa los artefactos persistentes de una evaluación nueva."""

    manifest_path, results_path = _evaluation_paths(
        eval_id,
        results_dir,
    )

    existing_paths = [
        path
        for path in (manifest_path, results_path)
        if path.exists()
    ]

    if existing_paths:
        existing_names = ", ".join(
            path.name
            for path in existing_paths
        )
        raise FileExistsError(
            f"El eval_id {eval_id!r} ya existe: {existing_names}."
        )

    manifest = build_evaluation_manifest(
        eval_id=eval_id,
        run_id=run_id,
        evaluation_config=evaluation_config,
    )

    _write_json_new(
        manifest_path,
        manifest,
    )

    _write_json_new(
        results_path,
        {
            "eval_id": eval_id,
            "run_id": run_id,
            "results": [],
            "analyses": {},
        },
    )
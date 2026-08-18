import json

import pytest

from eval import evaluation, persistence, run_execution
from eval.agent_configs import AGENT_CONFIGS
from eval.run_configs import M3_RUN_CONFIG
from eval.trial_configs import TRIAL_CONFIGS


def test_build_run_manifest_contains_reproducible_run_spec(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """El manifest conserva el plan y sus configuraciones efectivas."""

    monkeypatch.setattr(
        persistence,
        "_created_at",
        lambda: "2026-08-17T14:00:00+00:00",
    )
    monkeypatch.setattr(
        persistence,
        "_git_metadata",
        lambda: {
            "commit": "abc123",
            "branch": "m3/evaluation-persistence",
            "dirty": False,
        },
    )

    manifest = persistence.build_run_manifest(
        run_id="test-run",
        run_config=M3_RUN_CONFIG,
    )

    assert manifest["schema_version"] == 1
    assert manifest["run_id"] == "test-run"
    assert manifest["created_at"] == "2026-08-17T14:00:00+00:00"

    assert manifest["git"] == {
        "commit": "abc123",
        "branch": "m3/evaluation-persistence",
        "dirty": False,
    }

    assert manifest["run"] == {
        "systems": M3_RUN_CONFIG["systems"],
        "trial_configs": M3_RUN_CONFIG["trial_configs"],
        "scenarios": M3_RUN_CONFIG["scenarios"],
        "trials_per_case": M3_RUN_CONFIG["trials_per_case"],
    }
    assert "metrics" not in manifest["run"]

    assert manifest["agent_configs"] == {
        "minimal": AGENT_CONFIGS["minimal"],
    }

    assert manifest["llm_configs"]["llama3.1"] == {
        "provider": "ollama",
        "model": "llama3.1",
        "num_ctx": 32768,
        "temperature": 0.2,
    }

    assert manifest["llm_configs"]["nova-lite"] == {
        "provider": "bedrock",
        "model": "amazon.nova-lite-v1:0",
        "region": "us-west-2",
        "temperature": 0.2,
        "max_tokens": 4096,
    }

    assert manifest["trial_configs"] == {
        "single_attempt": TRIAL_CONFIGS["single_attempt"],
    }

    assert manifest["scenario_metadata"] == {
        "study-with-key": {
            "difficulty": "easy",
            "goal": {
                "type": "item_open",
                "item": "puerta_principal",
            },
        },
    }

    json.dumps(
        manifest,
        ensure_ascii=False,
    )


def test_build_run_manifest_rejects_empty_run_id() -> None:
    """Una corrida debe tener un run_id explícito."""

    with pytest.raises(
        ValueError,
        match="run_id no puede estar vacío",
    ):
        persistence.build_run_manifest(
            run_id="",
            run_config=M3_RUN_CONFIG,
        )


def test_initialize_run_creates_manifest_and_empty_results(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Una corrida nueva crea sus dos artefactos sin ejecutar trials."""

    monkeypatch.setattr(
        persistence,
        "_created_at",
        lambda: "2026-08-17T14:00:00+00:00",
    )
    monkeypatch.setattr(
        persistence,
        "_git_metadata",
        lambda: {
            "commit": "abc123",
            "branch": "m3/evaluation-persistence",
            "dirty": False,
        },
    )

    persistence.initialize_run(
        run_id="test-run",
        run_config=M3_RUN_CONFIG,
        results_dir=tmp_path,
    )

    manifest_path = tmp_path / "test-run.manifest.json"
    results_path = tmp_path / "test-run.json"

    assert manifest_path.is_file()
    assert results_path.is_file()

    manifest = json.loads(
        manifest_path.read_text(encoding="utf-8")
    )
    results = json.loads(
        results_path.read_text(encoding="utf-8")
    )

    assert manifest["run_id"] == "test-run"
    assert results == {
        "results": [],
    }


@pytest.mark.parametrize(
    "existing_name",
    [
        "test-run.manifest.json",
        "test-run.json",
    ],
)
def test_initialize_run_rejects_existing_run_id(
    tmp_path,
    existing_name: str,
) -> None:
    """Un run_id existente nunca se reutiliza en una corrida nueva."""

    existing_path = tmp_path / existing_name
    existing_path.write_text(
        "contenido existente",
        encoding="utf-8",
    )

    with pytest.raises(
        FileExistsError,
        match="El run_id 'test-run' ya existe",
    ):
        persistence.initialize_run(
            run_id="test-run",
            run_config=M3_RUN_CONFIG,
            results_dir=tmp_path,
        )

    assert existing_path.read_text(
        encoding="utf-8"
    ) == "contenido existente"

    assert not (
        tmp_path / (
            "test-run.json"
            if existing_name.endswith(".manifest.json")
            else "test-run.manifest.json"
        )
    ).exists()


def test_initialize_run_rejects_run_id_with_path_separator(
    tmp_path,
) -> None:
    """El run_id no puede seleccionar rutas fuera del directorio del run."""

    with pytest.raises(
        ValueError,
        match="run_id no puede contener separadores de ruta",
    ):
        persistence.initialize_run(
            run_id="otro/test-run",
            run_config=M3_RUN_CONFIG,
            results_dir=tmp_path,
        )


def test_start_run_persists_completed_trials(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """start_run crea la corrida y persiste sus trials."""

    monkeypatch.setattr(
        persistence,
        "_created_at",
        lambda: "2026-08-17T14:00:00+00:00",
    )
    monkeypatch.setattr(
        persistence,
        "_git_metadata",
        lambda: {
            "commit": "abc123",
            "branch": "m3/evaluation-persistence",
            "dirty": False,
        },
    )

    run_config = {
        **M3_RUN_CONFIG,
        "systems": [
            M3_RUN_CONFIG["systems"][0],
        ],
        "trials_per_case": 2,
    }

    def fake_run_case(**kwargs):
        for trial_index in kwargs["trial_indices"]:
            kwargs["trial_callback"]({
                "trial_index": trial_index,
                "goal_achieved": trial_index == 2,
                "goal_reason": "controlado",
                "attempts": [],
            })

    monkeypatch.setattr(
        run_execution,
        "run_case",
        fake_run_case,
    )

    result = run_execution.start_run(
        run_id="test-run",
        run_config=run_config,
        results_dir=tmp_path,
    )

    manifest_path = tmp_path / "test-run.manifest.json"
    results_path = tmp_path / "test-run.json"

    assert manifest_path.is_file()
    assert results_path.is_file()

    persisted = json.loads(
        results_path.read_text(encoding="utf-8")
    )

    assert result == persisted

    assert len(persisted["results"]) == 1

    assert [
        trial["trial_index"]
        for trial in persisted["results"][0]["trials"]
    ] == [1, 2]


def test_start_run_keeps_completed_trials_after_interruption(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Una interrupción conserva los trials ya persistidos."""

    monkeypatch.setattr(
        persistence,
        "_created_at",
        lambda: "2026-08-17T14:00:00+00:00",
    )
    monkeypatch.setattr(
        persistence,
        "_git_metadata",
        lambda: {
            "commit": "abc123",
            "branch": "m3/evaluation-persistence",
            "dirty": False,
        },
    )

    run_config = {
        **M3_RUN_CONFIG,
        "systems": [
            M3_RUN_CONFIG["systems"][0],
        ],
        "trials_per_case": 2,
    }

    def interrupted_run_case(**kwargs):
        assert kwargs["trial_indices"] == [1, 2]

        kwargs["trial_callback"]({
            "trial_index": 1,
            "goal_achieved": False,
            "goal_reason": "controlado",
            "attempts": [],
        })

        raise RuntimeError("interrupción controlada")

    monkeypatch.setattr(
        run_execution,
        "run_case",
        interrupted_run_case,
    )
    with pytest.raises(
        RuntimeError,
        match="interrupción controlada",
    ):
        run_execution.start_run(
            run_id="test-run",
            run_config=run_config,
            results_dir=tmp_path,
        )

    persisted = json.loads(
        (
            tmp_path / "test-run.json"
        ).read_text(encoding="utf-8")
    )

    assert len(persisted["results"]) == 1

    assert [
        trial["trial_index"]
        for trial in persisted["results"][0]["trials"]
    ] == [1]


def test_resume_run_requires_existing_run(
    tmp_path,
) -> None:
    """resume_run rechaza una corrida inexistente."""

    with pytest.raises(
        FileNotFoundError,
        match="No se puede reanudar el run_id 'missing-run'",
    ):
        run_execution.resume_run(
            run_id="missing-run",
            results_dir=tmp_path,
        )


@pytest.mark.parametrize(
    "existing_name",
    [
        "test-run.manifest.json",
        "test-run.json",
    ],
)
def test_resume_run_rejects_incomplete_run_artifacts(
    tmp_path,
    existing_name: str,
) -> None:
    """resume_run exige manifest y resultados."""

    (tmp_path / existing_name).write_text(
        "{}",
        encoding="utf-8",
    )

    with pytest.raises(
        FileNotFoundError,
        match="No se puede reanudar el run_id 'test-run'",
    ):
        run_execution.resume_run(
            run_id="test-run",
            results_dir=tmp_path,
        )


def test_resume_run_uses_common_execution_engine(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """resume_run delega la ejecución al motor común."""

    (tmp_path / "test-run.manifest.json").write_text(
        "{}",
        encoding="utf-8",
    )
    (tmp_path / "test-run.json").write_text(
        '{"results": []}',
        encoding="utf-8",
    )

    calls = []

    def fake_execute_pending_trials(
        run_id,
        *,
        results_dir,
        progress_callback=None,
    ):
        calls.append(
            {
                "run_id": run_id,
                "results_dir": results_dir,
                "progress_callback": progress_callback,
            }
        )
        return {
            "results": [],
        }

    monkeypatch.setattr(
        run_execution,
        "_execute_pending_trials",
        fake_execute_pending_trials,
    )

    result = run_execution.resume_run(
        run_id="test-run",
        results_dir=tmp_path,
    )
    assert result == {
        "results": [],
    }

    assert calls == [
        {
            "run_id": "test-run",
            "results_dir": tmp_path,
            "progress_callback": None,
        },
    ]


def test_create_evaluation_persists_definition_for_complete_run(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Una evaluación nueva referencia un run completo sin duplicarlo."""

    runs_dir = tmp_path / "runs"
    evaluations_dir = tmp_path / "evaluations"
    runs_dir.mkdir()

    run_manifest = {
        "run": {
            "systems": [
                {
                    "agent_config": "agent-a",
                    "llm_config": "llm-a",
                },
            ],
            "trial_configs": [
                "trial-a",
            ],
            "scenarios": [
                "scenario-a",
            ],
            "trials_per_case": 1,
        },
        "agent_configs": {},
        "llm_configs": {},
        "trial_configs": {},
    }

    run_result = {
        "results": [
            {
                "agent_config": "agent-a",
                "llm_config": "llm-a",
                "trial_config": "trial-a",
                "scenario": "scenario-a",
                "trials": [
                    {
                        "trial_index": 1,
                    },
                ],
            },
        ],
    }

    (
        runs_dir / "test-run.manifest.json"
    ).write_text(
        json.dumps(run_manifest),
        encoding="utf-8",
    )
    (
        runs_dir / "test-run.json"
    ).write_text(
        json.dumps(run_result),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        persistence,
        "_created_at",
        lambda: "2026-08-17T14:00:00+00:00",
    )
    monkeypatch.setattr(
        persistence,
        "_git_metadata",
        lambda: {
            "commit": "abc123",
            "branch": "m3/evaluation-persistence",
            "dirty": False,
        },
    )

    evaluation_config = {
        "metrics": [
            "success_rate",
        ],
    }

    evaluation.create_evaluation(
        eval_id="test-eval",
        run_id="test-run",
        evaluation_config=evaluation_config,
        runs_dir=runs_dir,
        evaluations_dir=evaluations_dir,
    )

    manifest = json.loads(
        (
            evaluations_dir / "test-eval.manifest.json"
        ).read_text(encoding="utf-8")
    )
    results = json.loads(
        (
            evaluations_dir / "test-eval.json"
        ).read_text(encoding="utf-8")
    )

    assert manifest == {
        "schema_version": 1,
        "eval_id": "test-eval",
        "run_id": "test-run",
        "created_at": "2026-08-17T14:00:00+00:00",
        "git": {
            "commit": "abc123",
            "branch": "m3/evaluation-persistence",
            "dirty": False,
        },
        "evaluation": evaluation_config,
    }

    assert results == {
        "eval_id": "test-eval",
        "run_id": "test-run",
        "results": [],
        "analyses": {},
    }


def test_create_evaluation_rejects_incomplete_run(
    tmp_path,
) -> None:
    """Una evaluación formal no se crea sobre evidencia incompleta."""

    runs_dir = tmp_path / "runs"
    evaluations_dir = tmp_path / "evaluations"
    runs_dir.mkdir()

    run_manifest = {
        "run": {
            "systems": [
                {
                    "agent_config": "agent-a",
                    "llm_config": "llm-a",
                },
            ],
            "trial_configs": [
                "trial-a",
            ],
            "scenarios": [
                "scenario-a",
            ],
            "trials_per_case": 1,
        },
        "agent_configs": {},
        "llm_configs": {},
        "trial_configs": {},
    }

    (
        runs_dir / "test-run.manifest.json"
    ).write_text(
        json.dumps(run_manifest),
        encoding="utf-8",
    )
    (
        runs_dir / "test-run.json"
    ).write_text(
        json.dumps({"results": []}),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="run_id 'test-run' no está completo",
    ):
        evaluation.create_evaluation(
            eval_id="test-eval",
            run_id="test-run",
            evaluation_config={
                "metrics": [
                    "success_rate",
                ],
            },
            runs_dir=runs_dir,
            evaluations_dir=evaluations_dir,
        )

    assert not evaluations_dir.exists()


@pytest.mark.parametrize(
    "existing_name",
    [
        "test-eval.manifest.json",
        "test-eval.json",
    ],
)
def test_initialize_evaluation_rejects_existing_eval_id(
    tmp_path,
    existing_name: str,
) -> None:
    """Un eval_id existente nunca se reutiliza."""

    existing_path = tmp_path / existing_name
    existing_path.write_text(
        "contenido existente",
        encoding="utf-8",
    )

    with pytest.raises(
        FileExistsError,
        match="El eval_id 'test-eval' ya existe",
    ):
        persistence.initialize_evaluation(
            eval_id="test-eval",
            run_id="test-run",
            evaluation_config={
                "metrics": [
                    "success_rate",
                ],
            },
            results_dir=tmp_path,
        )

    assert existing_path.read_text(
        encoding="utf-8"
    ) == "contenido existente"


def test_start_evaluation_computes_and_persists_metrics(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """La evaluación calcula métricas sin duplicar la evidencia del run."""

    runs_dir = tmp_path / "runs"
    evaluations_dir = tmp_path / "evaluations"
    runs_dir.mkdir()

    run_manifest = {
        "run": {
            "systems": [
                {
                    "agent_config": "agent-a",
                    "llm_config": "llm-a",
                },
            ],
            "trial_configs": [
                "trial-a",
            ],
            "scenarios": [
                "scenario-a",
            ],
            "trials_per_case": 2,
        },
        "agent_configs": {},
        "llm_configs": {},
        "trial_configs": {},
    }

    run_result = {
        "results": [
            {
                "agent_config": "agent-a",
                "llm_config": "llm-a",
                "trial_config": "trial-a",
                "scenario": "scenario-a",
                "trials": [
                    {
                        "trial_index": 1,
                        "goal_achieved": True,
                    },
                    {
                        "trial_index": 2,
                        "goal_achieved": False,
                    },
                ],
            },
        ],
    }

    (
        runs_dir / "test-run.manifest.json"
    ).write_text(
        json.dumps(run_manifest),
        encoding="utf-8",
    )
    (
        runs_dir / "test-run.json"
    ).write_text(
        json.dumps(run_result),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        persistence,
        "_created_at",
        lambda: "2026-08-17T14:00:00+00:00",
    )
    monkeypatch.setattr(
        persistence,
        "_git_metadata",
        lambda: {
            "commit": "abc123",
            "branch": "m3/evaluation-persistence",
            "dirty": False,
        },
    )

    result = evaluation.start_evaluation(
        eval_id="test-eval",
        run_id="test-run",
        evaluation_config={
            "metrics": [
                "success_rate",
            ],
        },
        runs_dir=runs_dir,
        evaluations_dir=evaluations_dir,
    )

    assert result == {
        "eval_id": "test-eval",
        "run_id": "test-run",
        "results": [
            {
                "agent_config": "agent-a",
                "llm_config": "llm-a",
                "trial_config": "trial-a",
                "scenario": "scenario-a",
                "metrics": {
                    "success_rate": 0.5,
                },
            },
        ],
        "analyses": {},
    }

    persisted = persistence.load_evaluation_results(
        "test-eval",
        results_dir=evaluations_dir,
    )

    assert persisted == result

    assert "trials" not in persisted["results"][0]
    assert "attempts" not in persisted["results"][0]
    assert "trace" not in persisted["results"][0]


def test_start_evaluation_computes_and_persists_error_analysis(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Una evaluación puede derivar análisis del run completo."""

    runs_dir = tmp_path / "runs"
    evaluations_dir = tmp_path / "evaluations"
    runs_dir.mkdir()

    run_manifest = {
        "run_id": "test-run",
        "run": {
            "systems": [
                {
                    "agent_config": "agent-a",
                    "llm_config": "llm-a",
                },
            ],
            "trial_configs": [
                "trial-a",
            ],
            "scenarios": [
                "scenario-a",
            ],
            "trials_per_case": 1,
        },
        "agent_configs": {},
        "llm_configs": {},
        "trial_configs": {},
        "scenario_metadata": {
            "scenario-a": {
                "difficulty": "test",
                "goal": {},
            },
        },
    }

    run_result = {
        "results": [
            {
                "agent_config": "agent-a",
                "llm_config": "llm-a",
                "trial_config": "trial-a",
                "scenario": "scenario-a",
                "trials": [
                    {
                        "trial_index": 1,
                        "goal_achieved": False,
                        "goal_reason": "incompleto",
                        "attempts": [
                            {
                                "goal_reason": "incompleto",
                                "agent_result": {
                                    "answer": "No pude resolverlo.",
                                    "steps": [],
                                    "error": None,
                                },
                            },
                        ],
                    },
                ],
            },
        ],
    }

    (
        runs_dir / "test-run.manifest.json"
    ).write_text(
        json.dumps(run_manifest),
        encoding="utf-8",
    )
    (
        runs_dir / "test-run.json"
    ).write_text(
        json.dumps(run_result),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        persistence,
        "_created_at",
        lambda: "2026-08-17T14:00:00+00:00",
    )
    monkeypatch.setattr(
        persistence,
        "_git_metadata",
        lambda: {
            "commit": "abc123",
            "branch": "m3/evaluation-persistence",
            "dirty": False,
        },
    )

    result = evaluation.start_evaluation(
        eval_id="test-eval",
        run_id="test-run",
        evaluation_config={
            "metrics": [],
            "analyses": [
                "error_analysis",
            ],
        },
        runs_dir=runs_dir,
        evaluations_dir=evaluations_dir,
    )

    analysis = result["analyses"]["error_analysis"]

    assert analysis["run_id"] == "test-run"
    assert analysis["total_trials"] == 1
    assert analysis["successes"] == 0
    assert analysis["failures"] == 1
    assert analysis["coverage"] == "1/1 trials fallidos clasificados"
    assert analysis["failures_by_mode"] == {
        "gave_up_early": 1,
    }

    persisted = persistence.load_evaluation_results(
        "test-eval",
        results_dir=evaluations_dir,
    )

    assert persisted == result


def test_start_evaluation_rejects_unknown_metric_before_creation(
    tmp_path,
) -> None:
    """Una métrica desconocida no crea artefactos de evaluación."""

    with pytest.raises(
        ValueError,
        match="Métrica de evaluación desconocida: 'missing_metric'",
    ):
        evaluation.start_evaluation(
            eval_id="test-eval",
            run_id="test-run",
            evaluation_config={
                "metrics": [
                    "missing_metric",
                ],
            },
            runs_dir=tmp_path / "runs",
            evaluations_dir=tmp_path / "evaluations",
        )

    assert not (
        tmp_path / "evaluations"
    ).exists()


def test_start_evaluation_rejects_unknown_analysis_before_creation(
    tmp_path,
) -> None:
    """Un análisis desconocido no crea artefactos de evaluación."""

    with pytest.raises(
        ValueError,
        match="Análisis de evaluación desconocido: 'missing_analysis'",
    ):
        evaluation.start_evaluation(
            eval_id="test-eval",
            run_id="test-run",
            evaluation_config={
                "metrics": [],
                "analyses": [
                    "missing_analysis",
                ],
            },
            runs_dir=tmp_path / "runs",
            evaluations_dir=tmp_path / "evaluations",
        )

    assert not (
        tmp_path / "evaluations"
    ).exists()
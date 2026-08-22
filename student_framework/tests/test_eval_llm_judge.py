import html
import json
import pytest
from pydantic import ValidationError

from eval.llm_judge.cases import build_qualitative_case
from eval.llm_judge.models import (
    ActionObservation,
    AttemptTermination,
    CaseSource,
    CriterionApplicability,
    QualitativeAction,
    QualitativeAttempt,
    QualitativeCase,
    QualitativeIteration,
    ToolCallView,
    ActionExecution,
    HumanAnnotation,
    HumanCriterionAnnotation,
)
from eval.llm_judge.persistence import (
    create_qualitative_dataset,
    load_case_sources,
    load_dataset_manifest,
    load_qualitative_cases,
)
from eval.llm_judge.rubric import (
    BOUNDARY_RULES,
    CRITERIA,
    CRITERIA_BY_ID,
    CRITERION_IDS,
    DIMENSION_DESCRIPTION,
    DIMENSION_ID,
    DIMENSION_NAME,
    EVIDENCE_RULES,
    MATERIALITY_RULE,
    Q1_1_GUIDANCE,
    Q1_2_GUIDANCE,
    Q1_4_APPLICABILITY_DESCRIPTION,
    Q1_4_APPLICABILITY_NOTES,
    Q1_4_APPLICABILITY_TRIGGERS,
    Q1_4_CONTINUATION_TRIGGER,
    Q1_4_ERROR_TRIGGER,
    Q1_4_GUIDANCE,
    Q1_4_NO_TRIGGER_REASON,
    Q1_4_REPETITION_TRIGGER,
    RUBRIC_VERSION,
)
from eval.llm_judge.configs.dataset_configs import (
    M3_QUALITATIVE_PILOT_DATASET_CONFIG,
)
from eval.llm_judge.prepare_dataset import (
    prepare_qualitative_dataset,
)
from eval.llm_judge.sampling import (
    RANDOM_STRATIFIED_BY_SCENARIO_METHOD,
    SampledTrial,
    TrialCandidate,
    collect_trial_candidates,
    sample_trials_by_scenario,
)
from eval.llm_judge.annotations import (
    HUMAN_ANNOTATION_SCHEMA_VERSION,
    validate_human_annotation,
    load_human_annotations,
    save_human_annotation,
    create_annotator,
    delete_annotator,
    delete_human_annotation,
    list_annotators,
    update_human_annotation,
)
from eval.llm_judge.presentation import (
    PRESENTATION_VERSION,
    build_case_presentation,
)
from eval.llm_judge.reviewer import (
    load_review_cases,
)
from eval.llm_judge.annotate import (
    _annotation_from_form,
    _load_selected_cases,
    _page_html,
    _selected_case,
    _default_annotator_id,
)

def _qualitative_case() -> QualitativeCase:
    return QualitativeCase(
        schema_version=1,
        case_view_version="trajectory-planning-v1",
        case_id="qc-001",
        task="Abrí la puerta principal.",
        criteria_applicability={
            "Q1.1": CriterionApplicability(applicable=True),
            "Q1.2": CriterionApplicability(applicable=True),
            "Q1.3": CriterionApplicability(applicable=True),
            "Q1.4": CriterionApplicability(
                applicable=False,
                reason="No hubo feedback adverso explícito.",
            ),
        },
        attempts=[
            QualitativeAttempt(
                attempt_index=1,
                user_message="Abrí la puerta principal.",
                iterations=[
                    QualitativeIteration(
                        iteration_index=1,
                        assistant_content=(
                            "<thinking>Primero voy a mirar.</thinking>"
                        ),
                        actions=[
                            QualitativeAction(
                                action_id="a1.i1.action1",
                                proposed_action=ToolCallView(
                                    tool="look",
                                    arguments_raw="{}",
                                    arguments={},
                                ),
                                execution=ActionExecution(
                                    action=ToolCallView(
                                        tool="look",
                                        arguments_raw="{}",
                                        arguments={},
                                    ),
                                    differs_from_proposal=False,
                                    observation=ActionObservation(
                                        content="Ves una llave.",
                                    ),
                                ),
                            ),
                        ],
                    ),
                ],
                termination=AttemptTermination(
                    answer="Respuesta final.",
                ),
            ),
        ],
    )


def _human_annotation() -> HumanAnnotation:
    criterion_annotation = HumanCriterionAnnotation(
        verdict="PASS",
        reason="La trayectoria mantiene una estrategia coherente.",
        evidence_refs=[
            "a1.i1",
        ],
    )

    return HumanAnnotation(
        schema_version=HUMAN_ANNOTATION_SCHEMA_VERSION,
        case_schema_version=1,
        case_view_version="trajectory-planning-v1",
        presentation_version=PRESENTATION_VERSION,
        rubric_version="planning-quality-v1",
        case_id="qc-001",
        annotator_id="annotator-a",
        criteria={
            "Q1.1": criterion_annotation,
            "Q1.2": criterion_annotation,
            "Q1.3": criterion_annotation,
        },
    )


def _attempt(
    *,
    attempt_index: int = 1,
    user_message: str = "Abrí la puerta.",
    trace: list[dict] | None = None,
    steps: list[dict] | None = None,
    answer: str = "Listo.",
    error: str | None = None,
) -> dict:
    return {
        "attempt_index": attempt_index,
        "user_message": user_message,
        "goal_achieved": False,
        "goal_reason": "pendiente",
        "agent_result": {
            "answer": answer,
            "steps": steps or [],
            "error": error,
            "input_tokens": None,
            "output_tokens": None,
        },
        "trace": trace or [],
    }


def _agent_call(
    *,
    content: str | None,
    tool_calls: list[dict] | None = None,
) -> dict:
    return {
        "type": "llm_call",
        "purpose": "agent",
        "retry_index": 0,
        "messages": [],
        "response": {
            "content": content,
            "tool_calls": tool_calls or [],
            "input_tokens": None,
            "output_tokens": None,
            "raw_response": None,
        },
    }


def _sampling_run() -> dict:
    results = []

    for scenario in (
        "study-with-key",
        "office-sequence",
    ):
        for agent_config in (
            "minimal",
            "minimal_tool_repair",
        ):
            results.append({
                "agent_config": agent_config,
                "llm_config": "nova-lite",
                "trial_config": "single_attempt",
                "scenario": scenario,
                "trials": [
                    {
                        "trial_index": trial_index,
                        "goal_achieved": trial_index % 2 == 0,
                        "attempts": [],
                    }
                    for trial_index in range(1, 4)
                ],
            })

        results.append({
            "agent_config": "minimal",
            "llm_config": "llama3.1",
            "trial_config": "single_attempt",
            "scenario": scenario,
            "trials": [
                {
                    "trial_index": trial_index,
                    "goal_achieved": False,
                    "attempts": [],
                }
                for trial_index in range(1, 4)
            ],
        })

    return {
        "results": results,
    }


def _sampled_trials_for_persistence() -> list[SampledTrial]:
    first_trial = {
        "trial_index": 1,
        "goal_achieved": True,
        "goal_reason": "completado",
        "attempts": [
            _attempt(
                user_message="Abrí la puerta.",
                trace=[
                    _agent_call(
                        content="Voy a resolver el desafío.",
                    ),
                ],
                answer="Listo.",
            ),
        ],
    }
    second_trial = {
        "trial_index": 2,
        "goal_achieved": False,
        "goal_reason": "pendiente",
        "attempts": [
            _attempt(
                user_message="Encontrá el documento.",
                trace=[
                    _agent_call(
                        content="Voy a buscarlo.",
                    ),
                ],
                answer="No lo encontré.",
            ),
        ],
    }

    return [
        SampledTrial(
            case_id="qc-001",
            split="dev",
            candidate=TrialCandidate(
                run_id="test-run",
                agent_config="minimal",
                llm_config="nova-lite",
                trial_config="single_attempt",
                scenario="study-with-key",
                trial_index=1,
                trial=first_trial,
            ),
        ),
        SampledTrial(
            case_id="qc-002",
            split="holdout",
            candidate=TrialCandidate(
                run_id="test-run",
                agent_config="minimal_tool_repair",
                llm_config="nova-lite",
                trial_config="single_attempt",
                scenario="office-sequence",
                trial_index=2,
                trial=second_trial,
            ),
        ),
    ]


def _dataset_config_for_persistence() -> dict:
    return {
        "dataset_id": "test-dataset",
        "run_ids": [
            "test-run",
        ],
        "population": {
            "agent_configs": None,
            "llm_configs": [
                "nova-lite",
            ],
            "trial_configs": [
                "single_attempt",
            ],
            "scenarios": [
                "study-with-key",
                "office-sequence",
            ],
        },
        "sampling": {
            "method": RANDOM_STRATIFIED_BY_SCENARIO_METHOD,
            "seed": 1234,
            "cases_per_scenario": 3,
            "dev_per_scenario": 2,
        },
    }


def test_llm_judge_rubric_defines_planning_quality_criteria() -> None:
    assert RUBRIC_VERSION == "planning-quality-v1"
    assert DIMENSION_ID == "Q1"
    assert CRITERION_IDS == (
        "Q1.1",
        "Q1.2",
        "Q1.3",
        "Q1.4",
    )
    assert len(CRITERIA) == 4
    assert set(CRITERIA_BY_ID) == set(CRITERION_IDS)
    assert CRITERIA_BY_ID["Q1.4"].applicability == "conditional"

    assert CRITERIA_BY_ID["Q1.1"].guidance == Q1_1_GUIDANCE
    assert CRITERIA_BY_ID["Q1.2"].guidance == Q1_2_GUIDANCE
    assert CRITERIA_BY_ID["Q1.3"].guidance == ()
    assert (
        CRITERIA_BY_ID["Q1.4"].guidance
        == Q1_4_GUIDANCE
    )
    assert (
        CRITERIA_BY_ID["Q1.4"].applicability_description
        == Q1_4_APPLICABILITY_DESCRIPTION
    )
    assert (
        CRITERIA_BY_ID["Q1.4"].applicability_triggers
        == Q1_4_APPLICABILITY_TRIGGERS
    )
    assert (
        CRITERIA_BY_ID["Q1.4"].applicability_notes
        == Q1_4_APPLICABILITY_NOTES
    )


def test_qualitative_case_preserves_blind_normalized_evidence() -> None:
    case = _qualitative_case()

    serialized = case.model_dump(mode="json")

    assert serialized["case_id"] == "qc-001"
    assert serialized["attempts"][0]["iterations"][0][
        "assistant_content"
    ] == "<thinking>Primero voy a mirar.</thinking>"
    assert serialized["attempts"][0]["iterations"][0]["actions"][0] == {
        "action_id": "a1.i1.action1",
        "proposed_action": {
            "tool": "look",
            "arguments_raw": "{}",
            "arguments": {},
        },
        "execution": {
            "action": {
                "tool": "look",
                "arguments_raw": "{}",
                "arguments": {},
            },
            "differs_from_proposal": False,
            "observation": {
                "content": "Ves una llave.",
                "error": None,
                "is_error": False,
            },
        },
    }
    assert "source" not in serialized
    assert "goal_achieved" not in serialized
    assert "goal_reason" not in serialized


def test_qualitative_case_requires_all_criteria_applicability() -> None:
    case_data = _qualitative_case().model_dump()
    del case_data["criteria_applicability"]["Q1.4"]

    with pytest.raises(
        ValidationError,
        match="criteria_applicability debe definir exactamente",
    ):
        QualitativeCase.model_validate(case_data)


def test_case_source_keeps_experimental_metadata_separate() -> None:
    source = CaseSource(
        case_id="qc-001",
        run_id="test-run",
        agent_config="minimal_tool_repair",
        llm_config="nova-lite",
        trial_config="single_attempt",
        scenario="office-sequence",
        trial_index=4,
        split="dev",
    )

    assert source.model_dump() == {
        "case_id": "qc-001",
        "run_id": "test-run",
        "agent_config": "minimal_tool_repair",
        "llm_config": "nova-lite",
        "trial_config": "single_attempt",
        "scenario": "office-sequence",
        "trial_index": 4,
        "split": "dev",
    }


def test_qualitative_models_reject_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        ToolCallView(
            tool="look",
            arguments_raw="{}",
            arguments={},
            unexpected=True,
        )


def test_build_qualitative_case_preserves_iteration_boundaries() -> None:
    trace = [
        _agent_call(
            content="Voy a moverme y examinar.",
            tool_calls=[
                {
                    "id": "go-1",
                    "name": "go",
                    "arguments": json.dumps({"direction": "este"}),
                },
                {
                    "id": "look-1",
                    "name": "look",
                    "arguments": "{}",
                },
            ],
        ),
        {
            "type": "tool_execution",
            "retry_index": 0,
            "tool_name": "go",
            "arguments": {"direction": "este"},
            "output": "Llegas al corredor.",
        },
        {
            "type": "tool_execution",
            "retry_index": 0,
            "tool_name": "look",
            "arguments": {},
            "output": "Ves una puerta.",
        },
        _agent_call(content="Terminé."),
    ]
    steps = [
        {
            "tool_name": "go",
            "tool_input": json.dumps({"direction": "este"}),
            "tool_output": "Llegas al corredor.",
            "error": None,
        },
        {
            "tool_name": "look",
            "tool_input": "{}",
            "tool_output": "Ves una puerta.",
            "error": None,
        },
    ]
    trial = {
        "trial_index": 1,
        "goal_achieved": True,
        "goal_reason": "completado",
        "attempts": [
            _attempt(trace=trace, steps=steps),
        ],
    }

    case = build_qualitative_case(trial, case_id="qc-001")

    assert len(case.attempts[0].iterations) == 2
    assert [
        action.execution.action.tool
        for action in case.attempts[0].iterations[0].actions
    ] == ["go", "look"]
    assert case.attempts[0].iterations[1].assistant_content == "Terminé."
    assert case.attempts[0].iterations[1].actions == []


def test_build_qualitative_case_distinguishes_repaired_action() -> None:
    original_arguments = json.dumps({"obj": "puerta"})
    repaired_arguments = json.dumps({"target": "puerta"})
    trace = [
        _agent_call(
            content="Voy a examinar la puerta.",
            tool_calls=[
                {
                    "id": "examine-1",
                    "name": "examine",
                    "arguments": original_arguments,
                },
            ],
        ),
        {
            "type": "llm_call",
            "purpose": "tool_call_repair",
            "retry_index": 0,
            "messages": [],
            "response": {
                "content": None,
                "tool_calls": [
                    {
                        "id": "examine-2",
                        "name": "examine",
                        "arguments": repaired_arguments,
                    },
                ],
            },
        },
        {
            "type": "tool_execution",
            "retry_index": 0,
            "tool_name": "examine",
            "arguments": {"target": "puerta"},
            "output": "La puerta está cerrada.",
        },
        _agent_call(content="Listo."),
    ]
    steps = [
        {
            "tool_name": "examine",
            "tool_input": repaired_arguments,
            "tool_output": "La puerta está cerrada.",
            "error": None,
        },
    ]
    trial = {
        "trial_index": 1,
        "goal_achieved": False,
        "goal_reason": "pendiente",
        "attempts": [
            _attempt(trace=trace, steps=steps),
        ],
    }

    case = build_qualitative_case(trial, case_id="qc-002")
    action = case.attempts[0].iterations[0].actions[0]

    assert action.execution is not None
    assert action.proposed_action.arguments == {"obj": "puerta"}
    assert action.execution.action.arguments == {"target": "puerta"}
    assert action.execution.differs_from_proposal is True


def test_build_qualitative_case_marks_world_error_as_q1_4_trigger() -> None:
    trace = [
        _agent_call(
            content=None,
            tool_calls=[
                {
                    "id": "use-1",
                    "name": "use",
                    "arguments": json.dumps({
                        "item": "llave",
                        "target": "puerta",
                    }),
                },
            ],
        ),
        _agent_call(content="No pude abrirla."),
    ]
    steps = [
        {
            "tool_name": "use",
            "tool_input": json.dumps({
                "item": "llave",
                "target": "puerta",
            }),
            "tool_output": "Error: no llevas ningún 'llave'.",
            "error": None,
        },
    ]
    trial = {
        "trial_index": 1,
        "goal_achieved": False,
        "goal_reason": "pendiente",
        "attempts": [
            _attempt(trace=trace, steps=steps),
        ],
    }

    case = build_qualitative_case(trial, case_id="qc-003")
    execution = case.attempts[0].iterations[0].actions[0].execution

    assert execution is not None
    observation = execution.observation

    assert observation.is_error is True
    assert case.criteria_applicability["Q1.4"].applicable is True

    assert (
        case.criteria_applicability["Q1.4"].reason
        == Q1_4_ERROR_TRIGGER
    )


def test_build_qualitative_case_marks_continuation_as_q1_4_trigger() -> None:
    first_attempt = _attempt(
        attempt_index=1,
        user_message="Abrí la puerta.",
        trace=[_agent_call(content="No terminé.")],
        answer="No terminé.",
    )
    second_attempt = _attempt(
        attempt_index=2,
        user_message="El desafío todavía no está completado. Continuá.",
        trace=[_agent_call(content="Ahora sí.")],
        answer="Ahora sí.",
    )
    trial = {
        "trial_index": 1,
        "goal_achieved": True,
        "goal_reason": "completado",
        "attempts": [first_attempt, second_attempt],
    }

    case = build_qualitative_case(trial, case_id="qc-004")

    assert case.task == "Abrí la puerta."
    assert len(case.attempts) == 2
    assert case.criteria_applicability["Q1.4"].applicable is True

    assert (
        case.criteria_applicability["Q1.4"].reason
        == Q1_4_CONTINUATION_TRIGGER
    )


def test_build_qualitative_case_rejects_unmatched_steps() -> None:
    trial = {
        "trial_index": 1,
        "goal_achieved": False,
        "goal_reason": "pendiente",
        "attempts": [
            _attempt(
                trace=[_agent_call(content="Respuesta final.")],
                steps=[
                    {
                        "tool_name": "look",
                        "tool_input": "{}",
                        "tool_output": "Nada.",
                        "error": None,
                    },
                ],
            ),
        ],
    }

    with pytest.raises(
        ValueError,
        match="acciones que no pudieron asociarse",
    ):
        build_qualitative_case(trial, case_id="qc-invalid")


def test_build_qualitative_case_does_not_mark_same_iteration_repetition_as_adaptation() -> None:
    trace = [
        _agent_call(
            content="Voy a mirar dos veces.",
            tool_calls=[
                {
                    "id": "look-1",
                    "name": "look",
                    "arguments": "{}",
                },
                {
                    "id": "look-2",
                    "name": "look",
                    "arguments": "{}",
                },
            ],
        ),
    ]
    steps = [
        {
            "tool_name": "look",
            "tool_input": "{}",
            "tool_output": "No ves nada nuevo.",
            "error": None,
        },
        {
            "tool_name": "look",
            "tool_input": "{}",
            "tool_output": "No ves nada nuevo.",
            "error": None,
        },
    ]
    trial = {
        "trial_index": 1,
        "goal_achieved": False,
        "goal_reason": "pendiente",
        "attempts": [
            _attempt(trace=trace, steps=steps),
        ],
    }

    case = build_qualitative_case(trial, case_id="qc-005")

    assert case.criteria_applicability["Q1.4"].applicable is False

    assert (
        case.criteria_applicability["Q1.4"].reason
        == Q1_4_NO_TRIGGER_REASON
    )


def test_build_qualitative_case_requires_decision_after_error_for_q1_4() -> None:
    trace = [
        _agent_call(
            content=None,
            tool_calls=[
                {
                    "id": "go-1",
                    "name": "go",
                    "arguments": json.dumps({"direction": "norte"}),
                },
            ],
        ),
    ]
    steps = [
        {
            "tool_name": "go",
            "tool_input": json.dumps({"direction": "norte"}),
            "tool_output": "Error: no hay salida 'norte' desde aquí.",
            "error": None,
        },
    ]
    trial = {
        "trial_index": 1,
        "goal_achieved": False,
        "goal_reason": "pendiente",
        "attempts": [
            _attempt(
                trace=trace,
                steps=steps,
                error="Se alcanzó el límite de iteraciones.",
            ),
        ],
    }

    case = build_qualitative_case(trial, case_id="qc-006")

    assert case.criteria_applicability["Q1.4"].applicable is False

    assert (
        case.criteria_applicability["Q1.4"].reason
        == Q1_4_NO_TRIGGER_REASON
    )


def test_build_qualitative_case_compares_tool_arguments_structurally() -> None:
    proposed_arguments = '{"item":"llave","target":"puerta"}'
    effective_arguments = '{"target": "puerta", "item": "llave"}'
    trace = [
        _agent_call(
            content=None,
            tool_calls=[
                {
                    "id": "use-1",
                    "name": "use",
                    "arguments": proposed_arguments,
                },
            ],
        ),
    ]
    steps = [
        {
            "tool_name": "use",
            "tool_input": effective_arguments,
            "tool_output": "Se abre.",
            "error": None,
        },
    ]
    trial = {
        "trial_index": 1,
        "goal_achieved": True,
        "goal_reason": "completado",
        "attempts": [
            _attempt(trace=trace, steps=steps),
        ],
    }

    case = build_qualitative_case(trial, case_id="qc-007")
    action = case.attempts[0].iterations[0].actions[0]

    assert action.execution is not None
    assert action.execution.differs_from_proposal is False


def test_build_qualitative_case_marks_repetition_across_iterations_as_q1_4_trigger() -> None:
    trace = [
        _agent_call(
            content=None,
            tool_calls=[
                {
                    "id": "look-1",
                    "name": "look",
                    "arguments": "{}",
                },
            ],
        ),
        _agent_call(
            content=None,
            tool_calls=[
                {
                    "id": "look-2",
                    "name": "look",
                    "arguments": "{}",
                },
            ],
        ),
    ]
    steps = [
        {
            "tool_name": "look",
            "tool_input": "{}",
            "tool_output": "No ves nada nuevo.",
            "error": None,
        },
        {
            "tool_name": "look",
            "tool_input": "{}",
            "tool_output": "No ves nada nuevo.",
            "error": None,
        },
    ]
    trial = {
        "trial_index": 1,
        "goal_achieved": False,
        "goal_reason": "pendiente",
        "attempts": [
            _attempt(trace=trace, steps=steps),
        ],
    }

    case = build_qualitative_case(trial, case_id="qc-008")

    assert case.criteria_applicability["Q1.4"].applicable is True

    assert (
        case.criteria_applicability["Q1.4"].reason
        == Q1_4_REPETITION_TRIGGER
    )


def test_build_qualitative_case_preserves_unexecuted_terminal_actions() -> None:
    trace = [
        _agent_call(
            content="Voy a mirar.",
            tool_calls=[
                {
                    "id": "look-1",
                    "name": "look",
                    "arguments": "{}",
                },
            ],
        ),
        _agent_call(
            content="Voy a volver y usar la llave.",
            tool_calls=[
                {
                    "id": "go-1",
                    "name": "go",
                    "arguments": json.dumps({"direction": "sur"}),
                },
                {
                    "id": "use-1",
                    "name": "use",
                    "arguments": json.dumps({
                        "item": "llave",
                        "target": "puerta",
                    }),
                },
            ],
        ),
    ]
    steps = [
        {
            "tool_name": "look",
            "tool_input": "{}",
            "tool_output": "Ves una puerta.",
            "error": None,
        },
    ]
    error_message = (
        "Se requirió una herramienta, pero el contexto necesario para "
        "continuar no cabe en max_history_messages=100."
    )
    trial = {
        "trial_index": 1,
        "goal_achieved": False,
        "goal_reason": "pendiente",
        "attempts": [
            _attempt(
                trace=trace,
                steps=steps,
                answer=error_message,
                error=error_message,
            ),
        ],
    }

    case = build_qualitative_case(
        trial,
        case_id="qc-unexecuted",
    )

    first_iteration = case.attempts[0].iterations[0]
    terminal_iteration = case.attempts[0].iterations[1]

    assert first_iteration.actions[0].execution is not None
    assert [
        action.proposed_action.tool
        for action in terminal_iteration.actions
    ] == ["go", "use"]
    assert all(
        action.execution is None
        for action in terminal_iteration.actions
    )
    assert case.attempts[0].termination.error == error_message


def test_build_qualitative_case_rejects_partially_executed_iteration() -> None:
    trace = [
        _agent_call(
            content=None,
            tool_calls=[
                {
                    "id": "go-1",
                    "name": "go",
                    "arguments": json.dumps({"direction": "sur"}),
                },
                {
                    "id": "look-1",
                    "name": "look",
                    "arguments": "{}",
                },
            ],
        ),
    ]
    steps = [
        {
            "tool_name": "go",
            "tool_input": json.dumps({"direction": "sur"}),
            "tool_output": "Llegas al corredor.",
            "error": None,
        },
    ]
    trial = {
        "trial_index": 1,
        "goal_achieved": False,
        "goal_reason": "pendiente",
        "attempts": [
            _attempt(trace=trace, steps=steps),
        ],
    }

    with pytest.raises(
        ValueError,
        match="sólo una parte de las acciones",
    ):
        build_qualitative_case(
            trial,
            case_id="qc-partial",
        )


def test_collect_trial_candidates_filters_population() -> None:
    candidates = collect_trial_candidates(
        {
            "test-run": _sampling_run(),
        },
        llm_configs={"nova-lite"},
    )

    assert len(candidates) == 12
    assert {
        candidate.agent_config
        for candidate in candidates
    } == {
        "minimal",
        "minimal_tool_repair",
    }
    assert {
        candidate.llm_config
        for candidate in candidates
    } == {
        "nova-lite",
    }
    assert {
        candidate.scenario
        for candidate in candidates
    } == {
        "study-with-key",
        "office-sequence",
    }


def test_sample_trials_by_scenario_assigns_dev_and_holdout() -> None:
    candidates = collect_trial_candidates(
        {
            "test-run": _sampling_run(),
        },
        llm_configs={"nova-lite"},
    )

    sampled = sample_trials_by_scenario(
        candidates,
        seed=1234,
        cases_per_scenario=3,
        dev_per_scenario=2,
    )

    assert len(sampled) == 6
    assert len({
        sample.case_id
        for sample in sampled
    }) == 6
    assert len({
        sample.candidate.identity
        for sample in sampled
    }) == 6

    for scenario in (
        "study-with-key",
        "office-sequence",
    ):
        scenario_samples = [
            sample
            for sample in sampled
            if sample.candidate.scenario == scenario
        ]

        assert len(scenario_samples) == 3
        assert sum(
            sample.split == "dev"
            for sample in scenario_samples
        ) == 2
        assert sum(
            sample.split == "holdout"
            for sample in scenario_samples
        ) == 1


def test_sample_trials_by_scenario_is_reproducible() -> None:
    candidates = collect_trial_candidates(
        {
            "test-run": _sampling_run(),
        },
        llm_configs={"nova-lite"},
    )

    first = sample_trials_by_scenario(
        candidates,
        seed=1234,
        cases_per_scenario=3,
        dev_per_scenario=2,
    )
    second = sample_trials_by_scenario(
        list(reversed(candidates)),
        seed=1234,
        cases_per_scenario=3,
        dev_per_scenario=2,
    )

    assert [
        (
            sample.case_id,
            sample.split,
            sample.candidate.identity,
        )
        for sample in first
    ] == [
        (
            sample.case_id,
            sample.split,
            sample.candidate.identity,
        )
        for sample in second
    ]


def test_sample_trials_by_scenario_rejects_insufficient_population() -> None:
    candidates = collect_trial_candidates(
        {
            "test-run": _sampling_run(),
        },
        llm_configs={"nova-lite"},
        agent_configs={"minimal"},
    )

    with pytest.raises(
        ValueError,
        match=(
            "tiene 3 trials elegibles, pero se requieren 4"
        ),
    ):
        sample_trials_by_scenario(
            candidates,
            seed=1234,
            cases_per_scenario=4,
            dev_per_scenario=2,
        )


def test_create_qualitative_dataset_persists_cases_and_sources(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "eval.llm_judge.persistence._created_at",
        lambda: "2026-08-21T20:00:00+00:00",
    )

    dataset_config = _dataset_config_for_persistence()

    manifest = create_qualitative_dataset(
        dataset_config,
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    dataset_dir = tmp_path / "test-dataset"

    assert sorted(
        path.name
        for path in dataset_dir.iterdir()
    ) == [
        "case_sources.jsonl",
        "cases.jsonl",
        "manifest.json",
    ]

    assert manifest["dataset_id"] == "test-dataset"
    assert manifest["created_at"] == "2026-08-21T20:00:00+00:00"
    assert manifest["counts"] == {
        "total": 2,
        "dev": 1,
        "holdout": 1,
    }
    assert manifest["splits"] == {
        "dev": ["qc-001"],
        "holdout": ["qc-002"],
    }
    assert manifest["dataset"] == {
        "run_ids": dataset_config["run_ids"],
        "population": dataset_config["population"],
        "sampling": dataset_config["sampling"],
    }

    cases = load_qualitative_cases(
        "test-dataset",
        results_dir=tmp_path,
    )
    sources = load_case_sources(
        "test-dataset",
        results_dir=tmp_path,
    )

    assert [
        case.case_id
        for case in cases
    ] == [
        "qc-001",
        "qc-002",
    ]
    assert [
        source.case_id
        for source in sources
    ] == [
        "qc-001",
        "qc-002",
    ]

    first_case = cases[0].model_dump(mode="json")

    assert "source" not in first_case
    assert "agent_config" not in first_case
    assert "llm_config" not in first_case
    assert "goal_achieved" not in first_case
    assert "goal_reason" not in first_case

    assert sources[0].agent_config == "minimal"
    assert sources[0].llm_config == "nova-lite"
    assert sources[1].split == "holdout"


def test_load_dataset_manifest_preserves_dataset_config(
    tmp_path,
) -> None:
    dataset_config = _dataset_config_for_persistence()

    create_qualitative_dataset(
        dataset_config,
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    manifest = load_dataset_manifest(
        "test-dataset",
        results_dir=tmp_path,
    )

    assert manifest["dataset"] == {
        "run_ids": dataset_config["run_ids"],
        "population": dataset_config["population"],
        "sampling": dataset_config["sampling"],
    }
    assert manifest["rubric_version"] == "planning-quality-v1"
    assert manifest["case_view_version"] == "trajectory-planning-v1"


def test_create_qualitative_dataset_rejects_existing_dataset(
    tmp_path,
) -> None:
    sampled_trials = _sampled_trials_for_persistence()

    dataset_config = _dataset_config_for_persistence()

    create_qualitative_dataset(
        dataset_config,
        sampled_trials,
        results_dir=tmp_path,
    )

    with pytest.raises(
        FileExistsError,
        match="test-dataset",
    ):
        create_qualitative_dataset(
            dataset_config,
            sampled_trials,
            results_dir=tmp_path,
        )

def test_create_qualitative_dataset_rejects_duplicate_case_ids(
    tmp_path,
) -> None:
    sampled_trials = _sampled_trials_for_persistence()

    duplicated = [
        sampled_trials[0],
        SampledTrial(
            case_id=sampled_trials[0].case_id,
            split="holdout",
            candidate=sampled_trials[1].candidate,
        ),
    ]

    with pytest.raises(
        ValueError,
        match="case_id del dataset deben ser únicos",
    ):
        create_qualitative_dataset(
            _dataset_config_for_persistence(),
            duplicated,
            results_dir=tmp_path,
        )

    assert not (tmp_path / "test-dataset").exists()


def test_pilot_dataset_config_defines_shared_population_and_sampling() -> None:
    config = M3_QUALITATIVE_PILOT_DATASET_CONFIG

    assert config["dataset_id"] == "qualitative-pilot-v1"
    assert config["run_ids"] == [
        "m3-nova-multi-attempt-run-004",
    ]
    assert config["population"]["agent_configs"] is None
    assert config["population"]["trial_configs"] == [
        "multi_attempt",
    ]
    assert config["sampling"] == {
        "method": RANDOM_STRATIFIED_BY_SCENARIO_METHOD,
        "seed": 20260821,
        "cases_per_scenario": 3,
        "dev_per_scenario": 2,
    }


def test_prepare_qualitative_dataset_uses_shared_config(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    run = _sampling_run()

    for result in run["results"]:
        for trial in result["trials"]:
            trial["attempts"] = [
                _attempt(
                    user_message="Resolvé el desafío.",
                    trace=[
                        _agent_call(
                            content="Respuesta final.",
                        ),
                    ],
                    answer="Respuesta final.",
                ),
            ]

    monkeypatch.setattr(
        "eval.llm_judge.prepare_dataset.load_run_results",
        lambda run_id: run,
    )

    dataset_config = {
        "dataset_id": "prepared-dataset",
        "run_ids": [
            "test-run",
        ],
        "population": {
            "agent_configs": None,
            "llm_configs": [
                "nova-lite",
            ],
            "trial_configs": [
                "single_attempt",
            ],
            "scenarios": [
                "study-with-key",
                "office-sequence",
            ],
        },
        "sampling": {
            "method": RANDOM_STRATIFIED_BY_SCENARIO_METHOD,
            "seed": 1234,
            "cases_per_scenario": 3,
            "dev_per_scenario": 2,
        },
    }

    result = prepare_qualitative_dataset(
        dataset_config,
        results_dir=tmp_path,
    )

    assert result["eligible_trials"] == 12
    assert result["manifest"]["counts"] == {
        "total": 6,
        "dev": 4,
        "holdout": 2,
    }
    assert (
        result["manifest"]["dataset"]["population"]
        == dataset_config["population"]
    )
    assert (
        result["manifest"]["dataset"]["sampling"]
        == dataset_config["sampling"]
    )


def test_prepare_qualitative_dataset_rejects_unknown_sampling_method(
    tmp_path,
) -> None:
    dataset_config = _dataset_config_for_persistence()
    dataset_config["sampling"]["method"] = "unknown"

    with pytest.raises(
        ValueError,
        match="Método de sampling no soportado",
    ):
        prepare_qualitative_dataset(
            dataset_config,
            results_dir=tmp_path,
        )


def test_human_annotation_accepts_only_applicable_criteria() -> None:
    case = _qualitative_case()
    annotation = _human_annotation()

    validate_human_annotation(
        case,
        annotation,
    )


def test_human_annotation_rejects_non_applicable_criterion() -> None:
    case = _qualitative_case()
    annotation_data = _human_annotation().model_dump()
    annotation_data["criteria"]["Q1.4"] = {
        "verdict": "PASS",
        "reason": "No fue necesario replanificar.",
        "evidence_refs": [
            "a1.i1.action1",
        ],
    }
    annotation = HumanAnnotation.model_validate(
        annotation_data
    )

    with pytest.raises(
        ValueError,
        match="criterios no aplicables",
    ):
        validate_human_annotation(
            case,
            annotation,
        )


def test_human_annotation_requires_reason_and_evidence() -> None:
    with pytest.raises(ValidationError):
        HumanCriterionAnnotation(
            verdict="FAIL",
            reason="",
            evidence_refs=[],
        )


def test_human_annotation_rejects_mismatched_case_version() -> None:
    case = _qualitative_case()
    annotation_data = _human_annotation().model_dump()
    annotation_data["case_view_version"] = "other-view"
    annotation = HumanAnnotation.model_validate(
        annotation_data
    )

    with pytest.raises(
        ValueError,
        match="vista del caso",
    ):
        validate_human_annotation(
            case,
            annotation,
        )


def test_human_annotation_rejects_unknown_evidence_ref() -> None:
    case = _qualitative_case()
    annotation_data = _human_annotation().model_dump()
    annotation_data["criteria"]["Q1.1"]["evidence_refs"] = [
        "a1.i99.action1",
    ]
    annotation = HumanAnnotation.model_validate(
        annotation_data
    )

    with pytest.raises(
        ValueError,
        match="referencias de evidencia inexistentes",
    ):
        validate_human_annotation(
            case,
            annotation,
        )


def test_save_and_load_human_annotation(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    annotation_data = _human_annotation().model_dump()
    annotation_data["case_id"] = "qc-001"
    annotation = HumanAnnotation.model_validate(
        annotation_data
    )

    save_human_annotation(
        "test-dataset",
        annotation,
        results_dir=tmp_path,
    )

    loaded = load_human_annotations(
        "test-dataset",
        "annotator-a",
        results_dir=tmp_path,
    )

    assert loaded == [
        annotation,
    ]
    assert (
        tmp_path
        / "test-dataset"
        / "annotations"
        / "annotator-a.jsonl"
    ).exists()


def test_save_human_annotation_rejects_duplicate_case(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    annotation = _human_annotation()

    save_human_annotation(
        "test-dataset",
        annotation,
        results_dir=tmp_path,
    )

    with pytest.raises(
        FileExistsError,
        match="ya tiene una anotación",
    ):
        save_human_annotation(
            "test-dataset",
            annotation,
            results_dir=tmp_path,
        )

    loaded = load_human_annotations(
        "test-dataset",
        "annotator-a",
        results_dir=tmp_path,
    )

    assert len(loaded) == 1


def test_save_human_annotation_rejects_unknown_case(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    annotation_data = _human_annotation().model_dump()
    annotation_data["case_id"] = "qc-999"
    annotation = HumanAnnotation.model_validate(
        annotation_data
    )

    with pytest.raises(
        ValueError,
        match="no pertenece al dataset",
    ):
        save_human_annotation(
            "test-dataset",
            annotation,
            results_dir=tmp_path,
        )


def test_case_presentation_preserves_canonical_blind_evidence() -> None:
    presentation = build_case_presentation(
        _qualitative_case()
    )

    assert presentation.version == PRESENTATION_VERSION
    assert presentation.evidence_refs == (
        "a1.user_message",
        "a1.i1",
        "a1.i1.action1",
        "a1.termination",
    )

    data = json.loads(presentation.text)

    assert data["case_id"] == "qc-001"
    assert data["task"] == "Abrí la puerta principal."
    assert tuple(data["evidence_rules"]) == EVIDENCE_RULES
    assert data["attempts"][0]["iterations"][0][
        "assistant_content"
    ] == "<thinking>Primero voy a mirar.</thinking>"

    action = data["attempts"][0]["iterations"][0][
        "actions"
    ][0]

    assert action["ref"] == "a1.i1.action1"
    assert action["proposed_action"]["tool"] == "look"
    assert action["execution"]["action"]["tool"] == "look"
    assert action["execution"]["differs_from_proposal"] is False
    assert action["execution"]["observation"]["content"] == (
        "Ves una llave."
    )


def test_case_presentation_excludes_evaluation_metadata() -> None:
    presentation = build_case_presentation(
        _qualitative_case()
    )

    assert "criteria_applicability" not in presentation.text
    assert "goal_achieved" not in presentation.text
    assert "goal_reason" not in presentation.text
    assert "agent_config" not in presentation.text
    assert "llm_config" not in presentation.text
    assert "trial_config" not in presentation.text


def test_human_annotation_rejects_mismatched_presentation_version() -> None:
    case = _qualitative_case()
    annotation_data = _human_annotation().model_dump()
    annotation_data["presentation_version"] = "other-presentation"
    annotation = HumanAnnotation.model_validate(
        annotation_data
    )

    with pytest.raises(
        ValueError,
        match="versión vigente de la presentación",
    ):
        validate_human_annotation(
            case,
            annotation,
        )


def test_annotator_management(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    assert list_annotators(
        "test-dataset",
        results_dir=tmp_path,
    ) == []

    create_annotator(
        "test-dataset",
        "annotator-a",
        results_dir=tmp_path,
    )

    assert list_annotators(
        "test-dataset",
        results_dir=tmp_path,
    ) == [
        "annotator-a",
    ]

    with pytest.raises(
        FileExistsError,
        match="ya existe",
    ):
        create_annotator(
            "test-dataset",
            "annotator-a",
            results_dir=tmp_path,
        )

    delete_annotator(
        "test-dataset",
        "annotator-a",
        results_dir=tmp_path,
    )

    assert list_annotators(
        "test-dataset",
        results_dir=tmp_path,
    ) == []


def test_update_human_annotation_requires_explicit_update(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    annotation = _human_annotation()

    save_human_annotation(
        "test-dataset",
        annotation,
        results_dir=tmp_path,
    )

    annotation_data = annotation.model_dump()
    annotation_data["criteria"]["Q1.1"]["verdict"] = "FAIL"
    annotation_data["criteria"]["Q1.1"]["reason"] = (
        "La evidencia muestra una inconsistencia material."
    )
    updated = HumanAnnotation.model_validate(
        annotation_data
    )

    update_human_annotation(
        "test-dataset",
        updated,
        results_dir=tmp_path,
    )

    loaded = load_human_annotations(
        "test-dataset",
        "annotator-a",
        results_dir=tmp_path,
    )

    assert len(loaded) == 1
    assert loaded[0].criteria["Q1.1"].verdict == "FAIL"
    assert loaded[0].criteria["Q1.1"].reason == (
        "La evidencia muestra una inconsistencia material."
    )


def test_delete_human_annotation_preserves_annotator(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    annotation = _human_annotation()

    save_human_annotation(
        "test-dataset",
        annotation,
        results_dir=tmp_path,
    )

    delete_human_annotation(
        "test-dataset",
        "annotator-a",
        "qc-001",
        results_dir=tmp_path,
    )

    assert load_human_annotations(
        "test-dataset",
        "annotator-a",
        results_dir=tmp_path,
    ) == []
    assert list_annotators(
        "test-dataset",
        results_dir=tmp_path,
    ) == [
        "annotator-a",
    ]


def test_load_review_cases_supports_all_splits(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    all_cases = load_review_cases(
        "test-dataset",
        "annotator-a",
        results_dir=tmp_path,
    )
    dev_cases = load_review_cases(
        "test-dataset",
        "annotator-a",
        split="dev",
        results_dir=tmp_path,
    )
    holdout_cases = load_review_cases(
        "test-dataset",
        "annotator-a",
        split="holdout",
        results_dir=tmp_path,
    )

    assert [
        review_case.case_id
        for review_case in all_cases
    ] == [
        "qc-001",
        "qc-002",
    ]
    assert [
        review_case.case_id
        for review_case in dev_cases
    ] == [
        "qc-001",
    ]
    assert [
        review_case.case_id
        for review_case in holdout_cases
    ] == [
        "qc-002",
    ]


def test_load_review_cases_preserves_annotation_state(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    save_human_annotation(
        "test-dataset",
        _human_annotation(),
        results_dir=tmp_path,
    )

    review_cases = load_review_cases(
        "test-dataset",
        "annotator-a",
        results_dir=tmp_path,
    )

    first_case = review_cases[0]
    second_case = review_cases[1]

    assert first_case.case_id == "qc-001"
    assert first_case.annotated is True
    assert first_case.annotation == _human_annotation()

    assert second_case.case_id == "qc-002"
    assert second_case.annotated is False
    assert second_case.annotation is None


def test_load_review_cases_does_not_depend_on_case_sources(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    (
        tmp_path
        / "test-dataset"
        / "case_sources.jsonl"
    ).unlink()

    review_cases = load_review_cases(
        "test-dataset",
        "annotator-a",
        results_dir=tmp_path,
    )

    assert len(review_cases) == 2

    for review_case in review_cases:
        assert review_case.presentation == (
            build_case_presentation(
                review_case.case
            )
        )


def test_annotate_selects_requested_case(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    review_cases = load_review_cases(
        "test-dataset",
        "annotator-a",
        results_dir=tmp_path,
    )

    selected = _selected_case(
        review_cases,
        "qc-002",
    )

    assert selected is not None
    assert selected.case_id == "qc-002"


def test_annotate_builds_annotation_from_shared_review_case(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    review_case = load_review_cases(
        "test-dataset",
        "annotator-a",
        split="dev",
        results_dir=tmp_path,
    )[0]

    form = {
        "Q1.1.verdict": ["PASS"],
        "Q1.1.reason": ["Consistencia factual adecuada."],
        "Q1.1.evidence_refs": ["a1.i1"],
        "Q1.2.verdict": ["PASS"],
        "Q1.2.reason": ["Subobjetivos razonables."],
        "Q1.2.evidence_refs": ["a1.i1"],
        "Q1.3.verdict": ["PASS"],
        "Q1.3.reason": ["Ejecución coherente."],
        "Q1.3.evidence_refs": ["a1.i1"],
    }

    annotation = _annotation_from_form(
        review_case,
        "annotator-a",
        form,
    )

    assert annotation.case_id == "qc-001"
    assert annotation.annotator_id == "annotator-a"
    assert (
        annotation.presentation_version
        == review_case.presentation.version
    )
    assert set(annotation.criteria) == {
        "Q1.1",
        "Q1.2",
        "Q1.3",
    }


def test_annotate_filters_cases_by_annotation_status(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    save_human_annotation(
        "test-dataset",
        _human_annotation(),
        results_dir=tmp_path,
    )

    monkeypatch.setattr(
        "eval.llm_judge.annotate.RESULTS_DIR",
        tmp_path,
    )

    pending = _load_selected_cases(
        "test-dataset",
        "annotator-a",
        "all",
        "pending",
    )
    annotated = _load_selected_cases(
        "test-dataset",
        "annotator-a",
        "all",
        "annotated",
    )

    assert [
        review_case.case_id
        for review_case in pending
    ] == [
        "qc-002",
    ]
    assert [
        review_case.case_id
        for review_case in annotated
    ] == [
        "qc-001",
    ]


def test_annotate_page_exposes_delete_only_for_annotated_case(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    save_human_annotation(
        "test-dataset",
        _human_annotation(),
        results_dir=tmp_path,
    )

    monkeypatch.setattr(
        "eval.llm_judge.annotate.RESULTS_DIR",
        tmp_path,
    )

    review_cases = load_review_cases(
        "test-dataset",
        "annotator-a",
        results_dir=tmp_path,
    )

    annotated_page = _page_html(
        dataset_id="test-dataset",
        annotator_id="annotator-a",
        split="all",
        status="all",
        review_cases=review_cases,
        review_case=review_cases[0],
    )
    pending_page = _page_html(
        dataset_id="test-dataset",
        annotator_id="annotator-a",
        split="all",
        status="all",
        review_cases=review_cases,
        review_case=review_cases[1],
    )

    assert 'formaction="/annotation/delete"' in annotated_page
    assert 'formaction="/annotation/delete"' not in pending_page


def test_annotate_page_case_links_preserve_filters(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    monkeypatch.setattr(
        "eval.llm_judge.annotate.RESULTS_DIR",
        tmp_path,
    )

    review_cases = load_review_cases(
        "test-dataset",
        "annotator-a",
        results_dir=tmp_path,
    )

    page = _page_html(
        dataset_id="test-dataset",
        annotator_id="annotator-a",
        split="dev",
        status="pending",
        review_cases=review_cases,
        review_case=review_cases[0],
    )

    assert (
        "dataset_id=test-dataset"
        "&amp;annotator_id=annotator-a"
        "&amp;split=dev"
        "&amp;status=pending"
        "&amp;case_id=qc-001"
    ) in page


def test_annotate_defaults_to_existing_annotator(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    create_annotator(
        "test-dataset",
        "Bruno",
        results_dir=tmp_path,
    )

    monkeypatch.setattr(
        "eval.llm_judge.annotate.RESULTS_DIR",
        tmp_path,
    )

    assert _default_annotator_id(
        "test-dataset"
    ) == "Bruno"


def test_human_annotation_accepts_partial_applicable_criteria() -> None:
    case = _qualitative_case()
    annotation_data = _human_annotation().model_dump()

    annotation_data["criteria"] = {
        "Q1.1": annotation_data[
            "criteria"
        ]["Q1.1"],
    }

    annotation = HumanAnnotation.model_validate(
        annotation_data
    )

    validate_human_annotation(
        case,
        annotation,
    )


def test_review_case_distinguishes_partial_and_completed_annotation(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    annotation_data = _human_annotation().model_dump()
    annotation_data["criteria"] = {
        "Q1.1": annotation_data[
            "criteria"
        ]["Q1.1"],
    }
    partial_annotation = HumanAnnotation.model_validate(
        annotation_data
    )

    save_human_annotation(
        "test-dataset",
        partial_annotation,
        results_dir=tmp_path,
    )

    review_cases = load_review_cases(
        "test-dataset",
        "annotator-a",
        results_dir=tmp_path,
    )

    first_case = review_cases[0]

    assert first_case.annotated is True
    assert first_case.in_progress is True
    assert first_case.completed is False


def test_annotate_builds_partial_annotation(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    review_case = load_review_cases(
        "test-dataset",
        "annotator-a",
        split="dev",
        results_dir=tmp_path,
    )[0]

    annotation = _annotation_from_form(
        review_case,
        "annotator-a",
        {
            "Q1.1.verdict": [
                "FAIL",
            ],
            "Q1.1.reason": [
                "La decisión contradice "
                "la evidencia disponible.",
            ],
            "Q1.1.evidence_refs": [
                "a1.i1",
            ],
        },
    )

    assert set(annotation.criteria) == {
        "Q1.1",
    }


def test_annotate_evidence_inputs_belong_to_annotation_form(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    monkeypatch.setattr(
        "eval.llm_judge.annotate.RESULTS_DIR",
        tmp_path,
    )

    review_cases = load_review_cases(
        "test-dataset",
        "annotator-a",
        results_dir=tmp_path,
    )

    page = _page_html(
        dataset_id="test-dataset",
        annotator_id="annotator-a",
        split="all",
        status="all",
        review_cases=review_cases,
        review_case=review_cases[0],
    )

    assert (
        'class="evidence-checkbox" '
        'type="checkbox" '
        'hidden '
        'form="annotation-form"'
    ) in page


def test_annotate_page_exposes_complete_canonical_rubric(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    monkeypatch.setattr(
        "eval.llm_judge.annotate.RESULTS_DIR",
        tmp_path,
    )

    review_cases = load_review_cases(
        "test-dataset",
        "annotator-a",
        results_dir=tmp_path,
    )

    page = _page_html(
        dataset_id="test-dataset",
        annotator_id="annotator-a",
        split="all",
        status="all",
        review_cases=review_cases,
        review_case=review_cases[0],
    )

    common_rubric_texts = (
        DIMENSION_NAME,
        DIMENSION_DESCRIPTION,
        MATERIALITY_RULE,
        *EVIDENCE_RULES,
        *BOUNDARY_RULES,
    )

    for text in common_rubric_texts:
        assert html.escape(text) in page

    for criterion in CRITERIA:
        assert html.escape(criterion.name) in page
        assert html.escape(criterion.question) in page
        assert html.escape(
            criterion.pass_description
        ) in page
        assert html.escape(
            criterion.fail_description
        ) in page

        for guidance in criterion.guidance:
            assert html.escape(guidance) in page

        if criterion.applicability_description:
            assert html.escape(
                criterion.applicability_description
            ) in page

        for trigger, explanation in (
            criterion.applicability_triggers
        ):
            assert html.escape(trigger) in page
            assert html.escape(explanation) in page

        for note in criterion.applicability_notes:
            assert html.escape(note) in page
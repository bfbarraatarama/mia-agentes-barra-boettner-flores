import html
import json
import pytest
from pydantic import ValidationError

from eval.llm_judge.cases import build_qualitative_case
from eval.llm_judge.models import (
    ActionObservation,
    ApplicabilityTrigger,
    ApplicabilityTriggerComponent,
    AttemptTermination,
    CaseSource,
    CriterionApplicability,
    QualitativeAction,
    QualitativeAttempt,
    QualitativeCase,
    QualitativeInternalContext,
    QualitativeIteration,
    ToolCallView,
    ActionExecution,
    HumanAnnotation,
    HumanCriterionAnnotation,
    JudgeCasePrediction,
    JudgeCriterionDecision,
)
from eval.llm_judge.persistence import (
    JUDGE_EVALUATION_MANIFEST_SCHEMA_VERSION,
    append_judge_trace_event,
    create_judge_evaluation,
    create_qualitative_dataset,
    load_case_sources,
    load_dataset_manifest,
    load_judge_case_predictions,
    load_judge_evaluation_manifest,
    load_judge_evaluation_progress,
    load_judge_trace,
    load_qualitative_cases,
    save_judge_case_prediction,
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
    Q1_4_GUIDANCE,
    Q1_4_NO_TRIGGER_REASON,
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
from eval.llm_judge.judge import (
    JUDGE_PREDICTION_SCHEMA_VERSION,
    JUDGE_PROMPT_VERSION,
    JUDGE_SYSTEM_PROMPT,
    judge_prompt_fingerprint,
    build_judge_case_prediction,
    build_judge_prompt,
    judge_case,
    judge_case_criterion,
)
from eval.llm_judge.runner import (
    resume_judge_evaluation,
    start_judge_evaluation,
)
from eval.llm_judge.run import (
    execute_judge_config,
    main as judge_run_main,
)
from eval.llm_judge.comparison import (
    ConfusionMatrix,
    compare_human_and_judge,
    compare_human_annotators,
    compute_agreement_stats,
)
from mia_agents.testing.mock_llm import MockLLMClient
from mia_agents.tool_schema import FINAL_RESULT_TOOL_NAME
from mia_agents.types import LLMResponse, ToolCall
from student_framework.agent import MyAgent
from eval.llm_judge.reviewer import (
    ReviewCase,
    load_review_cases,
)
from eval.llm_judge.annotate import (
    _annotation_from_form,
    _evidence_cards_html,
    _load_selected_cases,
    _page_html,
    _selected_case,
    _default_annotator_id,
)

def _qualitative_case() -> QualitativeCase:
    return QualitativeCase(
        schema_version=5,
        case_view_version="trajectory-planning-v5",
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
        case_schema_version=5,
        case_view_version="trajectory-planning-v5",
        presentation_version=PRESENTATION_VERSION,
        rubric_version=RUBRIC_VERSION,
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


def _judge_response(
    criterion_id: str,
) -> LLMResponse:
    return LLMResponse(
        content=None,
        tool_calls=[
            ToolCall(
                id=f"judge-{criterion_id}",
                name=FINAL_RESULT_TOOL_NAME,
                arguments=json.dumps({
                    "verdict": "PASS",
                    "reason": (
                        f"Justificación para {criterion_id}."
                    ),
                    "evidence_refs": [
                        "a1.i1",
                    ],
                }),
            ),
        ],
    )


def test_llm_judge_rubric_defines_planning_quality_criteria() -> None:
    assert RUBRIC_VERSION == "planning-quality-v4"
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


def test_qualitative_case_requires_q1_4_triggers_when_applicable() -> None:
    case_data = _qualitative_case().model_dump()
    case_data["criteria_applicability"]["Q1.4"] = {
        "applicable": True,
        "reason": None,
        "triggers": [],
    }

    with pytest.raises(
        ValidationError,
        match="si y sólo si contiene triggers",
    ):
        QualitativeCase.model_validate(
            case_data
        )


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


def test_build_qualitative_case_preserves_internal_context_temporally() -> None:
    first_summary = (
        "Hechos descubiertos:\n"
        "- La puerta requiere una llave."
    )
    continuation_summary = (
        "Subobjetivos pendientes:\n"
        "- Encontrar la llave."
    )
    unused_summary = "Este resumen ya no puede afectar otra decisión."

    first_attempt_trace = [
        {
            "type": "llm_call",
            "purpose": "planning",
            "retry_index": 0,
            "messages": [],
            "response": {
                "content": None,
                "tool_calls": [],
            },
        },
        {
            "type": "planning",
            "plan": {
                "steps": [
                    {"description": "Examinar la puerta"},
                    {"description": "Encontrar la llave"},
                ],
            },
        },
        _agent_call(
            content="Primero examino la puerta.",
            tool_calls=[
                {
                    "id": "examine-1",
                    "name": "examine",
                    "arguments": json.dumps({"target": "puerta"}),
                },
            ],
        ),
        {
            "type": "history_compaction",
            "evicted_messages": 4,
            "summary": first_summary,
            "summary_chars": len(first_summary),
        },
        {
            "type": "tool_execution",
            "retry_index": 0,
            "tool_name": "examine",
            "arguments": {"target": "puerta"},
            "output": "La puerta está cerrada.",
        },
        _agent_call(
            content="Todavía no terminé.",
        ),
        {
            "type": "history_compaction",
            "evicted_messages": 3,
            "summary": continuation_summary,
            "summary_chars": len(continuation_summary),
        },
    ]
    first_attempt_steps = [
        {
            "tool_name": "examine",
            "tool_input": json.dumps({"target": "puerta"}),
            "tool_output": "La puerta está cerrada.",
            "error": None,
        },
    ]
    second_attempt_trace = [
        _agent_call(
            content="Continúo buscando la llave.",
        ),
        {
            "type": "history_compaction",
            "evicted_messages": 3,
            "summary": unused_summary,
            "summary_chars": len(unused_summary),
        },
    ]
    trial = {
        "trial_index": 1,
        "goal_achieved": False,
        "goal_reason": "pendiente",
        "attempts": [
            _attempt(
                attempt_index=1,
                trace=first_attempt_trace,
                steps=first_attempt_steps,
                answer="Todavía no terminé.",
            ),
            _attempt(
                attempt_index=2,
                user_message=(
                    "El desafío todavía no está completado. Continuá."
                ),
                trace=second_attempt_trace,
                answer="Continúo buscando la llave.",
            ),
        ],
    }

    case = build_qualitative_case(
        trial,
        case_id="qc-internal-context",
    )

    first_iteration = case.attempts[0].iterations[0]
    final_first_attempt_iteration = case.attempts[0].iterations[1]
    second_attempt_iteration = case.attempts[1].iterations[0]

    assert [
        context.model_dump()
        for context in first_iteration.context_before_decision
    ] == [
        {
            "context_id": "a1.i1.plan1",
            "kind": "plan",
            "content": (
                "1. Examinar la puerta\n"
                "2. Encontrar la llave"
            ),
        },
    ]
    assert [
        context.model_dump()
        for context in first_iteration.context_after_decision
    ] == [
        {
            "context_id": "a1.i1.summary1",
            "kind": "summary",
            "content": first_summary,
        },
    ]
    assert [
        context.model_dump()
        for context in (
            final_first_attempt_iteration.context_after_decision
        )
    ] == [
        {
            "context_id": "a1.i2.summary1",
            "kind": "summary",
            "content": continuation_summary,
        },
    ]
    assert second_attempt_iteration.context_before_decision == []
    assert second_attempt_iteration.context_after_decision == []


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

    assert case.criteria_applicability["Q1.4"].reason is None
    assert case.criteria_applicability["Q1.4"].triggers == [
        ApplicabilityTrigger(
            target_ref="a1.i2",
            components=[
                ApplicabilityTriggerComponent(
                    kind="error_before_later_decision",
                    evidence_refs=[
                        "a1.i1.action1",
                    ],
                ),
            ],
        ),
    ]


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

    assert case.criteria_applicability["Q1.4"].reason is None
    assert case.criteria_applicability["Q1.4"].triggers == [
        ApplicabilityTrigger(
            target_ref="a2.i1",
            components=[
                ApplicabilityTriggerComponent(
                    kind="attempt_continuation",
                    evidence_refs=[
                        "a1.termination",
                        "a2.user_message",
                    ],
                ),
            ],
        ),
    ]


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
    assert case.criteria_applicability["Q1.4"].triggers == []


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
    assert case.criteria_applicability["Q1.4"].triggers == []


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

    assert case.criteria_applicability["Q1.4"].reason is None
    assert case.criteria_applicability["Q1.4"].triggers == [
        ApplicabilityTrigger(
            target_ref="a1.i2",
            components=[
                ApplicabilityTriggerComponent(
                    kind="consecutive_exact_repetition",
                    evidence_refs=[
                        "a1.i1.action1",
                        "a1.i2.action1",
                    ],
                ),
            ],
        ),
    ]


def test_build_qualitative_case_compacts_consecutive_repetition_episode() -> None:
    trace = [
        _agent_call(
            content=None,
            tool_calls=[
                {
                    "id": f"look-{iteration_index}",
                    "name": "look",
                    "arguments": "{}",
                },
            ],
        )
        for iteration_index in range(1, 4)
    ]
    steps = [
        {
            "tool_name": "look",
            "tool_input": "{}",
            "tool_output": "No ves nada nuevo.",
            "error": None,
        }
        for _ in range(3)
    ]
    trial = {
        "trial_index": 1,
        "goal_achieved": False,
        "goal_reason": "pendiente",
        "attempts": [
            _attempt(trace=trace, steps=steps),
        ],
    }

    case = build_qualitative_case(
        trial,
        case_id="qc-repetition-chain",
    )

    assert case.criteria_applicability["Q1.4"].triggers == [
        ApplicabilityTrigger(
            target_ref="a1.i2",
            components=[
                ApplicabilityTriggerComponent(
                    kind="consecutive_exact_repetition",
                    evidence_refs=[
                        "a1.i1.action1",
                        "a1.i2.action1",
                        "a1.i3.action1",
                    ],
                ),
            ],
        ),
    ]


def test_build_qualitative_case_collects_multiple_q1_4_trigger_types() -> None:
    first_attempt = _attempt(
        attempt_index=1,
        user_message="Abrí la puerta.",
        trace=[
            _agent_call(
                content=None,
                tool_calls=[
                    {
                        "id": "go-1",
                        "name": "go",
                        "arguments": json.dumps({
                            "direction": "norte",
                        }),
                    },
                ],
            ),
            _agent_call(content="Voy a corregirlo."),
        ],
        steps=[
            {
                "tool_name": "go",
                "tool_input": json.dumps({
                    "direction": "norte",
                }),
                "tool_output": (
                    "Error: no hay salida 'norte' desde aquí."
                ),
                "error": None,
            },
        ],
        answer="No terminé.",
    )
    second_attempt = _attempt(
        attempt_index=2,
        user_message=(
            "El desafío todavía no está completado. Continuá."
        ),
        trace=[
            _agent_call(content="Continúo."),
        ],
        answer="Continúo.",
    )
    trial = {
        "trial_index": 1,
        "goal_achieved": False,
        "goal_reason": "pendiente",
        "attempts": [
            first_attempt,
            second_attempt,
        ],
    }

    case = build_qualitative_case(
        trial,
        case_id="qc-multiple-triggers",
    )

    assert case.criteria_applicability["Q1.4"].triggers == [
        ApplicabilityTrigger(
            target_ref="a1.i2",
            components=[
                ApplicabilityTriggerComponent(
                    kind="error_before_later_decision",
                    evidence_refs=[
                        "a1.i1.action1",
                    ],
                ),
            ],
        ),
        ApplicabilityTrigger(
            target_ref="a2.i1",
            components=[
                ApplicabilityTriggerComponent(
                    kind="attempt_continuation",
                    evidence_refs=[
                        "a1.termination",
                        "a2.user_message",
                    ],
                ),
            ],
        ),
    ]


def test_build_qualitative_case_does_not_mark_non_consecutive_repetition() -> None:
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
                    "id": "examine-1",
                    "name": "examine",
                    "arguments": json.dumps({
                        "target": "puerta",
                    }),
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
            "tool_name": "examine",
            "tool_input": json.dumps({
                "target": "puerta",
            }),
            "tool_output": "La puerta está cerrada.",
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
            _attempt(
                trace=trace,
                steps=steps,
            ),
        ],
    }

    case = build_qualitative_case(
        trial,
        case_id="qc-non-consecutive-repetition",
    )

    assert case.criteria_applicability["Q1.4"].applicable is False
    assert case.criteria_applicability["Q1.4"].triggers == []


def test_build_qualitative_case_requires_same_repetition_observation() -> None:
    trace = [
        _agent_call(
            content=None,
            tool_calls=[
                {
                    "id": "go-1",
                    "name": "go",
                    "arguments": json.dumps({
                        "direction": "este",
                    }),
                },
            ],
        ),
        _agent_call(
            content=None,
            tool_calls=[
                {
                    "id": "go-2",
                    "name": "go",
                    "arguments": json.dumps({
                        "direction": "este",
                    }),
                },
            ],
        ),
    ]
    steps = [
        {
            "tool_name": "go",
            "tool_input": json.dumps({
                "direction": "este",
            }),
            "tool_output": "Llegas a Galería central.",
            "error": None,
        },
        {
            "tool_name": "go",
            "tool_input": json.dumps({
                "direction": "este",
            }),
            "tool_output": "Llegas a Taller.",
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
            ),
        ],
    }

    case = build_qualitative_case(
        trial,
        case_id="qc-different-observation",
    )

    assert case.criteria_applicability["Q1.4"].applicable is False
    assert case.criteria_applicability["Q1.4"].triggers == []


def test_build_qualitative_case_groups_q1_4_signals_by_decision() -> None:
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
        _agent_call(
            content="Voy a volver a mirar.",
            tool_calls=[
                {
                    "id": "look-3",
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
            "tool_output": "Error: no ves nada útil.",
            "error": None,
        },
        {
            "tool_name": "look",
            "tool_input": "{}",
            "tool_output": "Error: no ves nada útil.",
            "error": None,
        },
        {
            "tool_name": "look",
            "tool_input": "{}",
            "tool_output": "Error: no ves nada útil.",
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
            ),
        ],
    }

    case = build_qualitative_case(
        trial,
        case_id="qc-grouped-trigger",
    )

    assert case.criteria_applicability["Q1.4"].triggers == [
        ApplicabilityTrigger(
            target_ref="a1.i2",
            components=[
                ApplicabilityTriggerComponent(
                    kind="error_before_later_decision",
                    evidence_refs=[
                        "a1.i1.action1",
                        "a1.i1.action2",
                    ],
                ),
                ApplicabilityTriggerComponent(
                    kind="consecutive_exact_repetition",
                    evidence_refs=[
                        "a1.i1.action2",
                        "a1.i2.action1",
                    ],
                ),
            ],
        ),
    ]


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
    assert manifest["rubric_version"] == "planning-quality-v4"
    assert manifest["case_view_version"] == "trajectory-planning-v5"


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


def test_create_judge_evaluation_persists_reproducible_manifest(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    monkeypatch.setattr(
        "eval.llm_judge.persistence._created_at",
        lambda: "2026-08-23T21:00:00+00:00",
    )
    monkeypatch.setattr(
        "eval.llm_judge.persistence._git_metadata",
        lambda: {
            "commit": "abc123",
            "branch": "main",
            "dirty": False,
        },
    )
    monkeypatch.setattr(
        "eval.llm_judge.persistence._effective_llm_config",
        lambda config_name: {
            "provider": "bedrock",
            "model": "judge-model",
            "temperature": 0.0,
        },
    )

    manifest = create_judge_evaluation(
        "test-dataset",
        "judge-eval-001",
        split="dev",
        judge_llm_config="nova-lite",
        max_repair_attempts=2,
        results_dir=tmp_path,
    )

    assert manifest == {
        "schema_version": (
            JUDGE_EVALUATION_MANIFEST_SCHEMA_VERSION
        ),
        "judge_eval_id": "judge-eval-001",
        "dataset_id": "test-dataset",
        "created_at": "2026-08-23T21:00:00+00:00",
        "git": {
            "commit": "abc123",
            "branch": "main",
            "dirty": False,
        },
        "split": "dev",
        "case_ids": [
            "qc-001",
        ],
        "judge": {
            "llm_config": "nova-lite",
            "effective_llm_config": {
                "provider": "bedrock",
                "model": "judge-model",
                "temperature": 0.0,
            },
            "system_prompt": JUDGE_SYSTEM_PROMPT,
            "prompt_fingerprint_sha256": (
                judge_prompt_fingerprint()
            ),
            "max_repair_attempts": 2,
        },
        "versions": {
            "prediction_schema_version": (
                JUDGE_PREDICTION_SCHEMA_VERSION
            ),
            "case_schema_version": 5,
            "case_view_version": "trajectory-planning-v5",
            "presentation_version": PRESENTATION_VERSION,
            "rubric_version": RUBRIC_VERSION,
            "judge_prompt_version": JUDGE_PROMPT_VERSION,
        },
    }

    assert (
        load_judge_evaluation_manifest(
            "test-dataset",
            "judge-eval-001",
            results_dir=tmp_path,
        )
        == manifest
    )

    predictions_path = (
        tmp_path
        / "test-dataset"
        / "judge_evaluations"
        / "judge-eval-001"
        / "predictions.jsonl"
    )
    assert predictions_path.read_text(
        encoding="utf-8"
    ) == ""


def test_judge_prediction_persistence_round_trip_and_rejects_duplicate(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )
    create_judge_evaluation(
        "test-dataset",
        "judge-eval-001",
        split="dev",
        judge_llm_config="nova-lite",
        max_repair_attempts=0,
        results_dir=tmp_path,
    )

    case = load_qualitative_cases(
        "test-dataset",
        results_dir=tmp_path,
    )[0]
    decisions = {
        criterion_id: JudgeCriterionDecision(
            verdict="PASS",
            reason=f"Justificación para {criterion_id}.",
            evidence_refs=[
                "a1.i1",
            ],
        )
        for criterion_id in (
            "Q1.1",
            "Q1.2",
            "Q1.3",
        )
    }
    prediction = build_judge_case_prediction(
        case,
        decisions,
    )

    save_judge_case_prediction(
        "test-dataset",
        "judge-eval-001",
        prediction,
        results_dir=tmp_path,
    )

    assert load_judge_case_predictions(
        "test-dataset",
        "judge-eval-001",
        results_dir=tmp_path,
    ) == [
        prediction,
    ]

    with pytest.raises(
        FileExistsError,
        match="Ya existe una predicción",
    ):
        save_judge_case_prediction(
            "test-dataset",
            "judge-eval-001",
            prediction,
            results_dir=tmp_path,
        )


def test_judge_prediction_atomic_write_preserves_previous_predictions(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sampled_trials = (
        _sampled_trials_for_persistence()
    )
    second_sample = sampled_trials[1]

    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        [
            sampled_trials[0],
            SampledTrial(
                case_id=second_sample.case_id,
                split="dev",
                candidate=second_sample.candidate,
            ),
        ],
        results_dir=tmp_path,
    )
    create_judge_evaluation(
        "test-dataset",
        "judge-eval-001",
        split="dev",
        judge_llm_config="nova-lite",
        max_repair_attempts=0,
        results_dir=tmp_path,
    )

    cases = load_qualitative_cases(
        "test-dataset",
        results_dir=tmp_path,
    )
    predictions = []

    for case in cases:
        decisions = {
            criterion_id: JudgeCriterionDecision(
                verdict="PASS",
                reason=(
                    f"Justificación para {criterion_id}."
                ),
                evidence_refs=[
                    "a1.i1",
                ],
            )
            for criterion_id, applicability
            in case.criteria_applicability.items()
            if applicability.applicable
        }
        predictions.append(
            build_judge_case_prediction(
                case,
                decisions,
            )
        )

    save_judge_case_prediction(
        "test-dataset",
        "judge-eval-001",
        predictions[0],
        results_dir=tmp_path,
    )

    predictions_path = (
        tmp_path
        / "test-dataset"
        / "judge_evaluations"
        / "judge-eval-001"
        / "predictions.jsonl"
    )
    previous_content = (
        predictions_path.read_text(
            encoding="utf-8",
        )
    )

    def interrupted_replace(
        source,
        destination,
    ) -> None:
        raise RuntimeError(
            "corte simulado durante replace"
        )

    monkeypatch.setattr(
        "eval.llm_judge.persistence.os.replace",
        interrupted_replace,
    )

    with pytest.raises(
        RuntimeError,
        match="corte simulado durante replace",
    ):
        save_judge_case_prediction(
            "test-dataset",
            "judge-eval-001",
            predictions[1],
            results_dir=tmp_path,
        )

    assert predictions_path.read_text(
        encoding="utf-8",
    ) == previous_content

    assert load_judge_case_predictions(
        "test-dataset",
        "judge-eval-001",
        results_dir=tmp_path,
    ) == [
        predictions[0],
    ]

    assert list(
        predictions_path.parent.glob(
            ".predictions.jsonl.*.tmp"
        )
    ) == []


def test_judge_prediction_rejects_case_outside_evaluation_split(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )
    create_judge_evaluation(
        "test-dataset",
        "judge-eval-001",
        split="dev",
        judge_llm_config="nova-lite",
        max_repair_attempts=0,
        results_dir=tmp_path,
    )

    cases = load_qualitative_cases(
        "test-dataset",
        results_dir=tmp_path,
    )
    holdout_case = next(
        case
        for case in cases
        if case.case_id == "qc-002"
    )
    decisions = {
        criterion_id: JudgeCriterionDecision(
            verdict="PASS",
            reason=f"Justificación para {criterion_id}.",
            evidence_refs=[
                "a1.i1",
            ],
        )
        for criterion_id in (
            "Q1.1",
            "Q1.2",
            "Q1.3",
        )
    }
    prediction = build_judge_case_prediction(
        holdout_case,
        decisions,
    )

    with pytest.raises(
        ValueError,
        match="no pertenece al split 'dev'",
    ):
        save_judge_case_prediction(
            "test-dataset",
            "judge-eval-001",
            prediction,
            results_dir=tmp_path,
        )


def test_judge_evaluation_rejects_outdated_dataset_versions(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    manifest_path = (
        tmp_path
        / "test-dataset"
        / "manifest.json"
    )
    manifest = json.loads(
        manifest_path.read_text(
            encoding="utf-8",
        )
    )
    manifest["rubric_version"] = (
        "planning-quality-v1"
    )
    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="no corresponde a las versiones vigentes",
    ):
        create_judge_evaluation(
            "test-dataset",
            "judge-eval-001",
            split="dev",
            judge_llm_config="nova-lite",
            max_repair_attempts=0,
            results_dir=tmp_path,
        )


def test_judge_trace_atomic_write_preserves_previous_events(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )
    create_judge_evaluation(
        "test-dataset",
        "judge-eval-001",
        split="dev",
        judge_llm_config="nova-lite",
        max_repair_attempts=0,
        results_dir=tmp_path,
    )

    first_event = {
        "type": "llm_call",
        "messages": [],
        "response": LLMResponse(
            content="primera llamada",
            tool_calls=[],
            input_tokens=10,
            output_tokens=2,
        ),
    }

    append_judge_trace_event(
        "test-dataset",
        "judge-eval-001",
        "qc-001",
        "Q1.1",
        first_event,
        results_dir=tmp_path,
    )

    previous_trace = load_judge_trace(
        "test-dataset",
        "judge-eval-001",
        results_dir=tmp_path,
    )

    def interrupted_replace(
        source,
        destination,
    ) -> None:
        raise RuntimeError(
            "corte simulado durante replace"
        )

    monkeypatch.setattr(
        "eval.llm_judge.persistence.os.replace",
        interrupted_replace,
    )

    second_event = {
        "type": "llm_call",
        "messages": [],
        "response": LLMResponse(
            content="segunda llamada",
            tool_calls=[],
            input_tokens=20,
            output_tokens=4,
        ),
    }

    with pytest.raises(
        RuntimeError,
        match="corte simulado durante replace",
    ):
        append_judge_trace_event(
            "test-dataset",
            "judge-eval-001",
            "qc-001",
            "Q1.1",
            second_event,
            results_dir=tmp_path,
        )

    assert load_judge_trace(
        "test-dataset",
        "judge-eval-001",
        results_dir=tmp_path,
    ) == previous_trace

    trace_path = (
        tmp_path
        / "test-dataset"
        / "judge_evaluations"
        / "judge-eval-001"
        / "trace.jsonl"
    )
    assert list(
        trace_path.parent.glob(
            ".trace.jsonl.*.tmp"
        )
    ) == []


def test_judge_evaluation_traces_repairs_and_token_usage(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sampled_trial = (
        _sampled_trials_for_persistence()[0]
    )

    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        [
            sampled_trial,
        ],
        results_dir=tmp_path,
    )

    llm = MockLLMClient([
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="judge-q11-invalid",
                    name=FINAL_RESULT_TOOL_NAME,
                    arguments=json.dumps({
                        "verdict": "INVALID",
                        "reason": "Salida inválida.",
                        "evidence_refs": [
                            "a1.i1",
                        ],
                    }),
                ),
            ],
            input_tokens=100,
            output_tokens=10,
        ),
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="judge-q11-valid",
                    name=FINAL_RESULT_TOOL_NAME,
                    arguments=json.dumps({
                        "verdict": "PASS",
                        "reason": "Q1.1 corregido.",
                        "evidence_refs": [
                            "a1.i1",
                        ],
                    }),
                ),
            ],
            input_tokens=120,
            output_tokens=12,
        ),
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="judge-q12",
                    name=FINAL_RESULT_TOOL_NAME,
                    arguments=json.dumps({
                        "verdict": "PASS",
                        "reason": "Q1.2 correcto.",
                        "evidence_refs": [
                            "a1.i1",
                        ],
                    }),
                ),
            ],
            input_tokens=200,
            output_tokens=20,
        ),
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="judge-q13",
                    name=FINAL_RESULT_TOOL_NAME,
                    arguments=json.dumps({
                        "verdict": "PASS",
                        "reason": "Q1.3 correcto.",
                        "evidence_refs": [
                            "a1.i1",
                        ],
                    }),
                ),
            ],
            input_tokens=300,
            output_tokens=30,
        ),
    ])

    monkeypatch.setattr(
        "eval.llm_judge.runner.build_llm_client",
        lambda config: llm,
    )

    predictions = start_judge_evaluation(
        "test-dataset",
        "judge-eval-001",
        split="dev",
        judge_llm_config="nova-lite",
        max_repair_attempts=1,
        results_dir=tmp_path,
    )

    assert len(predictions) == 1

    trace = load_judge_trace(
        "test-dataset",
        "judge-eval-001",
        results_dir=tmp_path,
    )

    assert [
        event["criterion_id"]
        for event in trace
    ] == [
        "Q1.1",
        "Q1.1",
        "Q1.2",
        "Q1.3",
    ]
    assert all(
        event["type"] == "llm_call"
        for event in trace
    )
    assert [
        event["response"]["input_tokens"]
        for event in trace
    ] == [
        100,
        120,
        200,
        300,
    ]
    assert [
        event["response"]["output_tokens"]
        for event in trace
    ] == [
        10,
        12,
        20,
        30,
    ]

    q11_messages = trace[1][
        "messages"
    ]
    assert any(
        message.get("role") == "tool"
        and "Error de validación" in message.get(
            "content",
            "",
        )
        for message in q11_messages
    )


def test_execute_judge_config_starts_when_evaluation_does_not_exist(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    judge_config = {
        "dataset_id": "test-dataset",
        "judge_eval_id": "judge-eval-001",
        "split": "dev",
        "judge_llm_config": "nova-lite",
        "max_repair_attempts": 2,
    }
    calls = []

    def missing_manifest(
        dataset_id,
        judge_eval_id,
        *,
        results_dir,
    ):
        raise FileNotFoundError

    def fake_start(
        dataset_id,
        judge_eval_id,
        *,
        split,
        judge_llm_config,
        max_repair_attempts,
        results_dir,
    ):
        calls.append({
            "dataset_id": dataset_id,
            "judge_eval_id": judge_eval_id,
            "split": split,
            "judge_llm_config": judge_llm_config,
            "max_repair_attempts": max_repair_attempts,
            "results_dir": results_dir,
        })
        return []

    def unexpected_resume(*args, **kwargs):
        pytest.fail(
            "No debe reanudarse una evaluación inexistente."
        )

    monkeypatch.setattr(
        "eval.llm_judge.run.load_judge_evaluation_manifest",
        missing_manifest,
    )
    monkeypatch.setattr(
        "eval.llm_judge.run.start_judge_evaluation",
        fake_start,
    )
    monkeypatch.setattr(
        "eval.llm_judge.run.resume_judge_evaluation",
        unexpected_resume,
    )

    result = execute_judge_config(
        judge_config,
        results_dir=tmp_path,
    )

    assert result == {
        "mode": "start",
        "predictions": [],
    }
    assert calls == [
        {
            "dataset_id": "test-dataset",
            "judge_eval_id": "judge-eval-001",
            "split": "dev",
            "judge_llm_config": "nova-lite",
            "max_repair_attempts": 2,
            "results_dir": tmp_path,
        },
    ]


def test_execute_judge_config_resumes_existing_evaluation(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    judge_config = {
        "dataset_id": "test-dataset",
        "judge_eval_id": "judge-eval-001",
        "split": "dev",
        "judge_llm_config": "nova-lite",
        "max_repair_attempts": 2,
    }
    calls = []

    def existing_manifest(
        dataset_id,
        judge_eval_id,
        *,
        results_dir,
    ):
        return {
            "dataset_id": dataset_id,
            "judge_eval_id": judge_eval_id,
        }

    def unexpected_start(*args, **kwargs):
        pytest.fail(
            "No debe iniciarse nuevamente una evaluación existente."
        )

    def fake_resume(
        dataset_id,
        judge_eval_id,
        *,
        results_dir,
    ):
        calls.append({
            "dataset_id": dataset_id,
            "judge_eval_id": judge_eval_id,
            "results_dir": results_dir,
        })
        return []

    monkeypatch.setattr(
        "eval.llm_judge.run.load_judge_evaluation_manifest",
        existing_manifest,
    )
    monkeypatch.setattr(
        "eval.llm_judge.run.start_judge_evaluation",
        unexpected_start,
    )
    monkeypatch.setattr(
        "eval.llm_judge.run.resume_judge_evaluation",
        fake_resume,
    )

    result = execute_judge_config(
        judge_config,
        results_dir=tmp_path,
    )

    assert result == {
        "mode": "resume",
        "predictions": [],
    }
    assert calls == [
        {
            "dataset_id": "test-dataset",
            "judge_eval_id": "judge-eval-001",
            "results_dir": tmp_path,
        },
    ]


def test_judge_run_main_requires_explicit_active_config(
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    monkeypatch.setattr(
        "eval.llm_judge.run.JUDGE_CONFIG",
        None,
    )

    assert judge_run_main() == 1

    captured = capsys.readouterr()

    assert (
        "No hay una JUDGE_CONFIG activa."
        in captured.err
    )


def test_judge_evaluation_resumes_from_last_completed_criterion(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sampled_trials = (
        _sampled_trials_for_persistence()
    )
    second_sample = sampled_trials[1]

    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        [
            sampled_trials[0],
            SampledTrial(
                case_id=second_sample.case_id,
                split="dev",
                candidate=second_sample.candidate,
            ),
        ],
        results_dir=tmp_path,
    )

    first_llm = MockLLMClient([
        _judge_response("Q1.1"),
        _judge_response("Q1.2"),
        _judge_response("Q1.3"),
        _judge_response("Q1.1"),
        _judge_response("Q1.2"),
        RuntimeError("corte simulado"),
    ])
    first_configs = []

    def first_build_llm_client(config):
        first_configs.append(
            dict(config)
        )
        return first_llm

    monkeypatch.setattr(
        "eval.llm_judge.runner.build_llm_client",
        first_build_llm_client,
    )

    with pytest.raises(
        RuntimeError,
        match="corte simulado",
    ):
        start_judge_evaluation(
            "test-dataset",
            "judge-eval-001",
            split="dev",
            judge_llm_config="nova-lite",
            max_repair_attempts=0,
            results_dir=tmp_path,
        )

    predictions = (
        load_judge_case_predictions(
            "test-dataset",
            "judge-eval-001",
            results_dir=tmp_path,
        )
    )
    assert [
        prediction.case_id
        for prediction in predictions
    ] == [
        "qc-001",
    ]

    progress = (
        load_judge_evaluation_progress(
            "test-dataset",
            "judge-eval-001",
            results_dir=tmp_path,
        )
    )
    assert list(
        progress[
            "qc-002"
        ]
    ) == [
        "Q1.1",
        "Q1.2",
    ]

    manifest = (
        load_judge_evaluation_manifest(
            "test-dataset",
            "judge-eval-001",
            results_dir=tmp_path,
        )
    )
    assert first_configs == [
        manifest[
            "judge"
        ][
            "effective_llm_config"
        ]
    ]
    assert first_llm.call_count == 6
    assert all(
        call["system"]
        == JUDGE_SYSTEM_PROMPT
        for call in first_llm.calls
    )

    interrupted_trace = load_judge_trace(
        "test-dataset",
        "judge-eval-001",
        results_dir=tmp_path,
    )
    assert len(interrupted_trace) == 6
    assert interrupted_trace[-1][
        "case_id"
    ] == "qc-002"
    assert interrupted_trace[-1][
        "criterion_id"
    ] == "Q1.3"
    assert interrupted_trace[-1][
        "error"
    ] == {
        "type": "RuntimeError",
        "message": "corte simulado",
    }

    second_llm = MockLLMClient([
        _judge_response("Q1.3"),
    ])
    second_configs = []

    def second_build_llm_client(config):
        second_configs.append(
            dict(config)
        )
        return second_llm

    monkeypatch.setattr(
        "eval.llm_judge.runner.build_llm_client",
        second_build_llm_client,
    )

    resumed = resume_judge_evaluation(
        "test-dataset",
        "judge-eval-001",
        results_dir=tmp_path,
    )

    assert [
        prediction.case_id
        for prediction in resumed
    ] == [
        "qc-001",
        "qc-002",
    ]
    assert second_llm.call_count == 1
    assert second_configs == [
        manifest[
            "judge"
        ][
            "effective_llm_config"
        ]
    ]
    resumed_trace = load_judge_trace(
        "test-dataset",
        "judge-eval-001",
        results_dir=tmp_path,
    )
    assert len(resumed_trace) == 7
    assert resumed_trace[-1][
        "case_id"
    ] == "qc-002"
    assert resumed_trace[-1][
        "criterion_id"
    ] == "Q1.3"
    assert "response" in resumed_trace[-1]


def test_resume_judge_evaluation_rejects_unversioned_prompt_change(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )
    create_judge_evaluation(
        "test-dataset",
        "judge-eval-001",
        split="dev",
        judge_llm_config="nova-lite",
        max_repair_attempts=0,
        results_dir=tmp_path,
    )

    original_build_judge_prompt = (
        build_judge_prompt
    )

    def changed_build_judge_prompt(
        presentation,
        criterion_id,
    ):
        return (
            original_build_judge_prompt(
                presentation,
                criterion_id,
            )
            + "\nCAMBIO LOCAL DE CALIBRACIÓN"
        )

    monkeypatch.setattr(
        "eval.llm_judge.judge.build_judge_prompt",
        changed_build_judge_prompt,
    )

    with pytest.raises(
        ValueError,
        match="huella efectiva del prompt",
    ):
        resume_judge_evaluation(
            "test-dataset",
            "judge-eval-001",
            results_dir=tmp_path,
        )


def test_resume_judge_evaluation_rejects_stale_policy(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )
    create_judge_evaluation(
        "test-dataset",
        "judge-eval-001",
        split="dev",
        judge_llm_config="nova-lite",
        max_repair_attempts=0,
        results_dir=tmp_path,
    )

    manifest_path = (
        tmp_path
        / "test-dataset"
        / "judge_evaluations"
        / "judge-eval-001"
        / "manifest.json"
    )
    manifest = json.loads(
        manifest_path.read_text(
            encoding="utf-8",
        )
    )
    manifest["versions"][
        "judge_prompt_version"
    ] = "planning-criterion-judge-old"
    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    def unexpected_build_llm_client(config):
        pytest.fail(
            "No debe construirse el LLM para un manifest obsoleto."
        )

    monkeypatch.setattr(
        "eval.llm_judge.runner.build_llm_client",
        unexpected_build_llm_client,
    )

    with pytest.raises(
        ValueError,
        match="no corresponde a las versiones vigentes",
    ):
        resume_judge_evaluation(
            "test-dataset",
            "judge-eval-001",
            results_dir=tmp_path,
        )


def test_llm_judge_agreement_computes_confusion_and_cohen_kappa() -> None:
    stats = compute_agreement_stats([
        ("PASS", "PASS"),
        ("PASS", "PASS"),
        ("PASS", "FAIL"),
        ("FAIL", "FAIL"),
    ])

    assert stats.n == 4
    assert stats.agreement == pytest.approx(
        0.75
    )
    assert stats.cohen_kappa == pytest.approx(
        0.5
    )
    assert stats.confusion == ConfusionMatrix(
        first_pass_second_pass=2,
        first_pass_second_fail=1,
        first_fail_second_pass=0,
        first_fail_second_fail=1,
    )

    degenerate = compute_agreement_stats([
        ("PASS", "PASS"),
        ("PASS", "PASS"),
    ])

    assert degenerate.agreement == 1.0
    assert degenerate.cohen_kappa is None


def test_compare_human_and_judge_reports_per_criterion_and_overall(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )
    create_judge_evaluation(
        "test-dataset",
        "judge-eval-001",
        split="dev",
        judge_llm_config="nova-lite",
        max_repair_attempts=0,
        results_dir=tmp_path,
    )

    save_human_annotation(
        "test-dataset",
        _human_annotation(),
        results_dir=tmp_path,
    )

    case = load_qualitative_cases(
        "test-dataset",
        results_dir=tmp_path,
    )[0]
    decisions = {
        "Q1.1": JudgeCriterionDecision(
            verdict="PASS",
            reason="Acuerdo en Q1.1.",
            evidence_refs=[
                "a1.i1",
            ],
        ),
        "Q1.2": JudgeCriterionDecision(
            verdict="FAIL",
            reason="Desacuerdo en Q1.2.",
            evidence_refs=[
                "a1.i1",
            ],
        ),
        "Q1.3": JudgeCriterionDecision(
            verdict="PASS",
            reason="Acuerdo en Q1.3.",
            evidence_refs=[
                "a1.i1",
            ],
        ),
    }
    prediction = build_judge_case_prediction(
        case,
        decisions,
    )
    save_judge_case_prediction(
        "test-dataset",
        "judge-eval-001",
        prediction,
        results_dir=tmp_path,
    )

    report = compare_human_and_judge(
        "test-dataset",
        "judge-eval-001",
        "annotator-a",
        results_dir=tmp_path,
    )

    assert report.dataset_id == "test-dataset"
    assert report.judge_eval_id == "judge-eval-001"
    assert report.annotator_id == "annotator-a"
    assert report.split == "dev"
    assert report.case_ids == (
        "qc-001",
    )

    assert report.overall.n == 3
    assert report.overall.agreement == pytest.approx(
        2 / 3
    )
    assert report.overall.cohen_kappa == pytest.approx(
        0.0
    )
    assert report.overall.confusion == ConfusionMatrix(
        first_pass_second_pass=2,
        first_pass_second_fail=1,
        first_fail_second_pass=0,
        first_fail_second_fail=0,
    )

    assert report.by_criterion["Q1.1"].n == 1
    assert (
        report.by_criterion[
            "Q1.1"
        ].agreement
        == 1.0
    )
    assert (
        report.by_criterion[
            "Q1.1"
        ].cohen_kappa
        is None
    )

    assert report.by_criterion["Q1.2"].n == 1
    assert (
        report.by_criterion[
            "Q1.2"
        ].agreement
        == 0.0
    )
    assert (
        report.by_criterion[
            "Q1.2"
        ].cohen_kappa
        == 0.0
    )

    assert report.by_criterion["Q1.4"].n == 0
    assert (
        report.by_criterion[
            "Q1.4"
        ].agreement
        is None
    )
    assert (
        report.by_criterion[
            "Q1.4"
        ].cohen_kappa
        is None
    )


def test_compare_human_and_judge_allows_historical_judge_policy(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )
    create_judge_evaluation(
        "test-dataset",
        "judge-eval-001",
        split="dev",
        judge_llm_config="nova-lite",
        max_repair_attempts=0,
        results_dir=tmp_path,
    )

    save_human_annotation(
        "test-dataset",
        _human_annotation(),
        results_dir=tmp_path,
    )

    case = load_qualitative_cases(
        "test-dataset",
        results_dir=tmp_path,
    )[0]
    decisions = {
        criterion_id: JudgeCriterionDecision(
            verdict="PASS",
            reason=f"Justificación para {criterion_id}.",
            evidence_refs=[
                "a1.i1",
            ],
        )
        for criterion_id in (
            "Q1.1",
            "Q1.2",
            "Q1.3",
        )
    }
    prediction = build_judge_case_prediction(
        case,
        decisions,
    )
    save_judge_case_prediction(
        "test-dataset",
        "judge-eval-001",
        prediction,
        results_dir=tmp_path,
    )

    monkeypatch.setattr(
        "eval.llm_judge.persistence.judge_prompt_fingerprint",
        lambda: "politica-actual-distinta",
    )

    with pytest.raises(
        ValueError,
        match="huella efectiva del prompt",
    ):
        resume_judge_evaluation(
            "test-dataset",
            "judge-eval-001",
            results_dir=tmp_path,
        )

    report = compare_human_and_judge(
        "test-dataset",
        "judge-eval-001",
        "annotator-a",
        results_dir=tmp_path,
    )

    assert report.case_ids == (
        "qc-001",
    )
    assert report.overall.n == 3
    assert report.overall.agreement == 1.0


def test_compare_human_and_judge_rejects_partial_human_annotation(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )
    create_judge_evaluation(
        "test-dataset",
        "judge-eval-001",
        split="dev",
        judge_llm_config="nova-lite",
        max_repair_attempts=0,
        results_dir=tmp_path,
    )

    annotation_data = (
        _human_annotation().model_dump()
    )
    annotation_data["criteria"] = {
        "Q1.1": annotation_data[
            "criteria"
        ][
            "Q1.1"
        ],
    }
    partial_annotation = (
        HumanAnnotation.model_validate(
            annotation_data
        )
    )
    save_human_annotation(
        "test-dataset",
        partial_annotation,
        results_dir=tmp_path,
    )

    case = load_qualitative_cases(
        "test-dataset",
        results_dir=tmp_path,
    )[0]
    decisions = {
        criterion_id: JudgeCriterionDecision(
            verdict="PASS",
            reason=f"Justificación para {criterion_id}.",
            evidence_refs=[
                "a1.i1",
            ],
        )
        for criterion_id in (
            "Q1.1",
            "Q1.2",
            "Q1.3",
        )
    }
    prediction = build_judge_case_prediction(
        case,
        decisions,
    )
    save_judge_case_prediction(
        "test-dataset",
        "judge-eval-001",
        prediction,
        results_dir=tmp_path,
    )

    with pytest.raises(
        ValueError,
        match="debe estar completa para comparar",
    ):
        compare_human_and_judge(
            "test-dataset",
            "judge-eval-001",
            "annotator-a",
            results_dir=tmp_path,
        )


def test_compare_human_and_judge_rejects_incomplete_judge_evaluation(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )
    create_judge_evaluation(
        "test-dataset",
        "judge-eval-001",
        split="dev",
        judge_llm_config="nova-lite",
        max_repair_attempts=0,
        results_dir=tmp_path,
    )

    save_human_annotation(
        "test-dataset",
        _human_annotation(),
        results_dir=tmp_path,
    )

    with pytest.raises(
        ValueError,
        match="debe estar completa antes de calcular acuerdo",
    ):
        compare_human_and_judge(
            "test-dataset",
            "judge-eval-001",
            "annotator-a",
            results_dir=tmp_path,
        )


def test_compare_human_annotators_reports_dev_agreement(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    annotation_a = _human_annotation()
    save_human_annotation(
        "test-dataset",
        annotation_a,
        results_dir=tmp_path,
    )

    annotation_b_data = (
        annotation_a.model_dump()
    )
    annotation_b_data[
        "annotator_id"
    ] = "annotator-b"
    annotation_b_data[
        "criteria"
    ][
        "Q1.2"
    ][
        "verdict"
    ] = "FAIL"
    annotation_b_data[
        "criteria"
    ][
        "Q1.2"
    ][
        "reason"
    ] = "El segundo anotador discrepa en Q1.2."

    annotation_b = (
        HumanAnnotation.model_validate(
            annotation_b_data
        )
    )
    save_human_annotation(
        "test-dataset",
        annotation_b,
        results_dir=tmp_path,
    )

    report = compare_human_annotators(
        "test-dataset",
        "annotator-a",
        "annotator-b",
        split="dev",
        results_dir=tmp_path,
    )

    assert report.dataset_id == "test-dataset"
    assert report.annotator_a_id == "annotator-a"
    assert report.annotator_b_id == "annotator-b"
    assert report.split == "dev"
    assert report.case_ids == (
        "qc-001",
    )

    assert report.overall.n == 3
    assert report.overall.agreement == pytest.approx(
        2 / 3
    )
    assert report.overall.cohen_kappa == pytest.approx(
        0.0
    )
    assert report.overall.confusion == ConfusionMatrix(
        first_pass_second_pass=2,
        first_pass_second_fail=1,
        first_fail_second_pass=0,
        first_fail_second_fail=0,
    )

    assert report.by_criterion["Q1.1"].agreement == 1.0
    assert report.by_criterion["Q1.2"].agreement == 0.0
    assert report.by_criterion["Q1.3"].agreement == 1.0
    assert report.by_criterion["Q1.4"].n == 0


def test_compare_human_annotators_requires_complete_dev_annotations(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    annotation_a = _human_annotation()
    save_human_annotation(
        "test-dataset",
        annotation_a,
        results_dir=tmp_path,
    )

    annotation_b_data = (
        annotation_a.model_dump()
    )
    annotation_b_data[
        "annotator_id"
    ] = "annotator-b"
    annotation_b_data[
        "criteria"
    ] = {
        "Q1.1": annotation_b_data[
            "criteria"
        ][
            "Q1.1"
        ],
    }

    save_human_annotation(
        "test-dataset",
        HumanAnnotation.model_validate(
            annotation_b_data
        ),
        results_dir=tmp_path,
    )

    with pytest.raises(
        ValueError,
        match="annotator-b.*debe estar completa",
    ):
        compare_human_annotators(
            "test-dataset",
            "annotator-a",
            "annotator-b",
            split="dev",
            results_dir=tmp_path,
        )


def test_compare_human_annotators_requires_distinct_annotators(
    tmp_path,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    with pytest.raises(
        ValueError,
        match="deben ser distintos",
    ):
        compare_human_annotators(
            "test-dataset",
            "annotator-a",
            "annotator-a",
            split="dev",
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
    assert data["q1_4_applicability"] == {
        "applicable": False,
        "reason": "No hubo feedback adverso explícito.",
        "triggers": [],
    }


def test_case_presentation_exposes_internal_context_as_evidence() -> None:
    case = _qualitative_case()
    first_iteration = case.attempts[0].iterations[0]

    first_iteration.context_before_decision = [
        QualitativeInternalContext(
            context_id="a1.i1.plan1",
            kind="plan",
            content=(
                "1. Examinar la puerta\n"
                "2. Encontrar la llave"
            ),
        ),
    ]
    first_iteration.context_after_decision = [
        QualitativeInternalContext(
            context_id="a1.i1.summary1",
            kind="summary",
            content=(
                "Hechos descubiertos:\n"
                "- La puerta requiere una llave."
            ),
        ),
    ]
    case.attempts[0].iterations.append(
        QualitativeIteration(
            iteration_index=2,
            assistant_content="Ahora voy a buscar la llave.",
        )
    )

    presentation = build_case_presentation(
        case
    )

    assert presentation.evidence_refs == (
        "a1.user_message",
        "a1.i1.plan1",
        "a1.i1",
        "a1.i1.summary1",
        "a1.i1.action1",
        "a1.i2",
        "a1.termination",
    )

    data = json.loads(presentation.text)
    first_iteration_data = data["attempts"][0][
        "iterations"
    ][0]

    assert first_iteration_data["context_before_decision"] == [
        {
            "ref": "a1.i1.plan1",
            "kind": "plan",
            "content": (
                "1. Examinar la puerta\n"
                "2. Encontrar la llave"
            ),
        },
    ]
    assert first_iteration_data["context_after_decision"] == [
        {
            "ref": "a1.i1.summary1",
            "kind": "summary",
            "content": (
                "Hechos descubiertos:\n"
                "- La puerta requiere una llave."
            ),
        },
    ]

    review_case = ReviewCase(
        case=case,
        split="dev",
        presentation=presentation,
        annotation=None,
    )
    rendered = _evidence_cards_html(
        review_case
    )

    assert "PLAN" in rendered
    assert "Plan previo del agente" in rendered
    assert (
        "Estrategia previa del agente; "
        "no es una observación del mundo."
    ) in rendered

    assert "CONTEXTO REDUCIDO" in rendered
    assert (
        "Contexto reducido disponible "
        "para decisiones posteriores"
    ) in rendered
    assert (
        "Representación reducida de la trayectoria anterior; "
        "no es una observación del mundo."
    ) in rendered
    assert "a1.i1.plan1" in rendered
    assert "a1.i1.summary1" in rendered


def test_case_presentation_excludes_evaluation_metadata() -> None:
    presentation = build_case_presentation(
        _qualitative_case()
    )

    assert "criteria_applicability" not in presentation.text
    assert "q1_4_applicability" in presentation.text
    assert "goal_achieved" not in presentation.text
    assert "goal_reason" not in presentation.text
    assert "agent_config" not in presentation.text
    assert "llm_config" not in presentation.text
    assert "trial_config" not in presentation.text


def test_case_presentation_exposes_q1_4_triggers_to_all_evaluators() -> None:
    case = _qualitative_case()
    case.attempts[0].iterations.append(
        QualitativeIteration(
            iteration_index=2,
            assistant_content="Voy a corregir la estrategia.",
        )
    )
    case.criteria_applicability["Q1.4"] = CriterionApplicability(
        applicable=True,
        triggers=[
            ApplicabilityTrigger(
                target_ref="a1.i2",
                components=[
                    ApplicabilityTriggerComponent(
                        kind="error_before_later_decision",
                        evidence_refs=[
                            "a1.i1.action1",
                        ],
                    ),
                ],
            ),
        ],
    )

    presentation = build_case_presentation(
        case
    )
    data = json.loads(
        presentation.text
    )

    assert data["q1_4_applicability"] == {
        "applicable": True,
        "reason": None,
        "triggers": [
            {
                "target_ref": "a1.i2",
                "components": [
                    {
                        "kind": "error_before_later_decision",
                        "evidence_refs": [
                            "a1.i1.action1",
                        ],
                    },
                ],
            },
        ],
    }


def test_case_presentation_rejects_unknown_trigger_evidence_ref() -> None:
    case = _qualitative_case()
    case.criteria_applicability["Q1.4"] = CriterionApplicability(
        applicable=True,
        triggers=[
            ApplicabilityTrigger(
                target_ref="a1.i1",
                components=[
                    ApplicabilityTriggerComponent(
                        kind="error_before_later_decision",
                        evidence_refs=[
                            "a1.i99.action1",
                        ],
                    ),
                ],
            ),
        ],
    )

    with pytest.raises(
        ValueError,
        match="referencia evidencia inexistente",
    ):
        build_case_presentation(
            case
        )


def test_llm_judge_prompt_uses_canonical_presentation_and_rubric() -> None:
    presentation = build_case_presentation(
        _qualitative_case()
    )

    prompt = build_judge_prompt(
        presentation,
        "Q1.1",
    )

    assert JUDGE_PROMPT_VERSION == (
        "planning-criterion-judge-v1"
    )
    assert presentation.text in prompt
    assert DIMENSION_DESCRIPTION in prompt
    assert MATERIALITY_RULE in prompt
    assert BOUNDARY_RULES[0] in prompt
    assert CRITERIA_BY_ID["Q1.1"].question in prompt
    assert CRITERIA_BY_ID["Q1.1"].pass_description in prompt
    assert CRITERIA_BY_ID["Q1.1"].fail_description in prompt


def test_llm_judge_criterion_uses_structured_call() -> None:
    response = LLMResponse(
        content=None,
        tool_calls=[
            ToolCall(
                id="judge-1",
                name=FINAL_RESULT_TOOL_NAME,
                arguments=json.dumps({
                    "verdict": "PASS",
                    "reason": (
                        "La decisión se mantiene compatible "
                        "con la evidencia observada."
                    ),
                    "evidence_refs": [
                        "a1.i1.action1",
                    ],
                }),
            ),
        ],
    )
    llm = MockLLMClient([
        response,
    ])
    agent = MyAgent(
        llm_client=llm,
    )

    decision = judge_case_criterion(
        agent,
        _qualitative_case(),
        "Q1.1",
        max_repair_attempts=0,
    )

    assert decision == JudgeCriterionDecision(
        verdict="PASS",
        reason=(
            "La decisión se mantiene compatible "
            "con la evidencia observada."
        ),
        evidence_refs=[
            "a1.i1.action1",
        ],
    )
    assert llm.call_count == 1
    assert len(
        llm.calls[0]["tools"]
    ) == 1
    assert (
        llm.calls[0]["tools"][0].name
        == FINAL_RESULT_TOOL_NAME
    )


def test_llm_judge_case_evaluates_only_applicable_criteria() -> None:
    responses = [
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id=f"judge-{criterion_id}",
                    name=FINAL_RESULT_TOOL_NAME,
                    arguments=json.dumps({
                        "verdict": "PASS",
                        "reason": (
                            f"Justificación para {criterion_id}."
                        ),
                        "evidence_refs": [
                            "a1.i1.action1",
                        ],
                    }),
                ),
            ],
        )
        for criterion_id in (
            "Q1.1",
            "Q1.2",
            "Q1.3",
        )
    ]
    llm = MockLLMClient(
        responses
    )
    agent = MyAgent(
        llm_client=llm,
    )

    decisions = judge_case(
        agent,
        _qualitative_case(),
        max_repair_attempts=0,
    )

    assert list(decisions) == [
        "Q1.1",
        "Q1.2",
        "Q1.3",
    ]
    assert all(
        decision.verdict == "PASS"
        for decision in decisions.values()
    )
    assert llm.call_count == 3

    prompts = [
        call["messages"][0]["content"]
        for call in llm.calls
    ]

    assert (
        CRITERIA_BY_ID["Q1.1"].question
        in prompts[0]
    )
    assert (
        CRITERIA_BY_ID["Q1.2"].question
        in prompts[1]
    )
    assert (
        CRITERIA_BY_ID["Q1.3"].question
        in prompts[2]
    )
    assert all(
        CRITERIA_BY_ID["Q1.4"].question
        not in prompt
        for prompt in prompts
    )


def test_llm_judge_case_includes_q1_4_when_applicable() -> None:
    case = _qualitative_case()
    case.attempts[0].iterations.append(
        QualitativeIteration(
            iteration_index=2,
            assistant_content=(
                "Voy a adaptar la estrategia."
            ),
        )
    )
    case.criteria_applicability["Q1.4"] = (
        CriterionApplicability(
            applicable=True,
            triggers=[
                ApplicabilityTrigger(
                    target_ref="a1.i2",
                    components=[
                        ApplicabilityTriggerComponent(
                            kind="error_before_later_decision",
                            evidence_refs=[
                                "a1.i1.action1",
                            ],
                        ),
                    ],
                ),
            ],
        )
    )

    responses = [
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id=f"judge-{criterion_id}",
                    name=FINAL_RESULT_TOOL_NAME,
                    arguments=json.dumps({
                        "verdict": "PASS",
                        "reason": (
                            f"Justificación para {criterion_id}."
                        ),
                        "evidence_refs": [
                            "a1.i1.action1",
                        ],
                    }),
                ),
            ],
        )
        for criterion_id in (
            "Q1.1",
            "Q1.2",
            "Q1.3",
            "Q1.4",
        )
    ]
    llm = MockLLMClient(
        responses
    )
    agent = MyAgent(
        llm_client=llm,
    )

    decisions = judge_case(
        agent,
        case,
        max_repair_attempts=0,
    )

    assert list(decisions) == [
        "Q1.1",
        "Q1.2",
        "Q1.3",
        "Q1.4",
    ]
    assert llm.call_count == 4
    assert (
        CRITERIA_BY_ID["Q1.4"].question
        in llm.calls[3]["messages"][0]["content"]
    )


def test_llm_judge_builds_reproducible_case_prediction() -> None:
    case = _qualitative_case()
    decisions = {
        criterion_id: JudgeCriterionDecision(
            verdict="PASS",
            reason=f"Justificación para {criterion_id}.",
            evidence_refs=[
                "a1.i1.action1",
            ],
        )
        for criterion_id in (
            "Q1.1",
            "Q1.2",
            "Q1.3",
        )
    }

    prediction = build_judge_case_prediction(
        case,
        decisions,
    )

    assert prediction == JudgeCasePrediction(
        schema_version=JUDGE_PREDICTION_SCHEMA_VERSION,
        case_schema_version=case.schema_version,
        case_view_version=case.case_view_version,
        presentation_version=PRESENTATION_VERSION,
        rubric_version=RUBRIC_VERSION,
        judge_prompt_version=JUDGE_PROMPT_VERSION,
        case_id=case.case_id,
        criteria=decisions,
    )


def test_llm_judge_prediction_requires_exactly_applicable_criteria() -> None:
    case = _qualitative_case()
    incomplete = {
        criterion_id: JudgeCriterionDecision(
            verdict="PASS",
            reason=f"Justificación para {criterion_id}.",
            evidence_refs=[
                "a1.i1.action1",
            ],
        )
        for criterion_id in (
            "Q1.1",
            "Q1.2",
        )
    }

    with pytest.raises(
        ValueError,
        match="debe contener exactamente los criterios aplicables",
    ):
        build_judge_case_prediction(
            case,
            incomplete,
        )

    with_unexpected = {
        **incomplete,
        "Q1.3": JudgeCriterionDecision(
            verdict="PASS",
            reason="Justificación para Q1.3.",
            evidence_refs=[
                "a1.i1.action1",
            ],
        ),
        "Q1.4": JudgeCriterionDecision(
            verdict="PASS",
            reason="Q1.4 no debería estar presente.",
            evidence_refs=[
                "a1.i1.action1",
            ],
        ),
    }

    with pytest.raises(
        ValueError,
        match="debe contener exactamente los criterios aplicables",
    ):
        build_judge_case_prediction(
            case,
            with_unexpected,
        )


def test_llm_judge_prediction_revalidates_evidence_refs() -> None:
    case = _qualitative_case()
    decisions = {
        criterion_id: JudgeCriterionDecision(
            verdict="PASS",
            reason=f"Justificación para {criterion_id}.",
            evidence_refs=[
                (
                    "a1.i99.action1"
                    if criterion_id == "Q1.2"
                    else "a1.i1.action1"
                ),
            ],
        )
        for criterion_id in (
            "Q1.1",
            "Q1.2",
            "Q1.3",
        )
    }

    with pytest.raises(
        ValueError,
        match="Q1.2 contiene referencias de evidencia inexistentes",
    ):
        build_judge_case_prediction(
            case,
            decisions,
        )


def test_llm_judge_rejects_non_applicable_criterion_before_call() -> None:
    llm = MockLLMClient([])
    agent = MyAgent(
        llm_client=llm,
    )

    with pytest.raises(
        ValueError,
        match="Q1.4 no aplica",
    ):
        judge_case_criterion(
            agent,
            _qualitative_case(),
            "Q1.4",
        )

    assert llm.call_count == 0


def test_llm_judge_repairs_unknown_evidence_ref() -> None:
    responses = [
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="judge-invalid-ref",
                    name=FINAL_RESULT_TOOL_NAME,
                    arguments=json.dumps({
                        "verdict": "FAIL",
                        "reason": (
                            "La decisión contradice la evidencia."
                        ),
                        "evidence_refs": [
                            "a1.i99.action1",
                        ],
                    }),
                ),
            ],
        ),
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="judge-valid-ref",
                    name=FINAL_RESULT_TOOL_NAME,
                    arguments=json.dumps({
                        "verdict": "FAIL",
                        "reason": (
                            "La decisión contradice la evidencia."
                        ),
                        "evidence_refs": [
                            "a1.i1.action1",
                        ],
                    }),
                ),
            ],
        ),
    ]
    llm = MockLLMClient(
        responses
    )
    agent = MyAgent(
        llm_client=llm,
    )

    decision = judge_case_criterion(
        agent,
        _qualitative_case(),
        "Q1.1",
        max_repair_attempts=1,
    )

    assert decision == JudgeCriterionDecision(
        verdict="FAIL",
        reason=(
            "La decisión contradice la evidencia."
        ),
        evidence_refs=[
            "a1.i1.action1",
        ],
    )
    assert llm.call_count == 2
    assert any(
        message.get("role") == "tool"
        and (
            "referencias de evidencia inexistentes"
            in message.get(
                "content",
                "",
            )
        )
        for message in llm.calls[1][
            "messages"
        ]
    )


def test_llm_judge_rejects_unknown_evidence_ref() -> None:
    response = LLMResponse(
        content=None,
        tool_calls=[
            ToolCall(
                id="judge-1",
                name=FINAL_RESULT_TOOL_NAME,
                arguments=json.dumps({
                    "verdict": "FAIL",
                    "reason": (
                        "La decisión contradice la evidencia."
                    ),
                    "evidence_refs": [
                        "a1.i99.action1",
                    ],
                }),
            ),
        ],
    )
    llm = MockLLMClient([
        response,
    ])
    agent = MyAgent(
        llm_client=llm,
    )

    with pytest.raises(
        ValueError,
        match="referencias de evidencia inexistentes",
    ):
        judge_case_criterion(
            agent,
            _qualitative_case(),
            "Q1.1",
            max_repair_attempts=0,
        )


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


def test_annotate_page_allows_selecting_existing_dataset(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create_qualitative_dataset(
        _dataset_config_for_persistence(),
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    other_dataset_config = (
        _dataset_config_for_persistence()
    )
    other_dataset_config["dataset_id"] = (
        "other-dataset"
    )

    create_qualitative_dataset(
        other_dataset_config,
        _sampled_trials_for_persistence(),
        results_dir=tmp_path,
    )

    (
        tmp_path / "incomplete-dataset"
    ).mkdir()

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
        '<option value="test-dataset" selected>'
        "test-dataset</option>"
    ) in page
    assert (
        '<option value="other-dataset">'
        "other-dataset</option>"
    ) in page
    assert "incomplete-dataset" not in page
    assert '<select' in page
    assert 'name="dataset_id"' in page
    assert 'class="navigation-control"' in page


def test_annotate_without_registered_annotator_has_no_review_case(
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

    assert (
        _default_annotator_id(
            "test-dataset"
        )
        == ""
    )

    page = _page_html(
        dataset_id="test-dataset",
        annotator_id="",
        split="all",
        status="all",
        review_cases=[],
        review_case=None,
    )

    assert "Sin anotadores registrados" in page
    assert 'id="annotation-form"' not in page
    assert 'class="review-layout"' not in page


def test_annotate_page_allows_selecting_registered_annotator(
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
        "test-a",
        results_dir=tmp_path,
    )
    create_annotator(
        "test-dataset",
        "test-b",
        results_dir=tmp_path,
    )

    monkeypatch.setattr(
        "eval.llm_judge.annotate.RESULTS_DIR",
        tmp_path,
    )

    review_cases = load_review_cases(
        "test-dataset",
        "test-b",
        results_dir=tmp_path,
    )

    page = _page_html(
        dataset_id="test-dataset",
        annotator_id="test-b",
        split="all",
        status="all",
        review_cases=review_cases,
        review_case=review_cases[0],
    )

    assert (
        '<option value="test-a">test-a</option>'
        in page
    )
    assert (
        '<option value="test-b" selected>'
        "test-b</option>"
        in page
    )
    assert (
        '<select\n'
        '        name="annotator_id"\n'
        '        class="navigation-control"\n'
        '      >'
        in page
    )
    assert 'name="new_annotator_id"' in page
    assert 'list="annotators"' not in page


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


def test_annotate_page_exposes_q1_4_trigger_navigation(
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

    case = _qualitative_case()
    case.attempts[0].iterations.append(
        QualitativeIteration(
            iteration_index=2,
            assistant_content="Voy a corregir la estrategia.",
        )
    )
    case.criteria_applicability["Q1.4"] = CriterionApplicability(
        applicable=True,
        triggers=[
            ApplicabilityTrigger(
                target_ref="a1.i2",
                components=[
                    ApplicabilityTriggerComponent(
                        kind="error_before_later_decision",
                        evidence_refs=[
                            "a1.i1.action1",
                        ],
                    ),
                ],
            ),
        ],
    )
    review_case = ReviewCase(
        case=case,
        split="dev",
        presentation=build_case_presentation(
            case
        ),
        annotation=None,
    )

    page = _page_html(
        dataset_id="test-dataset",
        annotator_id="annotator-a",
        split="all",
        status="all",
        review_cases=[review_case],
        review_case=review_case,
    )

    assert "Disparadores detectados (1)" in page
    assert "Disparador 1 · 1 error previo" in page
    assert "Oportunidad de adaptación:</strong> Iter. 2" in page
    assert "no implican por sí mismos PASS ni FAIL" in page
    assert 'data-trigger-id="D1"' in page
    assert 'data-trigger-target="a1.i1.action1"' in page
    assert "Q1.4 · D1" in page
    assert 'class="q14-trigger-marker"' in page
    assert 'criterionId === "Q1.4"' in page
    assert "scrollIntoView" in page
    assert 'class="q14-auxiliary q14-detected-triggers"' in page
    assert 'class="criterion-applicability"' in page
    assert (
        'class="criterion-applicability"\n'
        '          open'
    ) not in page
    assert (
        page.index('class="annotation-actions"')
        < page.index(
            'class="q14-auxiliary q14-detected-triggers"'
        )
    )
    assert (
        'rubricPanel?.classList.toggle('
        in page
    )


def test_annotate_page_describes_q1_4_repetition_episode(
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

    case = _qualitative_case()
    case.attempts[0].iterations.append(
        QualitativeIteration(
            iteration_index=2,
            actions=[
                QualitativeAction(
                    action_id="a1.i2.action1",
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
        )
    )
    case.criteria_applicability["Q1.4"] = CriterionApplicability(
        applicable=True,
        triggers=[
            ApplicabilityTrigger(
                target_ref="a1.i2",
                components=[
                    ApplicabilityTriggerComponent(
                        kind="consecutive_exact_repetition",
                        evidence_refs=[
                            "a1.i1.action1",
                            "a1.i2.action1",
                        ],
                    ),
                ],
            ),
        ],
    )
    review_case = ReviewCase(
        case=case,
        split="dev",
        presentation=build_case_presentation(
            case
        ),
        annotation=None,
    )

    page = _page_html(
        dataset_id="test-dataset",
        annotator_id="annotator-a",
        split="all",
        status="all",
        review_cases=[review_case],
        review_case=review_case,
    )

    assert "Disparador 1 · Repetición consecutiva" in page
    assert "Oportunidad de adaptación:</strong> Iter. 2" in page
    assert "Episodio:</strong> Iter. 1 → 2" in page


def test_annotate_page_marks_attempt_continuation_for_q1_4() -> None:
    case = _qualitative_case()
    case.attempts.append(
        QualitativeAttempt(
            attempt_index=2,
            user_message=(
                "El desafío todavía no está completado. Continuá."
            ),
            iterations=[
                QualitativeIteration(
                    iteration_index=1,
                    assistant_content="Continúo.",
                ),
            ],
            termination=AttemptTermination(
                answer="Continúo.",
            ),
        )
    )
    case.criteria_applicability["Q1.4"] = CriterionApplicability(
        applicable=True,
        triggers=[
            ApplicabilityTrigger(
                target_ref="a2.i1",
                components=[
                    ApplicabilityTriggerComponent(
                        kind="attempt_continuation",
                        evidence_refs=[
                            "a1.termination",
                            "a2.user_message",
                        ],
                    ),
                ],
            ),
        ],
    )
    review_case = ReviewCase(
        case=case,
        split="dev",
        presentation=build_case_presentation(
            case
        ),
        annotation=None,
    )

    rendered = _evidence_cards_html(
        review_case
    )

    assert 'id="attempt-2"' in rendered
    assert "Q1.4 · D1" in rendered


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
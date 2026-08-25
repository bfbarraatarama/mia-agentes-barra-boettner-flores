"""Tests de compactación de historial (issue #26, M3).

Cubren los dos ganchos del compactor:

- eviction de trazas cerradas en `_trim_run_history` (entre runs);
- compactación intra-turno en `_prepare_run_tool_context`, el caso que
  la política M2 no cubre y que produce la terminación por presupuesto.

y los invariantes que deben sobrevivir: ventana acotada, rondas de
herramientas siempre completas, fallback controlado ante un compactor
roto y tokens del compactor por LLM contabilizados en AgentResult.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from mia_agents.testing import MockLLMClient, make_recording_tool
from mia_agents.types import LLMResponse, ToolCall
from student_framework import build_agent
from student_framework.context.summarizer import (
    deterministic_history_compactor,
)


def _tool_call_response(
    call_id: str,
    text: str,
    *,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
) -> LLMResponse:
    return LLMResponse(
        content=None,
        tool_calls=[
            ToolCall(call_id, "record", json.dumps({"text": text})),
        ],
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )


def _build_compaction_agent(
    mock: MockLLMClient,
    *,
    max_history_messages: int,
    history_compaction: Any,
    trace_callback: Any = None,
    max_iterations: int = 10,
    history_compaction_input_token_threshold: int | None = None,
) -> Any:
    config: dict[str, Any] = {
        "llm_client": mock,
        "register_default_tools": False,
        "max_history_messages": max_history_messages,
        "max_iterations": max_iterations,
    }

    if history_compaction is not None:
        config["history_compaction"] = history_compaction

    if trace_callback is not None:
        config["trace_callback"] = trace_callback

    if history_compaction_input_token_threshold is not None:
        config["history_compaction_input_token_threshold"] = (
            history_compaction_input_token_threshold
        )

    agent = build_agent(config)
    tool, schema = make_recording_tool()
    agent.register_tool(tool, schema)

    return agent


class RecordingCompactor:
    """Compactor de prueba que registra qué mensajes recibió."""

    def __init__(self, summary: str = "RESUMEN") -> None:
        self.summary = summary
        self.calls: list[list[dict[str, Any]]] = []

    def __call__(self, messages: list[dict[str, Any]]) -> str:
        self.calls.append(messages)
        return self.summary


def test_eviction_compaction_replaces_trace_with_single_message():
    """Donde M2 borraba la traza, queda exactamente un mensaje resumen."""

    compactor = RecordingCompactor()
    mock = MockLLMClient([
        _tool_call_response("c1", "uno"),
        LLMResponse(content="listo el primer turno"),
        _tool_call_response("c2", "dos"),
        LLMResponse(content="listo el segundo turno"),
    ])
    agent = _build_compaction_agent(
        mock,
        max_history_messages=6,
        history_compaction=compactor,
    )

    agent.run("primer turno")
    history_before = list(agent._history)
    agent.run("segundo turno")

    # La primera eviction compacta los dos mensajes intermedios del
    # primer turno: el assistant con tool_calls y su resultado. (Al
    # cerrar el run 2, _trim_closed_run_history puede compactar
    # también la traza propia; eso es comportamiento esperado.)
    assert compactor.calls
    assert [
        message["role"]
        for message in compactor.calls[0]
    ] == ["assistant", "tool"]
    assert compactor.calls[0][0]["tool_calls"][0]["id"] == "c1"

    summary_messages = [
        message
        for message in agent._history
        if message["content"] is not None
        and message["content"].startswith("[Resumen de contexto previo]")
    ]
    # Cada compactación dejó exactamente un mensaje resumen con rol
    # user (con rol assistant sería candidato a eviction como
    # "respuesta final").
    assert len(summary_messages) == len(compactor.calls)
    assert all(
        message["role"] == "user"
        for message in summary_messages
    )
    assert "RESUMEN" in summary_messages[0]["content"]

    assert history_before[0] == {
        "role": "user",
        "content": "primer turno",
    }


def test_window_budget_respected_with_compactor():
    """len(messages) nunca supera max_history_messages con compactor."""

    budget = 6
    mock = MockLLMClient([
        _tool_call_response("c1", "uno"),
        LLMResponse(content="fin uno"),
        _tool_call_response("c2", "dos"),
        _tool_call_response("c3", "tres"),
        LLMResponse(content="fin dos"),
    ])
    agent = _build_compaction_agent(
        mock,
        max_history_messages=budget,
        history_compaction=RecordingCompactor(),
    )

    agent.run("primer turno")
    agent.run("segundo turno")

    assert mock.calls
    assert all(
        len(call["messages"]) <= budget
        for call in mock.calls
    )


def test_no_orphan_tool_messages_after_compaction():
    """Todo mensaje tool enviado tiene su assistant con el mismo id."""

    mock = MockLLMClient([
        _tool_call_response("c1", "uno"),
        _tool_call_response("c2", "dos"),
        _tool_call_response("c3", "tres"),
        _tool_call_response("c4", "cuatro"),
        LLMResponse(content="fin"),
    ])
    agent = _build_compaction_agent(
        mock,
        max_history_messages=7,
        history_compaction=RecordingCompactor(),
    )

    agent.run("tarea larga")

    for call in mock.calls:
        announced_ids: set[str] = set()

        for message in call["messages"]:
            if message.get("role") == "assistant":
                announced_ids.update(
                    tool_call["id"]
                    for tool_call in message.get("tool_calls") or []
                )

            if message.get("role") == "tool":
                assert message["tool_call_id"] in announced_ids, (
                    "Mensaje tool huérfano en la ventana enviada: "
                    f"{message['tool_call_id']}"
                )


def test_single_message_trace_range_uses_plain_delete():
    """Un rango de 1 mensaje se borra plano: compactarlo no reduce."""

    compactor = RecordingCompactor()
    agent = _build_compaction_agent(
        MockLLMClient([]),
        max_history_messages=10,
        history_compaction=compactor,
    )

    # Traza artificial cuyo rango intermedio tiene un único mensaje.
    agent._history = [
        {"role": "user", "content": "pregunta"},
        {
            "role": "tool",
            "tool_call_id": "c1",
            "name": "record",
            "content": "resultado",
        },
        {"role": "assistant", "content": "respuesta final"},
    ]

    # Si la guarda end - start >= 2 faltara, este llamado no
    # terminaría: reemplazar 1 mensaje por 1 resumen no reduce nada.
    assert agent._trim_run_history(target_length=2) is True
    assert compactor.calls == []
    assert len(agent._history) == 2


def test_intra_turn_compaction_avoids_budget_termination():
    """El caso que mata al baseline: todo el historial es turno activo."""

    responses = [
        _tool_call_response("c1", "uno"),
        _tool_call_response("c2", "dos"),
        _tool_call_response("c3", "tres"),
        _tool_call_response("c4", "cuatro"),
        LLMResponse(content="objetivo cumplido"),
    ]

    # Sin compactor: la cuarta ronda no cabe y el run muere.
    baseline_mock = MockLLMClient(list(responses[:4]))
    baseline = _build_compaction_agent(
        baseline_mock,
        max_history_messages=7,
        history_compaction=None,
    )
    baseline_result = baseline.run("tarea larga")

    assert baseline_result.error is not None
    assert "no cabe en max_history_messages" in baseline_result.error

    # Con compactor: mismas respuestas, el run llega a la final.
    compactor = RecordingCompactor()
    mock = MockLLMClient(list(responses))
    agent = _build_compaction_agent(
        mock,
        max_history_messages=7,
        history_compaction=compactor,
    )
    result = agent.run("tarea larga")

    assert result.error is None
    assert result.answer == "objetivo cumplido"
    assert len(result.steps) == 4
    assert compactor.calls

    summary_contents = [
        message["content"]
        for call in compactor.calls
        for message in call
        if isinstance(message.get("content"), str)
    ]
    # La segunda pasada incluye el resumen previo: se fusiona en vez
    # de acumularse.
    assert any(
        content.startswith("[Resumen de progreso del intento actual]")
        for content in summary_contents
    )


def test_compaction_merges_adjacent_user_messages_before_llm_call():
    """El resumen no genera turnos user consecutivos al enviar contexto."""

    mock = MockLLMClient([
        _tool_call_response("c1", "uno"),
        _tool_call_response("c2", "dos"),
        _tool_call_response("c3", "tres"),
        _tool_call_response("c4", "cuatro"),
        LLMResponse(content="objetivo cumplido"),
    ])
    agent = _build_compaction_agent(
        mock,
        max_history_messages=7,
        history_compaction=RecordingCompactor(),
    )

    result = agent.run("tarea larga")

    assert result.error is None

    messages = mock.calls[-1]["messages"]

    assert [message["role"] for message in messages] == [
        "user",
        "assistant",
        "tool",
    ]
    assert messages[0]["content"].startswith("tarea larga\n\n")
    assert (
        "[Resumen de progreso del intento actual]"
        in messages[0]["content"]
    )


def test_failing_compactor_intra_turn_falls_back_to_budget_termination():
    """Compactor roto en el turno activo: error de presupuesto, no crash."""

    events: list[dict[str, Any]] = []

    def broken_compactor(messages: list[dict[str, Any]]) -> str:
        raise RuntimeError("resumidor roto")

    mock = MockLLMClient([
        _tool_call_response("c1", "uno"),
        _tool_call_response("c2", "dos"),
        _tool_call_response("c3", "tres"),
        _tool_call_response("c4", "cuatro"),
    ])
    agent = _build_compaction_agent(
        mock,
        max_history_messages=7,
        history_compaction=broken_compactor,
        trace_callback=events.append,
    )

    result = agent.run("tarea larga")

    assert result.error is not None
    assert "no cabe en max_history_messages" in result.error

    compaction_errors = [
        event
        for event in events
        if event.get("type") == "history_compaction"
        and event.get("error") is not None
    ]
    assert compaction_errors


def test_failed_second_intra_turn_compaction_keeps_first_summary():
    """Una compactación exitosa no se revierte por un fallo posterior."""

    calls = 0

    def partially_failing_compactor(
        messages: list[dict[str, Any]],
    ) -> str:
        nonlocal calls
        calls += 1

        if calls == 1:
            return "PRIMER RESUMEN"

        raise RuntimeError("falló la segunda compactación")

    agent = _build_compaction_agent(
        MockLLMClient([]),
        max_history_messages=7,
        history_compaction=partially_failing_compactor,
    )

    agent._history = [
        {
            "role": "user",
            "content": "tarea larga",
        },
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [{"id": "c1"}],
        },
        {
            "role": "tool",
            "tool_call_id": "c1",
            "content": "uno",
        },
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [{"id": "c2"}],
        },
        {
            "role": "tool",
            "tool_call_id": "c2",
            "content": "dos",
        },
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [{"id": "c3"}],
        },
        {
            "role": "tool",
            "tool_call_id": "c3",
            "content": "tres",
        },
    ]

    compacted = agent._compact_active_turn(
        active_turn_start=0,
        target_length=5,
    )

    assert compacted is False
    assert calls == 2
    assert [
        message["role"]
        for message in agent._history
    ] == [
        "user",
        "user",
        "assistant",
        "tool",
        "assistant",
        "tool",
    ]
    assert agent._history[1]["content"] == (
        "[Resumen de progreso del intento actual]\n"
        "PRIMER RESUMEN"
    )


def test_failing_compactor_degrades_to_m2_eviction():
    """Compactor roto en la eviction: se borra plano, como en M2."""

    def broken_compactor(messages: list[dict[str, Any]]) -> str:
        raise RuntimeError("resumidor roto")

    mock = MockLLMClient([
        _tool_call_response("c1", "uno"),
        LLMResponse(content="fin uno"),
        _tool_call_response("c2", "dos"),
        LLMResponse(content="fin dos"),
    ])
    agent = _build_compaction_agent(
        mock,
        max_history_messages=6,
        history_compaction=broken_compactor,
    )

    agent.run("primer turno")
    result = agent.run("segundo turno")

    assert result.error is None
    assert all(
        not (message.get("content") or "").startswith("[Resumen")
        for message in agent._history
    )


def test_llm_compactor_tokens_accumulate_in_agent_result():
    """Los tokens del resumidor por LLM entran en AgentResult."""

    summary_arguments = json.dumps({
        "discovered_facts": ["la caja azul contiene una llave"],
        "attempted_actions": ["record(uno) → ok"],
        "open_subgoals": ["abrir la puerta"],
        "dead_ends": [],
    })

    def summary_response() -> LLMResponse:
        return LLMResponse(
            content=None,
            tool_calls=[
                ToolCall("s1", "final_result", summary_arguments),
            ],
            input_tokens=100,
            output_tokens=50,
        )

    events: list[dict[str, Any]] = []
    mock = MockLLMClient([
        _tool_call_response("c1", "uno", input_tokens=10, output_tokens=5),
        _tool_call_response("c2", "dos", input_tokens=10, output_tokens=5),
        _tool_call_response("c3", "tres", input_tokens=10, output_tokens=5),
        _tool_call_response("c4", "cuatro", input_tokens=10, output_tokens=5),
        summary_response(),
        summary_response(),
        LLMResponse(
            content="objetivo cumplido",
            input_tokens=10,
            output_tokens=5,
        ),
    ])
    agent = _build_compaction_agent(
        mock,
        max_history_messages=7,
        history_compaction="llm",
        trace_callback=events.append,
    )

    result = agent.run("tarea larga")

    assert result.error is None
    # 5 llamadas del agente (10/5) + 2 del compactor (100/50).
    assert result.input_tokens == 5 * 10 + 2 * 100
    assert result.output_tokens == 5 * 5 + 2 * 50

    compaction_calls = [
        event
        for event in events
        if event.get("type") == "llm_call"
        and event.get("purpose") == "history_compaction"
    ]
    assert len(compaction_calls) == 2

    compaction_events = [
        event
        for event in events
        if event.get("type") == "history_compaction"
        and event.get("error") is None
    ]
    assert len(compaction_events) == 2

    for event in compaction_events:
        assert "Hechos descubiertos:" in event["summary"]
        assert event["summary_chars"] == len(event["summary"])

    # El resumen estructurado quedó renderizado en el historial.
    assert any(
        "Hechos descubiertos" in (message.get("content") or "")
        for message in agent._history
    )


def test_input_token_threshold_compacts_before_next_agent_call():
    """El trigger se consume justo antes de la siguiente llamada."""

    events: list[dict[str, Any]] = []
    compactor = RecordingCompactor()

    mock = MockLLMClient([
        _tool_call_response("c1", "uno", input_tokens=10),
        _tool_call_response("c2", "dos", input_tokens=10),
        _tool_call_response("c3", "tres", input_tokens=101),
        _tool_call_response("c4", "cuatro", input_tokens=10),
        LLMResponse(content="objetivo cumplido", input_tokens=10),
    ])
    agent = _build_compaction_agent(
        mock,
        max_history_messages=100,
        history_compaction=compactor,
        trace_callback=events.append,
        history_compaction_input_token_threshold=100,
    )

    result = agent.run("tarea larga")

    assert result.error is None
    assert result.answer == "objetivo cumplido"
    assert len(result.steps) == 4
    assert len(compactor.calls) == 1

    assert [
        message["role"]
        for message in compactor.calls[0]
    ] == ["assistant", "tool"]
    assert compactor.calls[0][0]["tool_calls"][0]["id"] == "c1"

    # c3 produce el trigger; c4 es la primera llamada que consume
    # el historial ya compactado.
    assert any(
        "[Resumen de progreso del intento actual]"
        in (message.get("content") or "")
        for message in mock.calls[3]["messages"]
    )

    trigger_events = [
        event
        for event in events
        if event.get("type") == "history_compaction_trigger"
    ]

    assert trigger_events == [{
        "type": "history_compaction_trigger",
        "reason": "input_tokens",
        "input_tokens": 101,
        "threshold": 100,
    }]


def test_input_token_threshold_does_not_compact_at_threshold():
    """Igualar el threshold no activa la compactación."""

    compactor = RecordingCompactor()

    mock = MockLLMClient([
        _tool_call_response("c1", "uno", input_tokens=100),
        _tool_call_response("c2", "dos", input_tokens=100),
        _tool_call_response("c3", "tres", input_tokens=100),
        _tool_call_response("c4", "cuatro", input_tokens=100),
        LLMResponse(content="objetivo cumplido", input_tokens=100),
    ])
    agent = _build_compaction_agent(
        mock,
        max_history_messages=100,
        history_compaction=compactor,
        history_compaction_input_token_threshold=100,
    )

    result = agent.run("tarea larga")

    assert result.error is None
    assert result.answer == "objetivo cumplido"
    assert compactor.calls == []


def test_input_token_trigger_waits_for_a_later_run():
    """Una respuesta final sólo se resume si luego existe otra llamada."""

    compactor = RecordingCompactor()

    mock = MockLLMClient([
        _tool_call_response("c1", "uno", input_tokens=10),
        _tool_call_response("c2", "dos", input_tokens=10),
        _tool_call_response("c3", "tres", input_tokens=10),
        LLMResponse(content="fin del primer run", input_tokens=101),
        LLMResponse(content="fin del segundo run", input_tokens=10),
    ])
    agent = _build_compaction_agent(
        mock,
        max_history_messages=100,
        history_compaction=compactor,
        history_compaction_input_token_threshold=100,
    )

    first_result = agent.run("primer turno")

    assert first_result.error is None
    assert first_result.answer == "fin del primer run"
    assert compactor.calls == []

    second_result = agent.run("segundo turno")

    assert second_result.error is None
    assert second_result.answer == "fin del segundo run"
    assert len(compactor.calls) == 1

    assert [
        message["role"]
        for message in compactor.calls[0]
    ] == [
        "assistant",
        "tool",
        "assistant",
        "tool",
        "assistant",
        "tool",
    ]

    assert any(
        "segundo turno" in (message.get("content") or "")
        for message in mock.calls[-1]["messages"]
    )


def test_failing_token_triggered_compaction_does_not_terminate_run():
    """Un fallo de la compactación disparada por tokens no mata el run."""

    events: list[dict[str, Any]] = []

    def broken_compactor(messages: list[dict[str, Any]]) -> str:
        raise RuntimeError("resumidor roto")

    mock = MockLLMClient([
        _tool_call_response("c1", "uno", input_tokens=10),
        _tool_call_response("c2", "dos", input_tokens=10),
        _tool_call_response("c3", "tres", input_tokens=101),
        _tool_call_response("c4", "cuatro", input_tokens=10),
        LLMResponse(content="objetivo cumplido", input_tokens=10),
    ])
    agent = _build_compaction_agent(
        mock,
        max_history_messages=100,
        history_compaction=broken_compactor,
        trace_callback=events.append,
        history_compaction_input_token_threshold=100,
    )

    result = agent.run("tarea larga")

    assert result.error is None
    assert result.answer == "objetivo cumplido"
    assert len(result.steps) == 4

    assert any(
        event.get("type") == "history_compaction_trigger"
        and event.get("reason") == "input_tokens"
        for event in events
    )
    assert any(
        event.get("type") == "history_compaction"
        and event.get("error") is not None
        for event in events
    )


def test_input_token_threshold_disabled_by_default():
    """Sin umbral no aparece la nueva compactación proactiva."""

    compactor = RecordingCompactor()

    mock = MockLLMClient([
        _tool_call_response("c1", "uno", input_tokens=1000),
        _tool_call_response("c2", "dos", input_tokens=1000),
        _tool_call_response("c3", "tres", input_tokens=1000),
        _tool_call_response("c4", "cuatro", input_tokens=1000),
        LLMResponse(content="objetivo cumplido", input_tokens=1000),
    ])
    agent = _build_compaction_agent(
        mock,
        max_history_messages=100,
        history_compaction=compactor,
    )

    result = agent.run("tarea larga")

    assert result.error is None
    assert result.answer == "objetivo cumplido"
    assert compactor.calls == []
    assert agent._history_compaction_input_token_threshold is None


def test_non_positive_input_token_threshold_rejected():
    """El trigger configurado debe tener un umbral estrictamente positivo."""

    with pytest.raises(
        ValueError,
        match="history_compaction_input_token_threshold debe ser positivo",
    ):
        build_agent({
            "llm_client": MockLLMClient([]),
            "register_default_tools": False,
            "history_compaction_input_token_threshold": 0,
        })


def test_compactor_disabled_by_default():
    """Sin history_compaction, build_agent conserva la política M2."""

    agent = build_agent({
        "llm_client": MockLLMClient([]),
        "register_default_tools": False,
    })

    assert agent._history_compactor is None


def test_build_agent_rejects_unknown_compaction_strategy():
    with pytest.raises(ValueError):
        build_agent({
            "llm_client": MockLLMClient([]),
            "register_default_tools": False,
            "history_compaction": "resumir-magicamente",
        })


def test_build_agent_forwards_llm_compactor_repair_attempts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, int] = {}

    def fake_make_llm_history_compactor(
        agent: Any,
        *,
        max_repair_attempts: int = 1,
    ) -> Any:
        captured["max_repair_attempts"] = max_repair_attempts
        return lambda messages: "RESUMEN"

    monkeypatch.setattr(
        "student_framework.make_llm_history_compactor",
        fake_make_llm_history_compactor,
    )

    build_agent({
        "llm_client": MockLLMClient([]),
        "register_default_tools": False,
        "history_compaction": "llm",
        "history_compaction_repair_max_attempts": 0,
    })

    assert captured["max_repair_attempts"] == 0


def test_negative_history_compaction_repair_attempts_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="history_compaction_repair_max_attempts no puede ser negativo",
    ):
        build_agent({
            "llm_client": MockLLMClient([]),
            "register_default_tools": False,
            "history_compaction": "llm",
            "history_compaction_repair_max_attempts": -1,
        })


def test_negative_keep_recent_rounds_rejected():
    with pytest.raises(ValueError):
        build_agent({
            "llm_client": MockLLMClient([]),
            "register_default_tools": False,
            "compaction_keep_recent_rounds": -1,
        })


def test_deterministic_compactor_folds_and_dedupes_actions():
    messages = [
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "c1",
                    "type": "function",
                    "function": {
                        "name": "record",
                        "arguments": '{"text": "uno"}',
                    },
                },
            ],
        },
        {
            "role": "tool",
            "tool_call_id": "c1",
            "name": "record",
            "content": "recorded:uno",
        },
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "c2",
                    "type": "function",
                    "function": {
                        "name": "record",
                        "arguments": '{"text": "uno"}',
                    },
                },
            ],
        },
        {
            "role": "tool",
            "tool_call_id": "c2",
            "name": "record",
            "content": "recorded:uno",
        },
    ]

    summary = deterministic_history_compactor(messages)

    assert summary.count("record(") == 1
    assert "(x2)" in summary
    assert "recorded:uno" in summary


def test_deterministic_compactor_preserves_assistant_content_with_tool_calls():
    messages = [
        {
            "role": "assistant",
            "content": "Primero voy a registrar esta pista.",
            "tool_calls": [
                {
                    "id": "c1",
                    "type": "function",
                    "function": {
                        "name": "record",
                        "arguments": '{"text": "pista"}',
                    },
                },
            ],
        },
        {
            "role": "tool",
            "tool_call_id": "c1",
            "name": "record",
            "content": "recorded:pista",
        },
    ]

    summary = deterministic_history_compactor(messages)

    assert "Primero voy a registrar esta pista." in summary
    assert "record(" in summary
    assert "recorded:pista" in summary


def test_deterministic_compactor_preserves_distinct_observations_on_truncation_collision():
    common_prefix = "A" * 220
    messages = [
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "c1",
                    "type": "function",
                    "function": {
                        "name": "examine",
                        "arguments": '{"target": "documento"}',
                    },
                },
            ],
        },
        {
            "role": "tool",
            "tool_call_id": "c1",
            "name": "examine",
            "content": common_prefix + " Código: 7391",
        },
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "c2",
                    "type": "function",
                    "function": {
                        "name": "examine",
                        "arguments": '{"target": "documento"}',
                    },
                },
            ],
        },
        {
            "role": "tool",
            "tool_call_id": "c2",
            "name": "examine",
            "content": common_prefix + " Código: 4826",
        },
    ]

    summary = deterministic_history_compactor(messages)

    assert "(x2)" not in summary
    assert "7391" in summary
    assert "4826" in summary

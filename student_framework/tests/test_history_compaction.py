"""Tests de compactación de historial (issue #26, M3).

Cubren los dos ganchos del compactor:

- eviction de trazas cerradas en `_trim_run_history` (entre runs);
- compactación intra-turno en `_prepare_run_tool_context`, el caso que
  la política M2 no cubre y que produce la terminación por presupuesto.

Y los invariantes que deben sobrevivir: ventana acotada, rondas de
herramientas siempre completas, degradación a M2 ante un compactor roto
y tokens del compactor por LLM contabilizados en AgentResult.
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


def test_failing_compactor_degrades_to_m2_intra_turn():
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

    # El resumen estructurado quedó renderizado en el historial.
    assert any(
        "Hechos descubiertos" in (message.get("content") or "")
        for message in agent._history
    )


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

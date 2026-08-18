import json

import pytest
from pydantic import BaseModel

from mia_agents.testing import MockLLMClient
from mia_agents.types import LLMResponse, ToolCall, ToolSchema
from student_framework import build_agent


class ExamineArguments(BaseModel):
    target: str


class UseArguments(BaseModel):
    item: str
    target: str


def test_run_repairs_invalid_tool_call_when_enabled() -> None:
    def examine(target: str) -> str:
        raise AssertionError("La llamada original inválida no debe ejecutarse.")

    def use(item: str, target: str) -> str:
        return f"{item}:{target}"

    examine_schema = ToolSchema.from_model(
        ExamineArguments,
        name="examine",
        description="Examina un objeto.",
    )
    use_schema = ToolSchema.from_model(
        UseArguments,
        name="use",
        description="Usa un objeto sobre otro.",
    )

    original_arguments = json.dumps({
        "item": "llave",
    })
    repaired_arguments = json.dumps({
        "item": "llave",
        "target": "cofre",
    })

    mock = MockLLMClient([
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="examine-1",
                    name="examine",
                    arguments=original_arguments,
                )
            ],
            input_tokens=100,
            output_tokens=20,
        ),
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="use-1",
                    name="use",
                    arguments=repaired_arguments,
                )
            ],
            input_tokens=30,
            output_tokens=10,
        ),
        LLMResponse(
            content="hecho",
            input_tokens=200,
            output_tokens=30,
        ),
    ])

    trace_events: list[dict[str, object]] = []

    agent = build_agent({
        "llm_client": mock,
        "register_default_tools": False,
        "tool_call_repair_max_attempts": 1,
        "trace_callback": trace_events.append,
    })
    agent.register_tool(examine, examine_schema)
    agent.register_tool(use, use_schema)

    result = agent.run("Abrí el cofre con la llave.")

    assert result.answer == "hecho"
    assert len(result.steps) == 1

    step = result.steps[0]
    assert step.tool_name == "use"
    assert step.tool_input == repaired_arguments
    assert step.tool_output == "llave:cofre"
    assert step.error is None

    assert result.input_tokens == 330
    assert result.output_tokens == 60
    assert mock.call_count == 3

    final_call_messages = mock.calls[2]["messages"]

    assistant_message = next(
        message
        for message in final_call_messages
        if message.get("role") == "assistant"
        and message.get("tool_calls")
    )
    effective_call = assistant_message["tool_calls"][0]

    assert effective_call["id"] == "use-1"
    assert effective_call["function"]["name"] == "use"
    assert effective_call["function"]["arguments"] == repaired_arguments

    tool_message = next(
        message
        for message in final_call_messages
        if message.get("role") == "tool"
    )

    assert tool_message["tool_call_id"] == "use-1"
    assert tool_message["name"] == "use"
    assert tool_message["content"] == "llave:cofre"

    llm_events = [
        event
        for event in trace_events
        if event["type"] == "llm_call"
    ]

    assert [event["purpose"] for event in llm_events] == [
        "agent",
        "tool_call_repair",
        "agent",
    ]


def test_repair_tool_call_can_switch_candidate_tool() -> None:
    def examine(target: str) -> str:
        return target

    def use(item: str, target: str) -> str:
        return f"{item}:{target}"

    examine_schema = ToolSchema.from_model(
        ExamineArguments,
        name="examine",
        description="Examina un objeto.",
    )
    use_schema = ToolSchema.from_model(
        UseArguments,
        name="use",
        description="Usa un objeto sobre otro.",
    )
    tools = [
        examine_schema,
        use_schema,
    ]

    mock = MockLLMClient([
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="use-1",
                    name="use",
                    arguments=json.dumps({
                        "item": "llave",
                        "target": "cofre",
                    }),
                )
            ],
        ),
    ])

    agent = build_agent({
        "llm_client": mock,
        "register_default_tools": False,
    })
    agent.register_tool(examine, examine_schema)
    agent.register_tool(use, use_schema)

    original_call = ToolCall(
        id="examine-1",
        name="examine",
        arguments=json.dumps({
            "item": "llave",
        }),
    )

    try:
        agent._validate_tool_call(original_call)
    except ValueError as e:
        error = str(e)
    else:
        raise AssertionError("La llamada original debía ser inválida.")

    result = agent._repair_tool_call(
        tool_call=original_call,
        error=error,
        max_attempts=1,
    )

    assert result.name == "use"
    assert json.loads(result.arguments) == {
        "item": "llave",
        "target": "cofre",
    }

    assert mock.call_count == 1
    assert mock.calls[0]["tools"] == tools


def test_validate_tool_call_rejects_structural_errors_without_executing_tool() -> None:
    def examine(target: str) -> str:
        raise AssertionError("La herramienta no debe ejecutarse durante la validación.")

    examine_schema = ToolSchema.from_callable(examine)

    agent = build_agent({
        "llm_client": MockLLMClient([]),
        "register_default_tools": False,
    })
    agent.register_tool(examine, examine_schema)

    valid_call = ToolCall(
        id="examine-valid",
        name="examine",
        arguments=json.dumps({
            "target": "puerta",
        }),
    )

    assert agent._validate_tool_call(valid_call) == {
        "target": "puerta",
    }

    with pytest.raises(ValueError, match="Herramienta desconocida"):
        agent._validate_tool_call(
            ToolCall(
                id="unknown-tool",
                name="use",
                arguments="{}",
            )
        )

    with pytest.raises(ValueError, match="Argumentos JSON inválidos"):
        agent._validate_tool_call(
            ToolCall(
                id="invalid-json",
                name="examine",
                arguments="{",
            )
        )

    with pytest.raises(
        ValueError,
        match="Los argumentos de la herramienta deben ser un objeto JSON",
    ):
        agent._validate_tool_call(
            ToolCall(
                id="non-object",
                name="examine",
                arguments='["puerta"]',
            )
        )

    with pytest.raises(ValueError):
        agent._validate_tool_call(
            ToolCall(
                id="invalid-signature",
                name="examine",
                arguments=json.dumps({
                    "obj": "puerta",
                }),
            )
        )
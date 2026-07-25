import json

from mia_agents.testing import MockLLMClient, make_recording_tool
from mia_agents.types import LLMResponse, ToolCall
from student_framework.agent import MyAgent


MAX_ITERATIONS_MESSAGE = (
    "Se alcanzó el límite de {limit} iteraciones "
    "sin obtener una respuesta final."
)


def _tool_call_response(
    *,
    call_id: str,
    tool_name: str,
    text: str,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
) -> LLMResponse:
    return LLMResponse(
        content=None,
        tool_calls=[
            ToolCall(
                id=call_id,
                name=tool_name,
                arguments=json.dumps({"text": text}),
            )
        ],
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )


def test_run_returns_explicit_result_after_one_iteration() -> None:
    """Una tool call en la única iteración termina de forma explícita."""

    tool, schema = make_recording_tool(
        return_value="recorded:uno",
    )
    mock = MockLLMClient([
        _tool_call_response(
            call_id="call-1",
            tool_name=schema.name,
            text="uno",
            input_tokens=3,
            output_tokens=5,
        ),
    ])

    agent = MyAgent(
        llm_client=mock,
        max_iterations=1,
        max_history_messages=10,
    )
    agent.register_tool(tool, schema)

    result = agent.run("procesá una herramienta")
    expected_message = MAX_ITERATIONS_MESSAGE.format(limit=1)

    assert mock.call_count == 1
    assert tool.calls == [{"text": "uno"}]

    assert result.answer == expected_message
    assert result.error == expected_message
    assert result.input_tokens == 3
    assert result.output_tokens == 5

    assert len(result.steps) == 1
    assert result.steps[0].tool_name == schema.name
    assert result.steps[0].tool_input == json.dumps({
        "text": "uno",
    })
    assert result.steps[0].tool_output == "recorded:uno"
    assert result.steps[0].error is None

    assert agent._history[-1] == {
        "role": "assistant",
        "content": expected_message,
    }


def test_run_preserves_steps_and_tokens_after_multiple_iterations(
) -> None:
    """El agotamiento conserva herramientas y tokens acumulados."""

    tool, schema = make_recording_tool(
        return_value="recorded",
    )
    mock = MockLLMClient([
        _tool_call_response(
            call_id="call-1",
            tool_name=schema.name,
            text="uno",
            input_tokens=2,
            output_tokens=3,
        ),
        _tool_call_response(
            call_id="call-2",
            tool_name=schema.name,
            text="dos",
            input_tokens=5,
            output_tokens=7,
        ),
    ])

    agent = MyAgent(
        llm_client=mock,
        max_iterations=2,
        max_history_messages=10,
    )
    agent.register_tool(tool, schema)

    result = agent.run("ejecutá dos iteraciones")
    expected_message = MAX_ITERATIONS_MESSAGE.format(limit=2)

    assert mock.call_count == 2
    assert tool.calls == [
        {"text": "uno"},
        {"text": "dos"},
    ]

    assert result.answer == expected_message
    assert result.error == expected_message
    assert result.input_tokens == 7
    assert result.output_tokens == 10

    assert len(result.steps) == 2
    assert [step.tool_name for step in result.steps] == [
        schema.name,
        schema.name,
    ]
    assert [step.error for step in result.steps] == [
        None,
        None,
    ]


def test_run_returns_normal_answer_on_last_allowed_iteration(
) -> None:
    """Una respuesta final en la última iteración no es agotamiento."""

    tool, schema = make_recording_tool(
        return_value="recorded:uno",
    )
    mock = MockLLMClient([
        _tool_call_response(
            call_id="call-1",
            tool_name=schema.name,
            text="uno",
        ),
        LLMResponse(content="respuesta final"),
    ])

    agent = MyAgent(
        llm_client=mock,
        max_iterations=2,
        max_history_messages=10,
    )
    agent.register_tool(tool, schema)

    result = agent.run("resolvé la solicitud")

    assert mock.call_count == 2
    assert tool.calls == [{"text": "uno"}]

    assert result.answer == "respuesta final"
    assert result.error is None
    assert len(result.steps) == 1

    assert agent._history[-1] == {
        "role": "assistant",
        "content": "respuesta final",
    }


def test_run_distinguishes_tool_error_from_iteration_exhaustion(
) -> None:
    """El error de herramienta se conserva aparte de la causa terminal."""

    mock = MockLLMClient([
        _tool_call_response(
            call_id="call-1",
            tool_name="missing_tool",
            text="uno",
        ),
    ])

    agent = MyAgent(
        llm_client=mock,
        max_iterations=1,
        max_history_messages=10,
    )

    result = agent.run("usá una herramienta inexistente")
    expected_message = MAX_ITERATIONS_MESSAGE.format(limit=1)

    assert mock.call_count == 1
    assert result.answer == expected_message
    assert result.error == expected_message

    assert len(result.steps) == 1
    assert result.steps[0].tool_name == "missing_tool"
    assert result.steps[0].tool_output == ""
    assert result.steps[0].error == (
        "Herramienta desconocida: missing_tool"
    )

    assert agent._history[-1] == {
        "role": "assistant",
        "content": expected_message,
    }


def test_run_closes_history_before_a_later_invocation() -> None:
    """Una ejecución posterior parte de un turno cerrado."""

    tool, schema = make_recording_tool(
        return_value="recorded:uno",
    )
    mock = MockLLMClient([
        _tool_call_response(
            call_id="call-1",
            tool_name=schema.name,
            text="uno",
        ),
        LLMResponse(content="respuesta posterior"),
    ])

    agent = MyAgent(
        llm_client=mock,
        max_iterations=1,
        max_history_messages=4,
    )
    agent.register_tool(tool, schema)

    first_result = agent.run("primer turno")
    expected_message = MAX_ITERATIONS_MESSAGE.format(limit=1)

    assert first_result.answer == expected_message
    assert agent._history == [
        {
            "role": "user",
            "content": "primer turno",
        },
        {
            "role": "assistant",
            "content": expected_message,
        },
    ]

    second_result = agent.run("segundo turno")

    assert second_result.answer == "respuesta posterior"
    assert mock.call_count == 2
    assert mock.calls[1]["messages"] == [
        {
            "role": "user",
            "content": "primer turno",
        },
        {
            "role": "assistant",
            "content": expected_message,
        },
        {
            "role": "user",
            "content": "segundo turno",
        },
    ]
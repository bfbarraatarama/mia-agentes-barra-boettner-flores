from eval.analyses.context_analysis import analyze_context, render_markdown


def _trial(*, budget_terminated: bool) -> dict:
    error = (
        "Se requirió una herramienta, pero el contexto necesario "
        "para continuar no cabe en max_history_messages=100."
        if budget_terminated
        else None
    )

    return {
        "trial_index": 1,
        "attempts": [
            {
                "attempt_index": 1,
                "agent_result": {
                    "input_tokens": 10,
                    "output_tokens": 5,
                    "steps": [],
                    "error": error,
                },
                "trace": [],
            },
        ],
    }


def test_context_analysis_keeps_logical_cases_separate() -> None:
    run_source = {
        "run_id": "test-run",
        "manifest": {
            "agent_configs": {
                "minimal": {
                    "max_history_messages": 100,
                },
            },
        },
        "result": {
            "results": [
                {
                    "agent_config": "minimal",
                    "llm_config": "nova-lite",
                    "trial_config": "multi_attempt",
                    "scenario": "study-with-key",
                    "trials": [
                        _trial(budget_terminated=True),
                    ],
                },
                {
                    "agent_config": "minimal",
                    "llm_config": "nova-lite",
                    "trial_config": "multi_attempt",
                    "scenario": "color-locks",
                    "trials": [
                        _trial(budget_terminated=False),
                    ],
                },
                {
                    "agent_config": "minimal",
                    "llm_config": "nova-lite",
                    "trial_config": "single_attempt",
                    "scenario": "study-with-key",
                    "trials": [
                        _trial(budget_terminated=False),
                    ],
                },
            ],
        },
    }

    analysis = analyze_context([run_source])

    assert [
        (
            case["agent_config"],
            case["llm_config"],
            case["trial_config"],
            case["scenario"],
            case["stats"]["budget_terminated_trials"],
        )
        for case in analysis["cases"]
    ] == [
        (
            "minimal",
            "nova-lite",
            "multi_attempt",
            "study-with-key",
            1,
        ),
        (
            "minimal",
            "nova-lite",
            "multi_attempt",
            "color-locks",
            0,
        ),
        (
            "minimal",
            "nova-lite",
            "single_attempt",
            "study-with-key",
            0,
        ),
    ]


def test_context_analysis_markdown_reports_logical_cases() -> None:
    run_source = {
        "run_id": "test-run",
        "manifest": {
            "agent_configs": {
                "minimal": {
                    "max_history_messages": 100,
                },
            },
        },
        "result": {
            "results": [
                {
                    "agent_config": "minimal",
                    "llm_config": "nova-lite",
                    "trial_config": "multi_attempt",
                    "scenario": "study-with-key",
                    "trials": [
                        _trial(budget_terminated=True),
                    ],
                },
            ],
        },
    }

    markdown = render_markdown(analyze_context([run_source]))

    assert "## Por caso" in markdown
    assert (
        "| Agente | Modelo | Trial config | Escenario | Ventana | "
        "Trials | Presupuesto | Compactaciones | Repetición |"
    ) in markdown
    assert (
        "| `minimal` | `nova-lite` | `multi_attempt` | "
        "`study-with-key` | 100 | 1 | 1 | 0 / 0 | n/a |"
    ) in markdown
    assert "### `minimal` / `nova-lite` / `multi_attempt`" not in markdown


def test_context_analysis_aggregates_runs_and_compaction_activity() -> None:
    def run_source(
        run_id: str,
        *,
        compaction_failed: bool,
        compaction_input_tokens: int,
        compaction_output_tokens: int,
    ) -> dict:
        return {
            "run_id": run_id,
            "manifest": {
                "agent_configs": {
                    "minimal_summary": {
                        "max_history_messages": 100,
                    },
                },
            },
            "result": {
                "results": [
                    {
                        "agent_config": "minimal_summary",
                        "llm_config": "nova-lite",
                        "trial_config": "multi_attempt",
                        "scenario": "study-with-key",
                        "trials": [
                            {
                                "trial_index": 1,
                                "attempts": [
                                    {
                                        "attempt_index": 1,
                                        "agent_result": {
                                            "input_tokens": 100,
                                            "output_tokens": 20,
                                            "steps": [],
                                            "error": None,
                                        },
                                        "trace": [
                                            {
                                                "type": "history_compaction",
                                                "error": (
                                                    "falló"
                                                    if compaction_failed
                                                    else None
                                                ),
                                            },
                                            {
                                                "type": "llm_call",
                                                "purpose": "history_compaction",
                                                "response": {
                                                    "input_tokens": (
                                                        compaction_input_tokens
                                                    ),
                                                    "output_tokens": (
                                                        compaction_output_tokens
                                                    ),
                                                },
                                            },
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        }

    analysis = analyze_context([
        run_source(
            "run-a",
            compaction_failed=False,
            compaction_input_tokens=30,
            compaction_output_tokens=10,
        ),
        run_source(
            "run-b",
            compaction_failed=True,
            compaction_input_tokens=40,
            compaction_output_tokens=15,
        ),
    ])

    assert analysis["run_ids"] == ["run-a", "run-b"]

    assert len(analysis["cases"]) == 1
    case = analysis["cases"][0]

    assert case["agent_config"] == "minimal_summary"
    assert case["llm_config"] == "nova-lite"
    assert case["trial_config"] == "multi_attempt"
    assert case["scenario"] == "study-with-key"

    stats = case["stats"]
    assert stats["trials"] == 2
    assert stats["attempts"] == 2
    assert stats["compaction_events"] == 2
    assert stats["compaction_failures"] == 1
    assert stats["compaction_llm_calls"] == 2
    assert stats["compaction_input_tokens"] == 70
    assert stats["compaction_output_tokens"] == 25

    assert analysis["totals"]["compaction_events"] == 2
    assert analysis["totals"]["compaction_failures"] == 1


def test_context_analysis_characterizes_budget_termination() -> None:
    run_source = {
        "run_id": "test-run",
        "manifest": {
            "agent_configs": {
                "minimal": {
                    "max_history_messages": 100,
                },
            },
        },
        "result": {
            "results": [
                {
                    "agent_config": "minimal",
                    "llm_config": "nova-lite",
                    "trial_config": "multi_attempt",
                    "scenario": "study-with-key",
                    "trials": [
                        {
                            "trial_index": 1,
                            "attempts": [
                                {
                                    "attempt_index": 1,
                                    "agent_result": {
                                        "input_tokens": 10,
                                        "output_tokens": 5,
                                        "steps": [],
                                        "error": None,
                                    },
                                    "trace": [],
                                },
                                {
                                    "attempt_index": 2,
                                    "agent_result": {
                                        "input_tokens": 20,
                                        "output_tokens": 8,
                                        "steps": [],
                                        "error": (
                                            "Se requirió una herramienta, "
                                            "pero el contexto necesario "
                                            "para continuar no cabe en "
                                            "max_history_messages=100."
                                        ),
                                    },
                                    "trace": [
                                        {
                                            "type": "llm_call",
                                            "purpose": "agent",
                                            "messages": [
                                                {"role": "user"}
                                            ] * 99,
                                            "response": {
                                                "tool_calls": [
                                                    {"name": "examine"},
                                                ],
                                            },
                                        },
                                        {
                                            "type": "llm_call",
                                            "purpose": "agent",
                                            "messages": [
                                                {"role": "user"}
                                            ] * 100,
                                            "response": {
                                                "tool_calls": [
                                                    {"name": "examine"},
                                                ],
                                            },
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    }

    analysis = analyze_context([run_source])
    stats = analysis["cases"][0]["stats"]

    assert stats["budget_terminated_trials"] == 1
    assert stats["budget_terminated_attempts"] == 1
    assert stats["budget_termination_by_attempt_index"] == {2: 1}
    assert stats["iterations_at_budget_termination"] == {
        "min": 2,
        "mean": 2.0,
        "max": 2,
    }
    assert stats["max_messages_seen"] == 100
    assert stats["llm_calls_at_window_limit"] == 1

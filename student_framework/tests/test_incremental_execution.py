from __future__ import annotations

import json

import pytest

from eval import persistence
from eval.configs.agent_configs import AGENT_CONFIGS
from eval.configs.run_configs import (
    M3_FINAL_INCREMENTAL_RUN_CONFIG,
    M3_FINAL_STRATEGIC_SUMMARY_RUN_CONFIG,
    M3_FINAL_TOKEN_TRIGGER_RUN_CONFIG,
)
from eval.configs.trial_configs import TRIAL_CONFIGS
from student_framework.escape_room import (
    ESCAPE_ROOM_INCREMENTAL_SYSTEM_PROMPT,
)


REFERENCE_TO_INCREMENTAL = {
    "baseline": "baseline_incremental",
    "planner": "planner_incremental",
    "summary": "summary_incremental",
    "planner_summary": "planner_summary_incremental",
}


SUMMARY_TO_TOKEN_TRIGGER = {
    "summary_incremental": "summary_incremental_token_trigger",
    "planner_summary_incremental": (
        "planner_summary_incremental_token_trigger"
    ),
}


TOKEN_TRIGGER_TO_STRATEGIC = {
    "summary_incremental_token_trigger": (
        "summary_incremental_strategic"
    ),
    "planner_summary_incremental_token_trigger": (
        "planner_summary_incremental_strategic"
    ),
}


def test_incremental_configs_change_only_system_prompt() -> None:
    """Etapa 2 modifica sólo el prompt de cada sistema promovido."""

    for reference_name, incremental_name in (
        REFERENCE_TO_INCREMENTAL.items()
    ):
        reference = AGENT_CONFIGS[reference_name]
        incremental = AGENT_CONFIGS[incremental_name]

        assert reference["system_prompt"] != (
            incremental["system_prompt"]
        )
        assert incremental["system_prompt"] == (
            ESCAPE_ROOM_INCREMENTAL_SYSTEM_PROMPT
        )

        reference_without_prompt = {
            key: value
            for key, value in reference.items()
            if key != "system_prompt"
        }
        incremental_without_prompt = {
            key: value
            for key, value in incremental.items()
            if key != "system_prompt"
        }

        assert incremental_without_prompt == (
            reference_without_prompt
        )


def test_incremental_run_manifest_materializes_stage2_condition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """El manifest conserva la intervención y recovery de Etapa 1."""

    monkeypatch.setattr(
        persistence,
        "_created_at",
        lambda: "2026-08-25T00:00:00+00:00",
    )
    monkeypatch.setattr(
        persistence,
        "_git_metadata",
        lambda: {
            "commit": "abc123",
            "branch": "m3/final-experimental-improvements",
            "dirty": False,
        },
    )

    manifest = persistence.build_run_manifest(
        run_id="m3-final-run-003",
        run_config=M3_FINAL_INCREMENTAL_RUN_CONFIG,
    )

    incremental_names = list(
        REFERENCE_TO_INCREMENTAL.values()
    )

    assert [
        system["agent_config"]
        for system in manifest["run"]["systems"]
    ] == incremental_names

    assert manifest["run"]["trial_configs"] == [
        "multi_attempt_recovery",
    ]
    assert manifest["trial_configs"] == {
        "multi_attempt_recovery": (
            TRIAL_CONFIGS["multi_attempt_recovery"]
        ),
    }

    assert manifest["agent_configs"] == {
        name: AGENT_CONFIGS[name]
        for name in sorted(incremental_names)
    }

    json.dumps(
        manifest,
        ensure_ascii=False,
    )


def test_token_trigger_configs_replace_message_trigger_policy() -> None:
    """Etapa 3 cambia sólo la política que dispara la compactación."""

    for reference_name, candidate_name in (
        SUMMARY_TO_TOKEN_TRIGGER.items()
    ):
        reference = AGENT_CONFIGS[reference_name]
        candidate = AGENT_CONFIGS[candidate_name]

        assert reference["max_history_messages"] == 20
        assert candidate["max_history_messages"] == 100
        assert (
            "history_compaction_input_token_threshold"
            not in reference
        )
        assert (
            candidate["history_compaction_input_token_threshold"]
            == 8_000
        )

        expected = {
            **reference,
            "max_history_messages": 100,
            "history_compaction_input_token_threshold": 8_000,
        }

        assert candidate == expected


def test_token_trigger_run_inherits_promoted_stage2_condition() -> None:
    """Run 004 modifica sólo los sistemas afectados por summarization."""

    assert M3_FINAL_TOKEN_TRIGGER_RUN_CONFIG["systems"] == [
        {
            "agent_config": "summary_incremental_token_trigger",
            "llm_config": "nova-lite",
        },
        {
            "agent_config": (
                "planner_summary_incremental_token_trigger"
            ),
            "llm_config": "nova-lite",
        },
    ]

    assert M3_FINAL_TOKEN_TRIGGER_RUN_CONFIG["trial_configs"] == (
        M3_FINAL_INCREMENTAL_RUN_CONFIG["trial_configs"]
    )
    assert M3_FINAL_TOKEN_TRIGGER_RUN_CONFIG["scenarios"] == (
        M3_FINAL_INCREMENTAL_RUN_CONFIG["scenarios"]
    )
    assert M3_FINAL_TOKEN_TRIGGER_RUN_CONFIG["trials_per_case"] == (
        M3_FINAL_INCREMENTAL_RUN_CONFIG["trials_per_case"]
    )

    total_trials = (
        len(M3_FINAL_TOKEN_TRIGGER_RUN_CONFIG["systems"])
        * len(M3_FINAL_TOKEN_TRIGGER_RUN_CONFIG["trial_configs"])
        * len(M3_FINAL_TOKEN_TRIGGER_RUN_CONFIG["scenarios"])
        * M3_FINAL_TOKEN_TRIGGER_RUN_CONFIG["trials_per_case"]
    )

    assert total_trials == 160


def test_token_trigger_run_manifest_materializes_stage3_condition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """El manifest conserva el trigger de 8k y la condición heredada."""

    monkeypatch.setattr(
        persistence,
        "_created_at",
        lambda: "2026-08-25T00:00:00+00:00",
    )
    monkeypatch.setattr(
        persistence,
        "_git_metadata",
        lambda: {
            "commit": "abc123",
            "branch": "m3/final-stage3",
            "dirty": False,
        },
    )

    manifest = persistence.build_run_manifest(
        run_id="m3-final-run-004",
        run_config=M3_FINAL_TOKEN_TRIGGER_RUN_CONFIG,
    )

    candidate_names = list(
        SUMMARY_TO_TOKEN_TRIGGER.values()
    )

    assert [
        system["agent_config"]
        for system in manifest["run"]["systems"]
    ] == candidate_names

    assert manifest["run"]["trial_configs"] == [
        "multi_attempt_recovery",
    ]
    assert manifest["agent_configs"] == {
        name: AGENT_CONFIGS[name]
        for name in sorted(candidate_names)
    }

    for name in candidate_names:
        assert (
            manifest["agent_configs"][name][
                "history_compaction_input_token_threshold"
            ]
            == 8_000
        )
        assert (
            manifest["agent_configs"][name]["max_history_messages"]
            == 100
        )

    json.dumps(
        manifest,
        ensure_ascii=False,
    )


def test_strategic_configs_extend_stage3_summary_policy() -> None:
    """Etapa 4 suma estrategia y periodicidad a la condición promovida."""

    for reference_name, candidate_name in (
        TOKEN_TRIGGER_TO_STRATEGIC.items()
    ):
        reference = AGENT_CONFIGS[reference_name]
        candidate = AGENT_CONFIGS[candidate_name]

        assert (
            "history_compaction_profile"
            not in reference
        )
        assert (
            "history_compaction_message_interval"
            not in reference
        )

        expected = {
            **reference,
            "history_compaction_profile": "strategic_v1",
            "history_compaction_message_interval": 20,
        }

        assert candidate == expected
        assert (
            candidate["history_compaction_input_token_threshold"]
            == 8_000
        )
        assert candidate["max_history_messages"] == 100


def test_strategic_summary_run_inherits_stage3_condition() -> None:
    """Run 005 conserva Stage 3 y cambia sólo los sistemas resumidores."""

    assert M3_FINAL_STRATEGIC_SUMMARY_RUN_CONFIG["systems"] == [
        {
            "agent_config": "summary_incremental_strategic",
            "llm_config": "nova-lite",
        },
        {
            "agent_config": "planner_summary_incremental_strategic",
            "llm_config": "nova-lite",
        },
    ]

    assert M3_FINAL_STRATEGIC_SUMMARY_RUN_CONFIG["trial_configs"] == (
        M3_FINAL_TOKEN_TRIGGER_RUN_CONFIG["trial_configs"]
    )
    assert M3_FINAL_STRATEGIC_SUMMARY_RUN_CONFIG["scenarios"] == (
        M3_FINAL_TOKEN_TRIGGER_RUN_CONFIG["scenarios"]
    )
    assert M3_FINAL_STRATEGIC_SUMMARY_RUN_CONFIG["trials_per_case"] == (
        M3_FINAL_TOKEN_TRIGGER_RUN_CONFIG["trials_per_case"]
    )

    total_trials = (
        len(M3_FINAL_STRATEGIC_SUMMARY_RUN_CONFIG["systems"])
        * len(M3_FINAL_STRATEGIC_SUMMARY_RUN_CONFIG["trial_configs"])
        * len(M3_FINAL_STRATEGIC_SUMMARY_RUN_CONFIG["scenarios"])
        * M3_FINAL_STRATEGIC_SUMMARY_RUN_CONFIG["trials_per_case"]
    )

    assert total_trials == 160


def test_strategic_summary_manifest_materializes_stage4_condition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """El manifest conserva profile, periodicidad y política heredada."""

    monkeypatch.setattr(
        persistence,
        "_created_at",
        lambda: "2026-08-25T00:00:00+00:00",
    )
    monkeypatch.setattr(
        persistence,
        "_git_metadata",
        lambda: {
            "commit": "abc123",
            "branch": "m3/final-stage4",
            "dirty": False,
        },
    )

    manifest = persistence.build_run_manifest(
        run_id="m3-final-run-005",
        run_config=M3_FINAL_STRATEGIC_SUMMARY_RUN_CONFIG,
    )

    candidate_names = list(
        TOKEN_TRIGGER_TO_STRATEGIC.values()
    )

    assert [
        system["agent_config"]
        for system in manifest["run"]["systems"]
    ] == candidate_names

    assert manifest["run"]["trial_configs"] == [
        "multi_attempt_recovery",
    ]
    assert manifest["agent_configs"] == {
        name: AGENT_CONFIGS[name]
        for name in sorted(candidate_names)
    }

    for name in candidate_names:
        agent_config = manifest["agent_configs"][name]

        assert (
            agent_config["history_compaction_profile"]
            == "strategic_v1"
        )
        assert (
            agent_config["history_compaction_message_interval"]
            == 20
        )
        assert (
            agent_config["history_compaction_input_token_threshold"]
            == 8_000
        )
        assert agent_config["max_history_messages"] == 100
        assert agent_config["compaction_keep_recent_rounds"] == 2

    json.dumps(
        manifest,
        ensure_ascii=False,
    )
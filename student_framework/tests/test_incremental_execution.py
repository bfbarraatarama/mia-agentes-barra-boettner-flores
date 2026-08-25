from __future__ import annotations

import json

import pytest

from eval import persistence
from eval.configs.agent_configs import AGENT_CONFIGS
from eval.configs.run_configs import M3_FINAL_INCREMENTAL_RUN_CONFIG
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
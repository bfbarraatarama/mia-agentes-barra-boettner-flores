"""Configuraciones de agentes para la evaluación de M3."""

from __future__ import annotations

from typing import Any

from student_framework.escape_room import (
    ESCAPE_ROOM_INCREMENTAL_SYSTEM_PROMPT,
    ESCAPE_ROOM_MINIMAL_SYSTEM_PROMPT,
)
from student_framework.planner_agent import (
    DEFAULT_PLAN_GUIDANCE,
    DEFAULT_PLANNING_PROMPT,
    DEFAULT_PLANNING_REPAIR_MAX_ATTEMPTS,
)


BASE_AGENT_CONFIG: dict[str, Any] = {
    "system_prompt": ESCAPE_ROOM_MINIMAL_SYSTEM_PROMPT,
    "register_default_tools": False,
    "max_iterations": 40,
}


BASELINE_AGENT_CONFIG: dict[str, Any] = {
    **BASE_AGENT_CONFIG,
    "max_history_messages": 100,
    "tool_call_repair_max_attempts": 0,
}


PLANNER_AGENT_CONFIG: dict[str, Any] = {
    **BASE_AGENT_CONFIG,
    "max_history_messages": 100,
    "tool_call_repair_max_attempts": 3,
    "use_planner": True,
    "planning_prompt": DEFAULT_PLANNING_PROMPT,
    "plan_guidance": DEFAULT_PLAN_GUIDANCE,
    "planning_repair_max_attempts": DEFAULT_PLANNING_REPAIR_MAX_ATTEMPTS,
}


SUMMARY_AGENT_CONFIG: dict[str, Any] = {
    **BASE_AGENT_CONFIG,
    "max_history_messages": 20,
    "tool_call_repair_max_attempts": 3,
    "history_compaction": "llm",
    "compaction_keep_recent_rounds": 2,
    "history_compaction_repair_max_attempts": 1,
}


PLANNER_SUMMARY_AGENT_CONFIG: dict[str, Any] = {
    **BASE_AGENT_CONFIG,
    "max_history_messages": 20,
    "tool_call_repair_max_attempts": 3,
    "use_planner": True,
    "planning_prompt": DEFAULT_PLANNING_PROMPT,
    "plan_guidance": DEFAULT_PLAN_GUIDANCE,
    "planning_repair_max_attempts": DEFAULT_PLANNING_REPAIR_MAX_ATTEMPTS,
    "history_compaction": "llm",
    "compaction_keep_recent_rounds": 2,
    "history_compaction_repair_max_attempts": 1,
}


BASELINE_INCREMENTAL_AGENT_CONFIG: dict[str, Any] = {
    **BASELINE_AGENT_CONFIG,
    "system_prompt": ESCAPE_ROOM_INCREMENTAL_SYSTEM_PROMPT,
}


PLANNER_INCREMENTAL_AGENT_CONFIG: dict[str, Any] = {
    **PLANNER_AGENT_CONFIG,
    "system_prompt": ESCAPE_ROOM_INCREMENTAL_SYSTEM_PROMPT,
}


SUMMARY_INCREMENTAL_AGENT_CONFIG: dict[str, Any] = {
    **SUMMARY_AGENT_CONFIG,
    "system_prompt": ESCAPE_ROOM_INCREMENTAL_SYSTEM_PROMPT,
}


PLANNER_SUMMARY_INCREMENTAL_AGENT_CONFIG: dict[str, Any] = {
    **PLANNER_SUMMARY_AGENT_CONFIG,
    "system_prompt": ESCAPE_ROOM_INCREMENTAL_SYSTEM_PROMPT,
}


SUMMARY_TOKEN_TRIGGER_AGENT_CONFIG: dict[str, Any] = {
    **SUMMARY_AGENT_CONFIG,
    "max_history_messages": 100,
    "history_compaction_input_token_threshold": 8_000,
}


PLANNER_SUMMARY_TOKEN_TRIGGER_AGENT_CONFIG: dict[str, Any] = {
    **PLANNER_SUMMARY_AGENT_CONFIG,
    "max_history_messages": 100,
    "history_compaction_input_token_threshold": 8_000,
}


SUMMARY_STRATEGIC_AGENT_CONFIG: dict[str, Any] = {
    **SUMMARY_TOKEN_TRIGGER_AGENT_CONFIG,
    "history_compaction_profile": "strategic_v1",
    "history_compaction_message_interval": 20,
}


PLANNER_SUMMARY_STRATEGIC_AGENT_CONFIG: dict[str, Any] = {
    **PLANNER_SUMMARY_TOKEN_TRIGGER_AGENT_CONFIG,
    "history_compaction_profile": "strategic_v1",
    "history_compaction_message_interval": 20,
}


SUMMARY_INCREMENTAL_TOKEN_TRIGGER_AGENT_CONFIG: dict[str, Any] = {
    **SUMMARY_INCREMENTAL_AGENT_CONFIG,
    "max_history_messages": 100,
    "history_compaction_input_token_threshold": 8_000,
}


PLANNER_SUMMARY_INCREMENTAL_TOKEN_TRIGGER_AGENT_CONFIG: dict[str, Any] = {
    **PLANNER_SUMMARY_INCREMENTAL_AGENT_CONFIG,
    "max_history_messages": 100,
    "history_compaction_input_token_threshold": 8_000,
}


SUMMARY_INCREMENTAL_STRATEGIC_AGENT_CONFIG: dict[str, Any] = {
    **SUMMARY_INCREMENTAL_TOKEN_TRIGGER_AGENT_CONFIG,
    "history_compaction_profile": "strategic_v1",
    "history_compaction_message_interval": 20,
}


PLANNER_SUMMARY_INCREMENTAL_STRATEGIC_AGENT_CONFIG: dict[str, Any] = {
    **PLANNER_SUMMARY_INCREMENTAL_TOKEN_TRIGGER_AGENT_CONFIG,
    "history_compaction_profile": "strategic_v1",
    "history_compaction_message_interval": 20,
}


MINIMAL_AGENT_CONFIG: dict[str, Any] = {
    "system_prompt": ESCAPE_ROOM_MINIMAL_SYSTEM_PROMPT,
    "register_default_tools": False,
    "max_iterations": 40,
    "max_history_messages": 100,
    "tool_call_repair_max_attempts": 0,
}


MINIMAL_TOOL_REPAIR_AGENT_CONFIG: dict[str, Any] = {
    **MINIMAL_AGENT_CONFIG,
    "tool_call_repair_max_attempts": 3,
}

# Control barato de la issue #26: cuánto del problema de contexto se
# resuelve solo subiendo el presupuesto.
MINIMAL_HISTORY_200_AGENT_CONFIG: dict[str, Any] = {
    **MINIMAL_AGENT_CONFIG,
    "max_history_messages": 200,
}


# Compactación sin LLM: comprime lo descartado sin abstracción.
MINIMAL_COMPACTION_AGENT_CONFIG: dict[str, Any] = {
    **MINIMAL_AGENT_CONFIG,
    "history_compaction": "deterministic",
    "compaction_keep_recent_rounds": 2,
}


# Variante del piloto cualitativo: reduce solamente la ventana para
# provocar compactaciones observables sin alterar el mecanismo.
QUALITATIVE_PILOT_COMPACTION_AGENT_CONFIG: dict[str, Any] = {
    **MINIMAL_COMPACTION_AGENT_CONFIG,
    "max_history_messages": 50,
}


# Resumen por LLM: abstrae lo descartado a estado estructurado.
MINIMAL_SUMMARY_AGENT_CONFIG: dict[str, Any] = {
    **MINIMAL_AGENT_CONFIG,
    "history_compaction": "llm",
    "compaction_keep_recent_rounds": 2,
    "history_compaction_repair_max_attempts": 1,
}


AGENT_CONFIGS: dict[str, dict[str, Any]] = {
    "baseline": BASELINE_AGENT_CONFIG,
    "planner": PLANNER_AGENT_CONFIG,
    "summary": SUMMARY_AGENT_CONFIG,
    "planner_summary": PLANNER_SUMMARY_AGENT_CONFIG,
    "baseline_incremental": BASELINE_INCREMENTAL_AGENT_CONFIG,
    "planner_incremental": PLANNER_INCREMENTAL_AGENT_CONFIG,
    "summary_incremental": SUMMARY_INCREMENTAL_AGENT_CONFIG,
    "planner_summary_incremental": PLANNER_SUMMARY_INCREMENTAL_AGENT_CONFIG,
    "summary_token_trigger": SUMMARY_TOKEN_TRIGGER_AGENT_CONFIG,
    "planner_summary_token_trigger": PLANNER_SUMMARY_TOKEN_TRIGGER_AGENT_CONFIG,
    "summary_strategic": SUMMARY_STRATEGIC_AGENT_CONFIG,
    "planner_summary_strategic": PLANNER_SUMMARY_STRATEGIC_AGENT_CONFIG,
    "summary_incremental_token_trigger": SUMMARY_INCREMENTAL_TOKEN_TRIGGER_AGENT_CONFIG,
    "planner_summary_incremental_token_trigger": PLANNER_SUMMARY_INCREMENTAL_TOKEN_TRIGGER_AGENT_CONFIG,
    "summary_incremental_strategic": SUMMARY_INCREMENTAL_STRATEGIC_AGENT_CONFIG,
    "planner_summary_incremental_strategic": PLANNER_SUMMARY_INCREMENTAL_STRATEGIC_AGENT_CONFIG,
    "minimal": MINIMAL_AGENT_CONFIG,
    "minimal_tool_repair": MINIMAL_TOOL_REPAIR_AGENT_CONFIG,
    "minimal_history_200": MINIMAL_HISTORY_200_AGENT_CONFIG,
    "minimal_compaction": MINIMAL_COMPACTION_AGENT_CONFIG,
    "qualitative_pilot_compaction": QUALITATIVE_PILOT_COMPACTION_AGENT_CONFIG,
    "minimal_summary": MINIMAL_SUMMARY_AGENT_CONFIG,
}
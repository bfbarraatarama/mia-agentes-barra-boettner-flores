"""Configuraciones de agentes para la evaluación de M3."""

from __future__ import annotations

from typing import Any

from student_framework.escape_room import ESCAPE_ROOM_MINIMAL_SYSTEM_PROMPT


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
}


# Resumen por LLM: abstrae lo descartado a estado estructurado.
MINIMAL_SUMMARY_AGENT_CONFIG: dict[str, Any] = {
    **MINIMAL_AGENT_CONFIG,
    "history_compaction": "llm",
}


AGENT_CONFIGS: dict[str, dict[str, Any]] = {
    "minimal": MINIMAL_AGENT_CONFIG,
    "minimal_tool_repair": MINIMAL_TOOL_REPAIR_AGENT_CONFIG,
    "minimal_history_200": MINIMAL_HISTORY_200_AGENT_CONFIG,
    "minimal_compaction": MINIMAL_COMPACTION_AGENT_CONFIG,
    "minimal_summary": MINIMAL_SUMMARY_AGENT_CONFIG,
}
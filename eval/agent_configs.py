"""Configuraciones de agentes para la evaluación de M3."""

from __future__ import annotations

from typing import Any

from student_framework.escape_room import ESCAPE_ROOM_MINIMAL_SYSTEM_PROMPT


MINIMAL_AGENT_CONFIG: dict[str, Any] = {
    "system_prompt": ESCAPE_ROOM_MINIMAL_SYSTEM_PROMPT,
    "register_default_tools": False,
    "max_iterations": 100,
    "max_history_messages": 50,
}


AGENT_CONFIGS: dict[str, dict[str, Any]] = {
    "minimal": MINIMAL_AGENT_CONFIG,
}
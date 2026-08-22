"""Paquete propio del grupo.

Implementen el agente en `agent.py` y registren sus herramientas a
continuación, en `build_agent`. Tanto el runner de la CLI como los tests
de conformidad llaman a `build_agent`, por lo que esta es la única puerta
de entrada pública de su entrega.
"""

from __future__ import annotations

from typing import Any

from mia_agents.llm_client import LLMClient
from mia_agents.protocols import Agent

from .agent import MyAgent

from student_framework.tools.calculator import  calculator, calculator_schema
from student_framework.tools.distance_converter import distance_converter, distance_converter_schema
from student_framework.tools.file_reader import file_reader, file_reader_schema
from student_framework.context.summarizer import (
    deterministic_history_compactor,
    make_llm_history_compactor,
)


def build_agent(config: dict[str, Any] | None = None) -> Agent:
    """Construye y configura su agente.

    `config` es opcional. Si se proporciona `config["llm_client"]`, el
    agente debe usarlo (así es como los tests de conformidad inyectan un
    cliente mock). Si no, se construye a partir del entorno.

    TODO (M1): instancien su agente y llamen a `agent.register_tool(...)`
    por cada una de sus herramientas antes de devolverlo.
    """

    config = config or {} #NO CAMBIAR
    llm = config.get("llm_client") or LLMClient.from_env() #NO CAMBIAR
    kwargs: dict[str, Any] = {"llm_client": llm} #NO CAMBIAR

    if "system_prompt" in config:
        kwargs["system_prompt"] = config["system_prompt"]

    if "max_history_messages" in config:
        kwargs["max_history_messages"] = config["max_history_messages"]

    if "max_iterations" in config:
        kwargs["max_iterations"] = config["max_iterations"]

    if "tool_call_repair_max_attempts" in config:
        kwargs["tool_call_repair_max_attempts"] = config[
            "tool_call_repair_max_attempts"
        ]
    if "trace_callback" in config:
        kwargs["trace_callback"] = config["trace_callback"]

    if "compaction_keep_recent_rounds" in config:
        kwargs["compaction_keep_recent_rounds"] = config[
            "compaction_keep_recent_rounds"
        ]

    agent = MyAgent(**kwargs)

    # Estrategia de compactación declarativa, para que las configs de
    # eval/ sigan siendo serializables en el manifest del run. También
    # se acepta un callable directo (tests).
    history_compaction = config.get("history_compaction")

    if callable(history_compaction):
        agent.set_history_compactor(history_compaction)
    elif history_compaction == "deterministic":
        agent.set_history_compactor(deterministic_history_compactor)
    elif history_compaction == "llm":
        agent.set_history_compactor(make_llm_history_compactor(agent))
    elif history_compaction is not None:
        raise ValueError(
            f"history_compaction desconocida: {history_compaction!r}. "
            "Valores válidos: 'deterministic', 'llm' o un callable."
        )

    if config.get("register_default_tools", True):
        agent.register_tool(calculator, calculator_schema)
        agent.register_tool(
            distance_converter,
            distance_converter_schema,
        )
        agent.register_tool(file_reader, file_reader_schema)

    return agent

"""Agente con planificación explícita antes del loop ReAct."""

from __future__ import annotations

from typing import Any, Callable

from mia_agents.protocols import LLMClient, AgentResult

from .agent import MyAgent
from .plan import Plan


class PlannerAgent(MyAgent):
    def run(self, user_message: str) -> AgentResult:
        plan = self.structured_call(
            prompt=(
                "Analizá la siguiente tarea de escape room y creá un plan de acción "
                "paso a paso. Tené en cuenta que el objetivo puede requerir cumplir "
                "sub-objetivos en un orden específico. Usá las herramientas disponibles "
                "para explorar, tomar objetos y usarlos.\n\n"
                f"{user_message}"
            ),
            schema=Plan,
        )

        plan_text = "Plan de acción:\n" + "\n".join(
            f"{i + 1}. {step.description}"
            for i, step in enumerate(plan.steps)
        )

        return super().run(
            f"{user_message}\n\n"
            f"{plan_text}\n\n"
            "Usá este plan como guía. Adaptá las acciones a las observaciones del "
            "entorno y no asumas que un paso es válido si nueva evidencia lo contradice."
        )

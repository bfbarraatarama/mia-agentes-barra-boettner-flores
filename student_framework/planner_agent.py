"""Agente con planificación explícita antes del loop ReAct."""

from __future__ import annotations

import json
from typing import Any

from mia_agents.protocols import AgentResult, LLMClient
from mia_agents.tool_schema import final_result_tool_schema

from .agent import MyAgent
from .plan import Plan


DEFAULT_PLANNING_PROMPT = (
    "Analizá la siguiente tarea de escape room y creá un plan de acción "
    "paso a paso. Tené en cuenta que el objetivo puede requerir cumplir "
    "sub-objetivos en un orden específico. Usá las herramientas disponibles "
    "para explorar, tomar objetos y usarlos."
)

DEFAULT_PLAN_GUIDANCE = (
    "Usá este plan como guía. Adaptá las acciones a las observaciones del "
    "entorno y no asumas que un paso es válido si nueva evidencia lo contradice."
)

DEFAULT_PLANNING_REPAIR_MAX_ATTEMPTS = 2


class PlannerAgent(MyAgent):
    def __init__(
        self,
        llm_client: LLMClient,
        planning_prompt: str = DEFAULT_PLANNING_PROMPT,
        plan_guidance: str = DEFAULT_PLAN_GUIDANCE,
        planning_repair_max_attempts: int = DEFAULT_PLANNING_REPAIR_MAX_ATTEMPTS,
        **kwargs: Any,
    ) -> None:
        super().__init__(llm_client=llm_client, **kwargs)

        if planning_repair_max_attempts < 0:
            raise ValueError(
                "planning_repair_max_attempts no puede ser negativo."
            )

        self._planning_prompt = planning_prompt
        self._plan_guidance = plan_guidance
        self._planning_repair_max_attempts = planning_repair_max_attempts
        self._initial_plan_generated = False

    def run(self, user_message: str) -> AgentResult:
        if self._initial_plan_generated:
            return super().run(user_message)

        plan_input_tokens: int | None = None
        plan_output_tokens: int | None = None

        def accumulate_plan_tokens(response: Any) -> None:
            nonlocal plan_input_tokens, plan_output_tokens

            if response.input_tokens is not None or plan_input_tokens is not None:
                plan_input_tokens = (
                    (plan_input_tokens or 0)
                    + (response.input_tokens or 0)
                )
            if response.output_tokens is not None or plan_output_tokens is not None:
                plan_output_tokens = (
                    (plan_output_tokens or 0)
                    + (response.output_tokens or 0)
                )

        final_tool = final_result_tool_schema(Plan)

        def validate_plan(final_call: Any) -> Plan:
            args = json.loads(final_call.arguments)
            return Plan.model_validate(args)

        try:
            plan = self._structured_call_with_repair(
                prompt=f"{self._planning_prompt}\n\n{user_message}",
                tools=[final_tool],
                validate_call=validate_plan,
                max_repair_attempts=self._planning_repair_max_attempts,
                response_callback=accumulate_plan_tokens,
                purpose="planning",
            )
        except ValueError as error:
            message = (
                "No se pudo generar el plan inicial: "
                f"{error}"
            )

            if self._trace_callback is not None:
                self._trace_callback({
                    "type": "planning_failure",
                    "message": message,
                })

            return AgentResult(
                answer=message,
                error=message,
                input_tokens=plan_input_tokens,
                output_tokens=plan_output_tokens,
            )

        if self._trace_callback is not None:
            self._trace_callback({
                "type": "planning",
                "plan": plan.model_dump(),
            })

        plan_text = "Plan de acción:\n" + "\n".join(
            f"{i + 1}. {step.description}"
            for i, step in enumerate(plan.steps)
        )

        self._initial_plan_generated = True

        result = super().run(
            f"{user_message}\n\n"
            f"{plan_text}\n\n"
            f"{self._plan_guidance}"
        )

        if plan_input_tokens is not None or result.input_tokens is not None:
            result.input_tokens = (
                (plan_input_tokens or 0)
                + (result.input_tokens or 0)
            )
        if plan_output_tokens is not None or result.output_tokens is not None:
            result.output_tokens = (
                (plan_output_tokens or 0)
                + (result.output_tokens or 0)
            )

        return result

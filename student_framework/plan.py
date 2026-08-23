"""Modelo de plan estructurado para el agente planificador."""

from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    description: str


class Plan(BaseModel):
    steps: list[PlanStep] = Field(min_length=1, max_length=12)

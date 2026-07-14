"""Pydantic schemas — Tasks."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    required_skills: list[str] = []
    estimated_hours: float | None = None
    deadline: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(None, max_length=255)
    description: str | None = None
    status: str | None = Field(None, pattern="^(pending|in_progress|completed|blocked)$")
    actual_hours: float | None = None


class TaskAssign(BaseModel):
    volunteer_id: UUID


class TaskResponse(BaseModel):
    id: UUID
    event_id: UUID
    title: str
    description: str | None
    required_skills: list | None
    estimated_hours: float | None
    actual_hours: float | None
    deadline: datetime | None
    assigned_to: UUID | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}

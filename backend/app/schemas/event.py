"""Pydantic schemas — Events."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class EventCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    location: str | None = None
    start_date: datetime
    end_date: datetime
    max_volunteers: int = Field(default=50, gt=0)
    required_skill_ids: list[UUID] = []

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")
        return self


class EventUpdate(BaseModel):
    title: str | None = Field(None, max_length=255)
    description: str | None = None
    location: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    max_volunteers: int | None = Field(None, gt=0)
    status: str | None = Field(None, pattern="^(planning|open|in_progress|completed|cancelled)$")


class EventResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    location: str | None
    start_date: datetime
    end_date: datetime
    max_volunteers: int
    status: str
    coordinator_id: UUID
    created_at: datetime
    registered_count: int = 0

    model_config = {"from_attributes": True}


class EventListResponse(BaseModel):
    events: list[EventResponse]
    total: int
    page: int
    per_page: int

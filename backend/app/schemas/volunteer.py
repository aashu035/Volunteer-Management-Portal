"""Pydantic schemas — Volunteer profiles and skills."""

from uuid import UUID

from pydantic import BaseModel, Field


class VolunteerProfileCreate(BaseModel):
    bio: str | None = None
    location: str | None = None
    emergency_contact: str | None = None


class VolunteerProfileUpdate(BaseModel):
    bio: str | None = None
    location: str | None = None
    emergency_contact: str | None = None


class SkillAssign(BaseModel):
    skill_id: UUID
    proficiency: str = Field(default="beginner", pattern="^(beginner|intermediate|expert)$")


class VolunteerProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    bio: str | None
    location: str | None
    total_hours: float
    badges: list | None

    model_config = {"from_attributes": True}


class VolunteerSearchResponse(BaseModel):
    id: UUID
    full_name: str
    email: str
    location: str | None
    total_hours: float
    skills: list[str]

    model_config = {"from_attributes": True}

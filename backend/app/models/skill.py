"""Skill models — skills and volunteer-skill M2M with proficiency."""

import enum
import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SkillProficiency(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Relationships
    volunteer_skills = relationship("VolunteerSkill", back_populates="skill")
    event_skills = relationship("EventSkill", back_populates="skill")


class VolunteerSkill(Base):
    __tablename__ = "volunteer_skills"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    volunteer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("volunteer_profiles.id", ondelete="CASCADE"), nullable=False
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False
    )
    proficiency: Mapped[SkillProficiency] = mapped_column(
        Enum(SkillProficiency, values_callable=lambda obj: [e.value for e in obj]), default=SkillProficiency.BEGINNER
    )
    verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    volunteer = relationship("VolunteerProfile", back_populates="skills")
    skill = relationship("Skill", back_populates="volunteer_skills")

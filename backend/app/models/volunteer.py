"""Volunteer profile model — extended user info for volunteers."""

import uuid

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class VolunteerProfile(Base):
    __tablename__ = "volunteer_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    emergency_contact: Mapped[str | None] = mapped_column(String(255), nullable=True)
    total_hours: Mapped[float] = mapped_column(Float, default=0.0)
    badges: Mapped[dict | None] = mapped_column(JSON, default=list)

    # Relationships
    user = relationship("User", back_populates="volunteer_profile")
    skills = relationship("VolunteerSkill", back_populates="volunteer", cascade="all, delete-orphan")

"""Volunteer repository — volunteer profile data access."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.volunteer import VolunteerProfile
from app.repositories.base import BaseRepository


class VolunteerRepository(BaseRepository[VolunteerProfile]):
    def __init__(self, db: AsyncSession):
        super().__init__(VolunteerProfile, db)

    async def get_by_user_id(self, user_id: UUID) -> VolunteerProfile | None:
        result = await self.db.execute(
            select(VolunteerProfile)
            .where(VolunteerProfile.user_id == user_id)
            .options(selectinload(VolunteerProfile.skills))
        )
        return result.scalar_one_or_none()

    async def get_all_with_skills(self, skip: int = 0, limit: int = 20) -> list[VolunteerProfile]:
        result = await self.db.execute(
            select(VolunteerProfile)
            .options(selectinload(VolunteerProfile.skills))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

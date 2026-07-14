"""Volunteer service — profile and skill management."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourceNotFoundError
from app.models.volunteer import VolunteerProfile
from app.models.skill import VolunteerSkill
from app.repositories.volunteer_repo import VolunteerRepository
from app.schemas.volunteer import VolunteerProfileUpdate


class VolunteerService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.volunteer_repo = VolunteerRepository(db)

    async def get_profile(self, user_id: UUID) -> VolunteerProfile:
        profile = await self.volunteer_repo.get_by_user_id(user_id)
        if not profile:
            raise ResourceNotFoundError("Volunteer profile")
        return profile

    async def update_profile(self, user_id: UUID, data: VolunteerProfileUpdate) -> VolunteerProfile:
        profile = await self.volunteer_repo.get_by_user_id(user_id)
        if not profile:
            raise ResourceNotFoundError("Volunteer profile")
        update_data = data.model_dump(exclude_unset=True)
        return await self.volunteer_repo.update(profile, update_data)

    async def add_skill(self, user_id: UUID, skill_id: UUID, proficiency: str = "beginner") -> None:
        profile = await self.volunteer_repo.get_by_user_id(user_id)
        if not profile:
            raise ResourceNotFoundError("Volunteer profile")
        vol_skill = VolunteerSkill(
            volunteer_id=profile.id,
            skill_id=skill_id,
            proficiency=proficiency,
        )
        self.db.add(vol_skill)
        await self.db.flush()

    async def list_volunteers(self, skip: int = 0, limit: int = 20) -> list[VolunteerProfile]:
        return await self.volunteer_repo.get_all_with_skills(skip=skip, limit=limit)

"""Volunteer endpoints — profile management and search."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.volunteer import SkillAssign, VolunteerProfileResponse, VolunteerProfileUpdate
from app.schemas.user import MessageResponse
from app.services.volunteer_service import VolunteerService

router = APIRouter()


@router.get("/me", response_model=VolunteerProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current volunteer's profile."""
    service = VolunteerService(db)
    return await service.get_profile(current_user.id)


@router.put("/me", response_model=VolunteerProfileResponse)
async def update_my_profile(
    data: VolunteerProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current volunteer's profile."""
    service = VolunteerService(db)
    return await service.update_profile(current_user.id, data)


@router.post("/me/skills", response_model=MessageResponse, status_code=201)
async def add_skill(
    data: SkillAssign,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add a skill to current volunteer's profile."""
    service = VolunteerService(db)
    await service.add_skill(current_user.id, data.skill_id, data.proficiency)
    return MessageResponse(message="Skill added successfully")


@router.get("/", response_model=list[VolunteerProfileResponse])
async def list_volunteers(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all volunteer profiles."""
    service = VolunteerService(db)
    return await service.list_volunteers(skip=skip, limit=limit)

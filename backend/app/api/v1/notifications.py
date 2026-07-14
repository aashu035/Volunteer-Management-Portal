"""Notification endpoints — list, read, delete."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import MessageResponse
from app.services.notification_service import NotificationService

router = APIRouter()


@router.get("/")
async def get_notifications(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's notifications."""
    service = NotificationService(db)
    return await service.get_user_notifications(current_user.id, skip=skip, limit=limit)


@router.put("/{notification_id}/read", response_model=MessageResponse)
async def mark_notification_read(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a notification as read."""
    service = NotificationService(db)
    await service.mark_as_read(notification_id, current_user.id)
    return MessageResponse(message="Notification marked as read")


@router.delete("/{notification_id}", response_model=MessageResponse)
async def delete_notification(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a notification."""
    service = NotificationService(db)
    await service.delete_notification(notification_id, current_user.id)
    return MessageResponse(message="Notification deleted")

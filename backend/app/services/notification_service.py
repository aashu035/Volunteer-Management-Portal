"""Notification service — in-app alerts (email stubbed)."""

from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.models.notification import Notification, NotificationType

logger = get_logger(__name__)


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_notification(
        self,
        user_id: UUID,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.GENERAL,
    ) -> Notification:
        notification = Notification(
            user_id=user_id,
            type=notification_type,
            title=title,
            message=message,
        )
        self.db.add(notification)
        await self.db.flush()

        # Stub email sending — logs instead of real SMTP
        logger.info(f"[EMAIL STUB] To: user={user_id} | Subject: {title} | Body: {message}")

        return notification

    async def get_user_notifications(
        self, user_id: UUID, skip: int = 0, limit: int = 20
    ) -> list[Notification]:
        result = await self.db.execute(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def mark_as_read(self, notification_id: UUID, user_id: UUID) -> None:
        await self.db.execute(
            update(Notification)
            .where(Notification.id == notification_id, Notification.user_id == user_id)
            .values(is_read=True)
        )
        await self.db.flush()

    async def delete_notification(self, notification_id: UUID, user_id: UUID) -> None:
        result = await self.db.execute(
            select(Notification)
            .where(Notification.id == notification_id, Notification.user_id == user_id)
        )
        notification = result.scalar_one_or_none()
        if notification:
            await self.db.delete(notification)
            await self.db.flush()

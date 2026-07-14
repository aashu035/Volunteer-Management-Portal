"""Task repository — task-specific data access."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: AsyncSession):
        super().__init__(Task, db)

    async def get_by_event(self, event_id: UUID) -> list[Task]:
        result = await self.db.execute(
            select(Task).where(Task.event_id == event_id).order_by(Task.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_assignee(self, user_id: UUID) -> list[Task]:
        result = await self.db.execute(
            select(Task).where(Task.assigned_to == user_id).order_by(Task.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_pending_count(self) -> int:
        from sqlalchemy import func
        result = await self.db.execute(
            select(func.count()).select_from(Task).where(Task.status == "pending")
        )
        return result.scalar_one()

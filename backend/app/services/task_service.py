"""Task service — task management and assignment."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourceNotFoundError
from app.models.task import Task
from app.repositories.task_repo import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_repo = TaskRepository(db)

    async def create_task(self, event_id: UUID, data: TaskCreate) -> Task:
        task = Task(
            event_id=event_id,
            title=data.title,
            description=data.description,
            required_skills=data.required_skills,
            estimated_hours=data.estimated_hours,
            deadline=data.deadline,
        )
        return await self.task_repo.create(task)

    async def get_task(self, task_id: UUID) -> Task:
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise ResourceNotFoundError("Task")
        return task

    async def get_tasks_by_event(self, event_id: UUID) -> list[Task]:
        return await self.task_repo.get_by_event(event_id)

    async def update_task(self, task_id: UUID, data: TaskUpdate) -> Task:
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise ResourceNotFoundError("Task")
        update_data = data.model_dump(exclude_unset=True)
        return await self.task_repo.update(task, update_data)

    async def assign_task(self, task_id: UUID, volunteer_id: UUID) -> Task:
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise ResourceNotFoundError("Task")
        task.assigned_to = volunteer_id
        task.status = "in_progress"
        await self.db.flush()
        await self.db.refresh(task)
        return task

    async def complete_task(self, task_id: UUID, actual_hours: float | None = None) -> Task:
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise ResourceNotFoundError("Task")
        task.status = "completed"
        if actual_hours is not None:
            task.actual_hours = actual_hours
        await self.db.flush()
        await self.db.refresh(task)
        return task

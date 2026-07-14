"""Task endpoints — CRUD, assignment, completion."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_user
from app.core.permissions import require_role
from app.models.user import User
from app.schemas.task import TaskAssign, TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter()


@router.get("/event/{event_id}", response_model=list[TaskResponse])
async def get_tasks_by_event(
    event_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all tasks for an event."""
    service = TaskService(db)
    return await service.get_tasks_by_event(event_id)


@router.post("/event/{event_id}", response_model=TaskResponse, status_code=201)
async def create_task(
    event_id: UUID,
    data: TaskCreate,
    current_user: User = Depends(require_role("admin", "coordinator")),
    db: AsyncSession = Depends(get_db),
):
    """Create a task within an event (coordinator+ only)."""
    service = TaskService(db)
    return await service.create_task(event_id, data)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get task details."""
    service = TaskService(db)
    return await service.get_task(task_id)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a task."""
    service = TaskService(db)
    return await service.update_task(task_id, data)


@router.post("/{task_id}/assign", response_model=TaskResponse)
async def assign_task(
    task_id: UUID,
    data: TaskAssign,
    current_user: User = Depends(require_role("admin", "coordinator")),
    db: AsyncSession = Depends(get_db),
):
    """Assign a volunteer to a task (coordinator+ only)."""
    service = TaskService(db)
    return await service.assign_task(task_id, data.volunteer_id)


@router.post("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: UUID,
    actual_hours: float | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a task as completed."""
    service = TaskService(db)
    return await service.complete_task(task_id, actual_hours)

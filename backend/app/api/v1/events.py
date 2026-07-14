"""Event endpoints — CRUD, registration, attendance."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_user
from app.core.permissions import require_role
from app.models.user import User
from app.schemas.event import EventCreate, EventListResponse, EventResponse, EventUpdate
from app.schemas.user import MessageResponse
from app.services.event_service import EventService

router = APIRouter()


@router.get("/", response_model=EventListResponse)
async def list_events(
    status: str | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List events with optional status filter and pagination."""
    service = EventService(db)
    events, total = await service.list_events(status=status, page=page, per_page=per_page)
    return EventListResponse(
        events=[EventResponse.model_validate(e) for e in events],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.post("/", response_model=EventResponse, status_code=201)
async def create_event(
    data: EventCreate,
    current_user: User = Depends(require_role("admin", "coordinator")),
    db: AsyncSession = Depends(get_db),
):
    """Create a new event (coordinator+ only)."""
    service = EventService(db)
    event = await service.create_event(data, current_user.id)
    return event


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get event details."""
    service = EventService(db)
    return await service.get_event(event_id)


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: UUID,
    data: EventUpdate,
    current_user: User = Depends(require_role("admin", "coordinator")),
    db: AsyncSession = Depends(get_db),
):
    """Update an event (coordinator+ only)."""
    service = EventService(db)
    return await service.update_event(event_id, data)


@router.delete("/{event_id}", response_model=MessageResponse)
async def delete_event(
    event_id: UUID,
    current_user: User = Depends(require_role("admin", "coordinator")),
    db: AsyncSession = Depends(get_db),
):
    """Soft delete an event (coordinator+ only)."""
    service = EventService(db)
    await service.delete_event(event_id)
    return MessageResponse(message="Event deleted")


@router.post("/{event_id}/register", response_model=MessageResponse, status_code=201)
async def register_for_event(
    event_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Register current user for an event."""
    service = EventService(db)
    await service.register_for_event(event_id, current_user.id)
    return MessageResponse(message="Successfully registered for event")

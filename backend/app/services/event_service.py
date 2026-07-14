"""Event service — event lifecycle management."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import EventFullError, ResourceAlreadyExistsError, ResourceNotFoundError
from app.models.event import Event, EventSkill
from app.repositories.event_repo import EventRepository
from app.schemas.event import EventCreate, EventUpdate


class EventService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.event_repo = EventRepository(db)

    async def create_event(self, data: EventCreate, coordinator_id: UUID) -> Event:
        event = Event(
            title=data.title,
            description=data.description,
            location=data.location,
            start_date=data.start_date,
            end_date=data.end_date,
            max_volunteers=data.max_volunteers,
            coordinator_id=coordinator_id,
        )
        event = await self.event_repo.create(event)

        # Add required skills
        for skill_id in data.required_skill_ids:
            event_skill = EventSkill(event_id=event.id, skill_id=skill_id)
            self.db.add(event_skill)
        await self.db.flush()

        return event

    async def get_event(self, event_id: UUID) -> Event:
        event = await self.event_repo.get_with_relations(event_id)
        if not event:
            raise ResourceNotFoundError("Event")
        return event

    async def list_events(self, status: str | None = None, page: int = 1, per_page: int = 20):
        skip = (page - 1) * per_page
        events = await self.event_repo.get_filtered(status=status, skip=skip, limit=per_page)
        total = await self.event_repo.count()
        return events, total

    async def update_event(self, event_id: UUID, data: EventUpdate) -> Event:
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise ResourceNotFoundError("Event")
        update_data = data.model_dump(exclude_unset=True)
        return await self.event_repo.update(event, update_data)

    async def register_for_event(self, event_id: UUID, volunteer_id: UUID) -> None:
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise ResourceNotFoundError("Event")

        # Check capacity
        count = await self.event_repo.get_registration_count(event_id)
        if count >= event.max_volunteers:
            raise EventFullError()

        # Check duplicate registration
        if await self.event_repo.is_registered(event_id, volunteer_id):
            raise ResourceAlreadyExistsError("Already registered for this event")

        await self.event_repo.register_volunteer(event_id, volunteer_id)

    async def delete_event(self, event_id: UUID) -> None:
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise ResourceNotFoundError("Event")
        await self.event_repo.delete(event)

"""Event repository — event-specific data access."""

from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.event import Event, EventRegistration
from app.repositories.base import BaseRepository


class EventRepository(BaseRepository[Event]):
    def __init__(self, db: AsyncSession):
        super().__init__(Event, db)

    async def get_with_relations(self, event_id: UUID) -> Event | None:
        result = await self.db.execute(
            select(Event)
            .where(Event.id == event_id)
            .options(
                selectinload(Event.registrations),
                selectinload(Event.tasks),
                selectinload(Event.required_skills),
            )
        )
        return result.scalar_one_or_none()

    async def get_filtered(
        self,
        status: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Event]:
        query = select(Event)
        if status:
            query = query.where(Event.status == status)
        query = query.order_by(Event.start_date.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_registration_count(self, event_id: UUID) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(EventRegistration).where(
                EventRegistration.event_id == event_id
            )
        )
        return result.scalar_one()

    async def is_registered(self, event_id: UUID, volunteer_id: UUID) -> bool:
        result = await self.db.execute(
            select(EventRegistration).where(
                EventRegistration.event_id == event_id,
                EventRegistration.volunteer_id == volunteer_id,
            )
        )
        return result.scalar_one_or_none() is not None

    async def register_volunteer(self, event_id: UUID, volunteer_id: UUID) -> EventRegistration:
        registration = EventRegistration(event_id=event_id, volunteer_id=volunteer_id)
        self.db.add(registration)
        await self.db.flush()
        return registration

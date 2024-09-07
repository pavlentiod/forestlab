import json
from typing import List, Optional, Type

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.event.event import Event
from src.schemas.event.event_schema import EventInput, EventInDB


class EventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: EventInput) -> EventInDB:
        event = Event(**data.model_dump(exclude_unset=True))
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return EventInDB(
            id=event.id,
            title=event.title,
            **data.model_dump(exclude={"title"})
        )

    async def get_all(self) -> List[Optional[EventInDB]]:
        stmt = select(Event).order_by(Event.id)
        result = await self.session.execute(stmt)
        entities = result.scalars().all()
        return [EventInDB(**event.__dict__) for event in entities]

    async def get_event(self, _id: UUID4) -> EventInDB:
        event = await self.session.get(Event, _id)
        return EventInDB(**event.__dict__)

    async def get_by_id(self, _id: UUID4) -> Optional[Event]:
        return await self.session.get(Event, _id)

    async def get_by_source_link(self, link: str) -> Optional[EventInDB]:
        if "#" in link:
            link = link[:link.index("#")]
        event = await self.session.scalar(select(Event).where(Event.source == link))
        if event:
            return EventInDB(**event.__dict__)

    async def update(self, event: Type[Event], data: EventInput) -> EventInDB:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(event, key, value)
        await self.session.commit()
        await self.session.refresh(event)
        return EventInDB(**event.__dict__)

    async def delete(self, event: Type[Event]) -> bool:
        await self.session.delete(event)
        await self.session.commit()
        return True

from typing import List
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.event.event_repository import EventRepository
from src.schemas.event.event_schema import EventInDB, EventEndpoint, EventUpdate
from src.services.event.subservices.parser.parser import Parser


class EventService:
    """
    Service class for handling events.
    """

    def __init__(self, session: AsyncSession):
        self.repository = EventRepository(session)

    async def create(self, data_from_api: EventEndpoint) -> EventInDB:
        # TODO: add EventEndpoint data validation
        # Check if event exist
        exist = await self.repository.get_by_source_link(data_from_api.source)
        if exist:
            return exist

        # Parse data from link
        parser = Parser()
        event = parser.parse(source_link=data_from_api.source)

        # Update EventInput object and add to db
        event.title = data_from_api.title
        event.date = data_from_api.date
        event.source = data_from_api.source
        event_from_db = await self.repository.create(event)
        return event_from_db

    async def get_all(self) -> List[EventInDB]:
        return await self.repository.get_all()

    async def get_event(self, _id: UUID) -> EventInDB:
        event = await self.repository.get_event(_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

    async def update(self, _id: UUID, data: EventUpdate) -> EventInDB:
        event = await self.repository.get_by_id(_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        updated_event = await self.repository.update(event, data)
        return updated_event

    async def delete(self, _id: UUID) -> bool:
        event = await self.repository.get_by_id(_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return await self.repository.delete(event)


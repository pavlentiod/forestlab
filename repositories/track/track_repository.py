from typing import List, Optional, Type
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.track.track import Track
from src.schemas.track.track_schema import TrackInput, TrackInDB


class TrackRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: TrackInput) -> TrackInDB:
        track = Track(**data.model_dump(exclude_unset=True))
        self.session.add(track)
        await self.session.commit()
        await self.session.refresh(track)
        return TrackInDB(
            id=track.id,
            runner=track.runner,
            **data.model_dump(exclude={"runner"})
        )

    async def get_all(self) -> List[Optional[TrackInDB]]:
        stmt = select(Track).order_by(Track.id)
        result = await self.session.execute(stmt)
        entities = result.scalars().all()
        return [TrackInDB(**track.__dict__) for track in entities]

    async def get_track(self, _id: UUID) -> TrackInDB:
        track = await self.session.get(Track, _id)
        return TrackInDB(**track.__dict__)

    async def get_by_id(self, _id: UUID) -> Optional[Track]:
        return await self.session.get(Track, _id)

    async def get_by_event(self, event_id: UUID) -> List[TrackInDB]:
        stmt = select(Track).where(Track.event == event_id)
        result = await self.session.execute(stmt)
        entities = result.scalars().all()
        return [TrackInDB(**track.__dict__) for track in entities]

    async def get_by_event_and_runner(self, event_id: UUID, runner_id: UUID) -> TrackInDB:
        stmt = select(Track).where(Track.event == event_id).where(Track.runner == runner_id)
        result = await self.session.execute(stmt)
        track = result.scalar()
        return TrackInDB(**track.__dict__)


    async def delete(self, track: Type[Track]) -> bool:
        await self.session.delete(track)
        await self.session.commit()
        return True

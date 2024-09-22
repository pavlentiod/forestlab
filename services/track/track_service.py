from typing import List
from uuid import UUID

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.track.track_repository import TrackRepository
from src.schemas.track.track_schema import TrackInput, TrackInDB, TrackEndpoint
from src.services.track.subservices.gpx_transformer.gpx_transformer_service import GPXTransformer


class TrackService:
    """
    Service class for handling tracks.
    """

    def __init__(self, session: AsyncSession):
        self.repository = TrackRepository(session)

    async def create(self, data_from_api: TrackEndpoint, gpxfile: UploadFile) -> TrackInDB:

        # Check if track already exists for the given event and runner
        exist = await self.repository.get_by_event(data_from_api.event)
        if any(track.runner == data_from_api.runner for track in exist):
            raise HTTPException(status_code=400, detail="Track for this runner in the event already exists")

        gpxfile_bytes = gpxfile
        track_data = GPXTransformer(gpxfile_bytes).to_track_data()

        # Create a new TrackInput object and add to db
        track_input = TrackInput(
            runner=data_from_api.runner,
            event=data_from_api.event,
            **track_data.model_dump()
        )
        track_from_db = await self.repository.create(track_input)
        return track_from_db

    async def get_all(self) -> List[TrackInDB]:
        return await self.repository.get_all()

    async def get_track(self, _id: UUID) -> TrackInDB:
        track = await self.repository.get_track(_id)
        if not track:
            raise HTTPException(status_code=404, detail="Track not found")
        return track

    async def get_track_by_event_and_runner(self, event_id:UUID,  runner_id: UUID) -> TrackInDB:
        track = await self.repository.get_by_event_and_runner(event_id, runner_id)
        if not track:
            raise HTTPException(status_code=404, detail="Track not found")
        return track

    async def delete(self, _id: UUID) -> bool:
        track = await self.repository.get_by_id(_id)
        if not track:
            raise HTTPException(status_code=404, detail="Track not found")
        return await self.repository.delete(track)

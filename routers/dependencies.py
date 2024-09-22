from pathlib import Path
from typing import Annotated, Type, List, Dict, Any, TypedDict, Tuple, Union

from fastapi import Depends, HTTPException, Form
from pydantic import BaseModel, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import db_helper
from src.schemas.event.event_schema import EventInDB
from src.schemas.track.track_schema import TrackInDB
from src.services.event.event_service import EventService
from src.services.single_event_data.single_event_data_service import SingleEventDataService
from src.services.single_event_statistics.statistics_service import SingleEventStatisticsService
from src.services.single_event_statistics.subservices.geosplit.geosplit_service import GeoSplitService
from src.services.track.track_service import TrackService


async def event_by_id(
        event_id: Annotated[str, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> EventInDB:
    event_service = EventService(session=session)
    event = await event_service.get_event(event_id)
    if event is not None:
        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Event {event_id} not found!",
    )


async def track_by_event_and_runner(event_id: Annotated[str, Path], runner_id: Annotated[str, Path],
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    track_service = TrackService(session)
    track = await track_service.get_track_by_event_and_runner(event_id, runner_id)
    if track is not None:
        return track

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Track on event {event_id} by runner {runner_id} not found!",
    )

def get_geosplit_service(track: TrackInDB = Depends(track_by_event_and_runner)) -> GeoSplitService:
    if track:
        return GeoSplitService(track)
    else:
        return None

def get_track_service(session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> TrackService:
    return TrackService(session)




def get_event_service(session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> EventService:
    return EventService(session)


def get_event_data_service(event: EventInDB = Depends(event_by_id)) -> SingleEventDataService:
    return SingleEventDataService(event)


def get_event_statistics_service(event: EventInDB = Depends(event_by_id)) -> SingleEventStatisticsService:
    return SingleEventStatisticsService(event)

from typing import List, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, HTTPException, File

from src.routers.dependencies import get_track_service, validate_json
from src.schemas.track.track_schema import TrackEndpoint, TrackResponse
from src.services.track.track_service import TrackService

track_router = APIRouter()


# Endpoint for creating a new track
@track_router.post("/{event_id}/runners/{runner_id}/track", response_model=TrackResponse)
async def create_track(event_id: str, runner_id: str,
        gpxfile: Annotated[bytes, File()],
        service: TrackService = Depends(get_track_service)
):
    """
    Create a new track for an event and runner.
    """
    track_data = TrackEndpoint(
        event=UUID(event_id),
        runner=UUID(runner_id)
    )
    try:
        return await service.create(track_data, gpxfile)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


# Endpoint for retrieving all tracks
@track_router.get("/{event_id}/tracks", response_model=List[TrackResponse])
async def get_all_tracks(service: TrackService = Depends(get_track_service)):
    """
    Get a list of all tracks.
    """
    return await service.get_all()


# Endpoint for retrieving a specific track by its ID
@track_router.get("/{event_id}/runners/{runner_id}/track", response_model=TrackResponse)
async def get_track(track_id: UUID, service: TrackService = Depends(get_track_service)):
    """
    Get a specific track by its UUID.
    """
    track = await service.get_track(track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


# Endpoint for deleting a track by its ID
@track_router.delete("/{event_id}/runners/{runner_id}/track")
async def delete_track(track_id: UUID, service: TrackService = Depends(get_track_service)):
    """
    Delete a track by its UUID.
    """
    result = await service.delete(track_id)
    if result:
        return {"message": "Track deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Track not found")

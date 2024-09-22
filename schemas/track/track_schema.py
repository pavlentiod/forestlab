from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TrackData(BaseModel):
    distance: float
    elevation: float
    duration: float
    points: list


class TrackInput(BaseModel):
    event: Optional[UUID]
    runner: UUID
    distance: float
    elevation: float
    duration: float
    points: list


class TrackInDB(BaseModel):
    id: UUID
    event: Optional[UUID]
    runner: UUID
    distance: float
    elevation: float
    duration: float
    points: list

    @property
    def points_count(self):
        return len(self.points)


class TrackResponse(BaseModel):
    id: UUID
    event: Optional[UUID]
    runner: UUID
    distance: float
    elevation: float
    duration: float
    points_count: int


class TrackEndpoint(BaseModel): # + UploadFile in request
    runner: UUID
    event: UUID

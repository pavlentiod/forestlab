from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel


class EventInput(BaseModel):
    title: str = None
    source: str = None
    count: int = None
    status: bool = None
    date: datetime = None
    splits: str = None
    courses: str = None
    groups: str = None
    legs: str = None
    runners: str = None
    results: str = None


class EventInDB(BaseModel):
    id: UUID
    title: str
    source: str
    count: int
    status: bool
    splits: str
    date: datetime = None
    courses: str
    groups: str
    legs: str
    runners: str
    results: str


class EventEndpoint(BaseModel):
    title: str
    source: str
    date: date

class EventUpdate(BaseModel):
    title: str = None
    source: str = None
    date: datetime = None

class EventResponse(BaseModel):
    id: UUID
    title: str
    source: str
    count: int
    status: bool
    date: datetime
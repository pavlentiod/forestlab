from datetime import datetime
from uuid import UUID

from pandas import DataFrame
from pydantic import BaseModel


class EventInput(BaseModel):
    title: str = None
    source: str = None
    count: int = None
    status: bool = None
    splits: str = None
    courses: str = None
    date: datetime = None

class EventInDB(BaseModel):
    id: UUID
    title: str
    source: str
    count: int
    status: bool
    splits: str
    courses: str
    date: datetime

class EventEndpoint(BaseModel):
    title: str
    source: str
    date: datetime



from datetime import datetime
from typing import Optional, Dict, List
from uuid import UUID

from pydantic import BaseModel, Field


class LegOutput(BaseModel):
    id: UUID
    start: int
    end: int


class CourseOutput(BaseModel):
    id: UUID
    points: Dict[LegOutput]


class RunnerOutput(BaseModel):
    id: UUID
    name: str
    surname: str
    result: int
    course: CourseOutput
    group: UUID
    place: int
    data: Optional[dict]


class GroupOutput(BaseModel):
    id: UUID
    name: str
    runners: List[RunnerOutput]
    courses: List[CourseOutput]


class EventOutput(BaseModel):
    id: UUID
    title: str
    count: int
    date: datetime
    groups: List[GroupOutput]
    runners: List[RunnerOutput]
    courses: List[CourseOutput]
    legs: List[LegOutput]

from datetime import datetime
from typing import Dict, Optional, List
from uuid import UUID

from pydantic import BaseModel


class LegStatistics(BaseModel):
    pass

class CourseStatistics(BaseModel):
    pass

class RunnerLegGEOStatistics(BaseModel):
    length: int
    path: int
    ele: int


class RunnerLegStatistics(BaseModel):
    id: UUID
    split: Optional[int]
    gen_time: Optional[int]
    backlog: Optional[int]
    place: Optional[int]
    geo_stat: Optional[RunnerLegGEOStatistics] = None



class RunnerStatistics(BaseModel):
    place: int
    result: int
    course_stat: List[RunnerLegStatistics]


class LeaderBoard(BaseModel):
    id: UUID
    type: str
    leaderboard: Dict[UUID, int]
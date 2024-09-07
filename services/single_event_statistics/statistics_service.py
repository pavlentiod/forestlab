import json
from uuid import UUID

import pandas as pd

from src.schemas.event.event_schema import EventInDB
from src.schemas.single_event_statistics.single_event_schema import EventOutput, GroupOutput, CourseOutput, \
    RunnerOutput, LegOutput


class SingleEventStatisticsService:
    """
    GENERAL API SERVICE for calculate event, group and runner metrics on certain event(one day of event).
    """

    def __init__(self, event: EventInDB, group_id: UUID = None, runner_id: UUID = None, leg_id: UUID = None):
        self.event = event
        self.group_id = group_id
        self.runner_id = runner_id
        self.leg_id = leg_id

    def event(self) -> EventOutput:
        splits = pd.read_json(self.event.splits)
        courses = pd.read_json(self.event.courses)

    def group(self) -> GroupOutput:
        pass

    def course(self) -> CourseOutput:
        pass

    def runner(self) -> RunnerOutput:
        pass

    def leg(self) -> LegOutput:
        pass

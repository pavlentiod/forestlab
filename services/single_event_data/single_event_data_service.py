import json
from io import StringIO
from typing import List, Dict, Union
import datetime
from uuid import UUID

import numpy as np
import pandas as pd

from src.schemas.event.event_schema import EventInDB
from src.schemas.single_event_data.single_event_data_schema import EventOutput, GroupOutput, CourseOutput, RunnerOutput, \
    LegOutput

NANOSECONDS_TO_SECONDS = 1e9

class SingleEventDataService:
    """
    This class processes event data and provides methods to retrieve information about the event, its groups,
    courses, runners, and legs in different levels of nesting (for hierarchical data).
    """

    def __init__(self, event: EventInDB):
        """
        Initializes the service with event data.

        Args:
            event (EventInDB): The event data object from the database schema.
        """
        self.id: UUID = event.id
        self.title: str = event.title
        self.count: int = event.count
        self.source: str = event.source
        self.date: datetime.datetime = datetime.datetime.now()

        # Load splits and results as DataFrames, converting them to appropriate time formats.
        self.splits: pd.DataFrame = pd.read_json(StringIO(event.splits), orient="index").T / NANOSECONDS_TO_SECONDS

        self.results: pd.Series = pd.read_json(StringIO(event.results), orient="index").iloc[:,0] / NANOSECONDS_TO_SECONDS

        # Load other JSON-encoded event data.
        self.courses: Dict[str, Dict] = json.loads(event.courses)
        self.groups: Dict[str, Dict] = json.loads(event.groups)
        self.runners: Dict[str, Dict] = json.loads(event.runners)
        self.legs: Dict[str, Dict] = json.loads(event.legs)

    def get_event(self, nesting_level: int = 0) -> EventOutput:
        """
        Retrieves the full event information, including groups, runners, courses, and legs.

        Args:
            nesting_level (int): The level of detail (nesting) to include in the event's groups, courses, and runners.

        Returns:
            EventOutput: The complete event data structure.
        """
        groups = self.get_groups(nesting_level)
        runners = self.get_runners(nesting_level)
        courses = self.get_courses(nesting_level)

        event = {
            "id": self.id,
            "title": self.title,
            "count": self.count,
            "date": self.date,
            "source": self.source,
            "runners": runners,
            "groups": groups,
            "courses": courses,
            "legs": self.get_legs()
        }
        return EventOutput(**event)

    def get_group(self, group_id: str, nesting_level: int = 0) -> GroupOutput:
        """
        Retrieves information about a specific group.

        Args:
            group_id (str): The ID of the group to retrieve.
            nesting_level (int): The level of detail (nesting) to include in the group's runners and courses.

        Returns:
            GroupOutput: The complete group data structure.
        """
        group_db = self.groups[group_id]
        name = group_db['name']

        # Get the runners and courses associated with this group.
        group_runners_id = [i for i, v in self.runners.items() if v['group'] == group_id]
        group_courses_id = list(set([self.runners[r]['course'] for r in group_runners_id]))

        if nesting_level > 0:
            nesting_level -= 1
            runners = [self.get_runner(i, nesting_level=nesting_level) for i in group_runners_id]
            courses = [self.get_course(i, nesting_level=nesting_level) for i in group_courses_id]
        else:
            runners = [UUID(i) for i in group_runners_id]
            courses = [UUID(i) for i in group_courses_id]

        group = {
            "id": UUID(group_id),
            "name": name,
            "runners": runners,
            "courses": courses
        }
        return GroupOutput(**group)

    def get_groups(self, nesting_level: int = 0) -> List[GroupOutput]:
        """
        Retrieves all groups within the event.

        Args:
            nesting_level (int): The level of detail (nesting) to include in each group's runners and courses.

        Returns:
            List[GroupOutput]: A list of all group data structures.
        """
        return [self.get_group(i, nesting_level=nesting_level) for i in self.groups]

    def get_course(self, course_id: str, nesting_level: int = 0) -> CourseOutput:
        """
        Retrieves information about a specific course.

        Args:
            course_id (str): The ID of the course to retrieve.
            nesting_level (int): The level of detail (nesting) to include in the course's legs.

        Returns:
            CourseOutput: The complete course data structure.
        """
        course_db = self.courses[course_id]

        if nesting_level > 0:
            nesting_level -= 1
            points = {n: self.get_leg(course_db[n]) for n in course_db}
        else:
            points = course_db

        course = {"id": UUID(course_id), "points": points}
        return CourseOutput(**course)

    def get_courses(self, nesting_level: int = 0) -> List[CourseOutput]:
        """
        Retrieves all courses within the event.

        Args:
            nesting_level (int): The level of detail (nesting) to include in each course's legs.

        Returns:
            List[CourseOutput]: A list of all course data structures.
        """
        return [self.get_course(i, nesting_level=nesting_level) for i in self.courses]

    def get_runner(self, runner_id: str, nesting_level: int = 0) -> RunnerOutput:
        """
        Retrieves information about a specific runner.

        Args:
            runner_id (str): The ID of the runner to retrieve.
            nesting_level (int): The level of detail (nesting) to include in the runner's course.

        Returns:
            RunnerOutput: The complete runner data structure.
        """
        runner_db = self.runners[runner_id]
        name = runner_db['name'].split(' ')[-1]
        surname = runner_db['name'].split(' ')[0]

        if nesting_level > 0:
            nesting_level -= 1
            course = self.get_course(runner_db['course'], nesting_level=nesting_level)
        else:
            course = runner_db['course']

        group = UUID(runner_db['group'])
        result = self.results.loc[runner_id]

        runner = {
            "id": UUID(runner_id),
            "name": name,
            "surname": surname,
            "group": group,
            "course": course,
            "result": result
        }
        return RunnerOutput(**runner)

    def get_runners(self, nesting_level: int = 0) -> List[RunnerOutput]:
        """
        Retrieves all runners within the event.

        Args:
            nesting_level (int): The level of detail (nesting) to include in each runner's course.

        Returns:
            List[RunnerOutput]: A list of all runner data structures.
        """
        return [self.get_runner(i, nesting_level=nesting_level) for i in self.runners]

    def get_leg(self, leg_id: str) -> LegOutput:
        """
        Retrieves information about a specific leg.

        Args:
            leg_id (str): The ID of the leg to retrieve.

        Returns:
            LegOutput: The complete leg data structure.
        """
        leg_db = self.legs[leg_id]
        leg_db.setdefault("id", UUID(leg_id))
        return LegOutput(**leg_db)

    def get_legs(self) -> List[LegOutput]:
        """
        Retrieves all legs within the event.

        Returns:
            List[LegOutput]: A list of all leg data structures.
        """
        return [self.get_leg(leg_id) for leg_id in self.legs]

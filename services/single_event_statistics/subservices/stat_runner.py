from uuid import UUID
import pandas as pd
from pandas import Series
from typing import Dict, Tuple, Union

from src.schemas.single_event_statistics.single_event_statistics_schema import RunnerStatistics, RunnerLegStatistics
from src.services.single_event_data.single_event_data_service import SingleEventDataService
from src.services.single_event_statistics.subservices.stat_group import StatGroup
from src.services.single_event_statistics.subservices.stat_leg import StatLeg


class StatRunner:
    """
    Class representing a runner's statistics for a certain event.
    This class calculates personal statistics, such as split times, places, and leg backlogs.
    """

    def __init__(self, runner_id: str, service: SingleEventDataService):
        """
        Initializes a StatRunner object with the runner's ID and the event data service.

        Args:
            runner_id (str): The ID of the runner.
            service (SingleEventDataService): The service providing access to event data.
        """
        self.service: SingleEventDataService = service
        self.data: dict = self.service.get_runner(runner_id).to_str()  # Runner data from the service

    def get_runner_statistics(self, filter: str = "group") -> RunnerStatistics:
        """
        Calculates and returns the runner's statistics for the event.

        Args:
            filter (str): The filter to use when calculating statistics. Defaults to "group".
                          Options: "group", "all".

        Returns:
            RunnerStatistics: The runner's overall statistics for the event, including places, splits, and results.
        """
        # Collect split times, general times, places, backlogs, and final results
        splits = self.get_split().to_dict()
        general_times = self.get_general_times()
        leg_backlogs, leg_places = self.get_leg_backlogs_and_places(filter=filter)

        result = self.data['result']
        place = self.get_place()

        # Prepare the course_stat list for each leg
        course_stat = []
        for leg_id, split in splits.items():
            leg_stat = RunnerLegStatistics(
                id=UUID(leg_id),  # Convert leg_id to UUID
                split=split if split else None,
                gen_time=general_times.get(leg_id, 0) if split else None,
                backlog=leg_backlogs.get(leg_id, 0) if split else None,
                place=leg_places.get(leg_id, 0) if split else None
            )
            course_stat.append(leg_stat)

        # Return the final RunnerStatistics object
        return RunnerStatistics(
            place=place,
            result=result,
            course_stat=course_stat
        )

    def get_course(self) -> Dict[int, str]:
        """
        Retrieves the runner's course data, including the leg sequence.

        Returns:
            Dict[int, str]: A dictionary mapping the leg sequence number to the leg ID (as a string).
        """
        course_data = self.service.get_course(self.data['course']).dict()
        course = {n - 1: str(leg) for n, leg in course_data['points'].items()}
        return course

    def get_split(self) -> Series:
        """
        Retrieves the runner's split times for their course.

        Returns:
            Series: A pandas Series containing the runner's split times for each leg.
        """
        course = self.get_course()
        return self.service.splits.loc[self.data['id'], course.values()]

    def get_place(self) -> int:
        """
        Retrieves the runner's overall place within their group.

        Returns:
            int: The runner's place in their group.
        """
        group_service = StatGroup(self.data['group'], self.service)
        leaderboard = group_service.get_leaderboard()
        return leaderboard.index.to_list().index(self.data['id'])

    def get_general_times(self) -> Dict[str, Union[int, None]]:
        """
        Calculates the runner's general times (cumulative time at each leg).

        Returns:
            Dict[str, Union[int, None]]: A dictionary mapping leg IDs to the cumulative time in seconds
                                         or None if not applicable.
        """
        course = self.get_course()
        split_data = self.get_split()
        result = self.data['result']

        # Identify legs where splits were not recorded (timecut points)
        timecut_points = [n for n, value in enumerate(split_data) if not pd.notna(value)]
        if not timecut_points:
            timecut_points = [len(course)]

        general_times = {}
        for n, leg in course.items():
            if n < timecut_points[0]:
                general_times.setdefault(leg, split_data[:n + 1].sum())
            elif timecut_points[0] <= n <= timecut_points[-1]:
                general_times.setdefault(leg, None)
            elif n > timecut_points[-1]:
                general_times.setdefault(leg, result - split_data[n:].sum())

        # Convert times to integers (seconds)
        for k, v in general_times.items():
            if v:
                general_times[k] = int(v)

        return general_times

    def get_leg_backlogs_and_places(self, filter: str = "all") -> Tuple[Dict[str, int], Dict[str, int]]:
        """
        Calculates the runner's leg backlogs (time behind the leader) and places for each leg.

        Args:
            filter (str): The filter to use for the leaderboard. Defaults to "all".
                          Options: "group", "all".

        Returns:
            Tuple[Dict[str, int], Dict[str, int]]: Two dictionaries, one for backlogs and one for places,
                                                   both mapping leg IDs to their respective values.
        """
        split = self.get_split()
        leg_places = {}
        leg_backlogs = {}

        for leg in self.get_course().values():
            leg_service = StatLeg(leg, self.service)

            # Filter by group or use all participants
            if filter == "group":
                leaderboard = leg_service.get_leaderboard(group_id=self.data['group'])
            else:
                leaderboard = leg_service.get_leaderboard()

            # Get the runner's place and backlog for the leg
            leg_places.setdefault(leg, leaderboard.values.tolist().index(split[leg]) + 1)

            if split[leg] == leaderboard.values[0]:
                leg_backlogs.setdefault(leg, split[leg] - leaderboard.values[1])
            elif split[leg] > leaderboard.values[0]:
                leg_backlogs.setdefault(leg, split[leg] - leaderboard.values[0])

        # Convert backlogs to integers (seconds)
        for k, v in leg_backlogs.items():
            leg_backlogs[k] = int(v)

        return leg_backlogs, leg_places

from uuid import UUID

from src.schemas.event.event_schema import EventInDB
from src.schemas.single_event_statistics.single_event_statistics_schema import RunnerStatistics, LeaderBoard
from src.services.single_event_data.single_event_data_service import SingleEventDataService
from src.services.single_event_statistics.subservices.stat_course import StatCourse
from src.services.single_event_statistics.subservices.stat_group import StatGroup
from src.services.single_event_statistics.subservices.stat_leg import StatLeg
from src.services.single_event_statistics.subservices.stat_runner import StatRunner


class SingleEventStatisticsService:
    """
    GENERAL API SERVICE for calculate event, group and runner metrics on certain event(one day of event).
    """

    def __init__(self, event: EventInDB):
        self.event_data_service = SingleEventDataService(event=event)

    def get_runner_statisics(self, runner_id: str, filter: str = "all") -> RunnerStatistics:
        stat_service = StatRunner(runner_id, self.event_data_service)
        return stat_service.get_runner_statistics(filter=filter)

    def get_group_leaderboard(self, group_id: str) -> LeaderBoard:
        stat_service = StatGroup(group_id, self.event_data_service)
        leaderboard_data = stat_service.get_leaderboard()
        return LeaderBoard(id=UUID(group_id),
                           type="group",
                           leaderboard=leaderboard_data.to_dict())

    def get_leg_leaderboard(self, leg_id: str, group_id: str = None) -> LeaderBoard:
        stat_service = StatLeg(leg_id, self.event_data_service)
        leaderboard_data = stat_service.get_leaderboard(group_id)
        return LeaderBoard(id=UUID(leg_id),
                           type="leg",
                           leaderboard=leaderboard_data.to_dict())

    def get_course_leaderboard(self, course_id: str, group_id: str = None) -> LeaderBoard:
        stat_service = StatCourse(course_id, self.event_data_service)
        leaderboard_data = stat_service.get_leaderboard(group_id=group_id)
        return LeaderBoard(id=UUID(course_id),
                           type="course",
                           leaderboard=leaderboard_data.to_dict())

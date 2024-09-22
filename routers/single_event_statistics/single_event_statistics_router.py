from datetime import datetime

from fastapi import APIRouter, Depends

from src.routers.dependencies import get_event_statistics_service, get_geosplit_service
from src.schemas.single_event_statistics.single_event_statistics_schema import RunnerStatistics, LeaderBoard
from src.services.single_event_statistics.statistics_service import SingleEventStatisticsService
# Create a FastAPI router for event statistics
from src.services.single_event_statistics.subservices.geosplit.geosplit_service import GeoSplitService

event_statistics_router = APIRouter()


# Retrieve the statistics for a specific runner
@event_statistics_router.get("/{event_id}/statistics/runners/{runner_id}", response_model=RunnerStatistics)
async def get_runner_stats(
        runner_id: str,
        filter: str = None,
        start: datetime = "2024-09-15 09:51:00+00:00",
        service: SingleEventStatisticsService = Depends(get_event_statistics_service),
        geo_split_service: GeoSplitService = Depends(get_geosplit_service)
) -> RunnerStatistics:
    """
    Retrieve the statistics for a specific runner in a particular event.

    Args:
        runner_id (str): The ID of the runner whose statistics are being retrieved.
        filter (str, optional): An optional filter to apply to the statistics (e.g., by group).
        service (SingleEventStatisticsService): The event statistics service with injected event data.

    Returns:
        RunnerStatistics: A RunnerStatistics object containing the runner's performance data.
    """
    runner_stat = service.get_runner_statisics(runner_id, filter)
    if geo_split_service:
        runner_stat = geo_split_service.get_runner_legs_stat(runner_stat, course_start=start)
    return runner_stat

# Retrieve the leaderboard for a specific group
@event_statistics_router.get("/{event_id}/statistics/groups/{group_id}/leaderboard", response_model=LeaderBoard)
async def get_group_leaderboard(
        group_id: str,
        service: SingleEventStatisticsService = Depends(get_event_statistics_service)
) -> LeaderBoard:
    """
    Retrieve the leaderboard for a specific group in a particular event.

    Args:
        group_id (str): The ID of the group whose leaderboard is being retrieved.
        service (SingleEventStatisticsService): The event statistics service with injected event data.

    Returns:
        LeaderBoard: A LeaderBoard object containing the ranking of runners in the group.
    """
    return service.get_group_leaderboard(group_id)


# Retrieve the leaderboard for a specific leg
@event_statistics_router.get("/{event_id}/statistics/legs/{leg_id}/leaderboard", response_model=LeaderBoard)
async def get_leg_leaderboard(
        leg_id: str,
        group_id: str = None,
        service: SingleEventStatisticsService = Depends(get_event_statistics_service)
) -> LeaderBoard:
    """
    Retrieve the leaderboard for a specific leg in a particular event.
    Optionally, filter by group.

    Args:
        leg_id (str): The ID of the leg whose leaderboard is being retrieved.
        group_id (str, optional): The ID of the group to filter the leaderboard by (if applicable).
        service (SingleEventStatisticsService): The event statistics service with injected event data.

    Returns:
        LeaderBoard: A LeaderBoard object containing the ranking of runners in the leg.
    """
    return service.get_leg_leaderboard(leg_id, group_id)


# Retrieve the leaderboard for a specific course
@event_statistics_router.get("/{event_id}/statistics/courses/{course_id}/leaderboard", response_model=LeaderBoard)
async def get_course_leaderboard(
        course_id: str,
        group_id: str = None,
        service: SingleEventStatisticsService = Depends(get_event_statistics_service)
) -> LeaderBoard:
    """
    Retrieve the leaderboard for a specific course in a particular event.
    Optionally, filter by group.

    Args:
        course_id (str): The ID of the course whose leaderboard is being retrieved.
        group_id (str, optional): The ID of the group to filter the leaderboard by (if applicable).
        service (SingleEventStatisticsService): The event statistics service with injected event data.

    Returns:
        LeaderBoard: A LeaderBoard object containing the ranking of runners in the course.
    """
    return service.get_course_leaderboard(course_id, group_id)

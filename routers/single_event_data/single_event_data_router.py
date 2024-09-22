from fastapi import APIRouter, Depends
from typing import List

from src.schemas.event.event_schema import EventInDB
from src.schemas.single_event_data.single_event_data_schema import EventOutput, GroupOutput, CourseOutput, RunnerOutput, LegOutput
from src.routers.dependencies import event_by_id, get_event_data_service
from ...services.single_event_data.single_event_data_service import SingleEventDataService

# Create a FastAPI router for event data-related endpoints
event_data_router = APIRouter()



# Retrieve full event data
@event_data_router.get("/{event_id}", response_model=EventOutput)
async def get_event(
        service: SingleEventDataService = Depends(get_event_data_service),
        nesting_level: int = 0
):
    """
    Retrieves detailed information about the specified event.

    Args:
        service (SingleEventDataService): The event data service with injected event data.
        nesting_level (int, optional): The level of nesting for related data such as groups, courses, and runners.
                                       Default is 0 (no nesting).

    Returns:
        EventOutput: Complete event data including groups, runners, courses, and legs.
    """
    return service.get_event(nesting_level)

# Retrieve a specific group within the event
@event_data_router.get("/{event_id}/groups/{group_id}", response_model=GroupOutput)
async def get_group(
        group_id: str,
        service: SingleEventDataService = Depends(get_event_data_service),
        nesting_level: int = 0
):
    """
    Retrieves information about a specific group within the event.

    Args:
        group_id (str): The ID of the group to retrieve.
        service (SingleEventDataService): The event data service with injected event data.
        nesting_level (int, optional): The level of nesting for group details (runners and courses).
                                       Default is 0 (no nesting).

    Returns:
        GroupOutput: Detailed group data.
    """
    return service.get_group(group_id=group_id, nesting_level=nesting_level)

# Retrieve all groups within the event
@event_data_router.get("/{event_id}/groups", response_model=List[GroupOutput])
async def get_groups(
        service: SingleEventDataService = Depends(get_event_data_service),
        nesting_level: int = 0
):
    """
    Retrieves a list of all groups within the event.

    Args:
        service (SingleEventDataService): The event data service with injected event data.
        nesting_level (int, optional): The level of nesting for group details (runners and courses).
                                       Default is 0 (no nesting).

    Returns:
        List[GroupOutput]: A list of all group data within the event.
    """
    return service.get_groups(nesting_level)

# Retrieve a specific course within the event
@event_data_router.get("/{event_id}/courses/{course_id}", response_model=CourseOutput)
async def get_course(
        course_id: str,
        service: SingleEventDataService = Depends(get_event_data_service),
        nesting_level: int = 0
):
    """
    Retrieves information about a specific course within the event.

    Args:
        course_id (str): The ID of the course to retrieve.
        service (SingleEventDataService): The event data service with injected event data.
        nesting_level (int, optional): The level of nesting for course details (legs). Default is 0 (no nesting).

    Returns:
        CourseOutput: Detailed course data.
    """
    return service.get_course(course_id=course_id, nesting_level=nesting_level)

# Retrieve all courses within the event
@event_data_router.get("/{event_id}/courses", response_model=List[CourseOutput])
async def get_courses(
        service: SingleEventDataService = Depends(get_event_data_service),
        nesting_level: int = 0
):
    """
    Retrieves a list of all courses within the event.

    Args:
        service (SingleEventDataService): The event data service with injected event data.
        nesting_level (int, optional): The level of nesting for course details (legs). Default is 0 (no nesting).

    Returns:
        List[CourseOutput]: A list of all course data within the event.
    """
    return service.get_courses(nesting_level)

# Retrieve a specific runner within the event
@event_data_router.get("/{event_id}/runners/{runner_id}", response_model=RunnerOutput)
async def get_runner(
        runner_id: str,
        service: SingleEventDataService = Depends(get_event_data_service),
        nesting_level: int = 0
):
    """
    Retrieves information about a specific runner within the event.

    Args:
        runner_id (str): The ID of the runner to retrieve.
        service (SingleEventDataService): The event data service with injected event data.
        nesting_level (int, optional): The level of nesting for runner details (course). Default is 0 (no nesting).

    Returns:
        RunnerOutput: Detailed runner data.
    """
    return service.get_runner(runner_id=runner_id, nesting_level=nesting_level)

# Retrieve all runners within the event
@event_data_router.get("/{event_id}/runners", response_model=List[RunnerOutput])
async def get_runners(
        service: SingleEventDataService = Depends(get_event_data_service),
        nesting_level: int = 0
):
    """
    Retrieves a list of all runners within the event.

    Args:
        service (SingleEventDataService): The event data service with injected event data.
        nesting_level (int, optional): The level of nesting for runner details (course). Default is 0 (no nesting).

    Returns:
        List[RunnerOutput]: A list of all runner data within the event.
    """
    return service.get_runners(nesting_level)

# Retrieve a specific leg within the event
@event_data_router.get("/{event_id}/legs/{leg_id}", response_model=LegOutput)
async def get_leg(
        leg_id: str,
        service: SingleEventDataService = Depends(get_event_data_service)
):
    """
    Retrieves information about a specific leg within the event.

    Args:
        leg_id (str): The ID of the leg to retrieve.
        service (SingleEventDataService): The event data service with injected event data.

    Returns:
        LegOutput: Detailed leg data.
    """
    return service.get_leg(leg_id)

# Retrieve all legs within the event
@event_data_router.get("/{event_id}/legs", response_model=List[LegOutput])
async def get_legs(
        service: SingleEventDataService = Depends(get_event_data_service)
):
    """
    Retrieves a list of all legs within the event.

    Args:
        service (SingleEventDataService): The event data service with injected event data.

    Returns:
        List[LegOutput]: A list of all leg data within the event.
    """
    return service.get_legs()

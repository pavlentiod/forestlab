from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db_helper
from src.routers.dependencies import get_event_service
from src.schemas.event.event_schema import EventEndpoint, EventResponse, EventUpdate
from src.services.event.event_service import EventService

# Create a FastAPI router for event-related endpoints
event_router = APIRouter()

# Define a dependency to get EventService with injected session


@event_router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
        event_input: EventEndpoint,
        service: EventService = Depends(get_event_service)
) -> EventResponse:
    """
    Create a new event.

    Args:
        event_input (EventEndpoint): The input data for creating a new event.
        service (EventService, optional): The EventService instance with the database session injected.

    Returns:
        EventResponse: The created event's response data.
    """
    return await service.create(data_from_api=event_input)

@event_router.patch("/{event_id}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def update_event(
        event_id: str,
        event_update: EventUpdate,
        service: EventService = Depends(get_event_service)
) -> EventResponse:
    """
    Update an existing event.

    Args:
        event_id (str): The ID of the event to be updated.
        event_update (EventUpdate): The updated event data.
        service (EventService, optional): The EventService instance with the database session injected.

    Returns:
        EventResponse: The updated event's response data.
    """
    return await service.update(event_id, data=event_update)

@event_router.delete("/{event_id}")
async def delete_event(
        event_id: str,
        service: EventService = Depends(get_event_service)
) -> bool:
    """
    Delete an event by its ID.

    Args:
        event_id (str): The ID of the event to be deleted.
        service (EventService, optional): The EventService instance with the database session injected.

    Returns:
        bool: A boolean confirming the deletion of the event.
    """
    return await service.delete(event_id)

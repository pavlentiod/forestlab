import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from src.schemas.event.event_schema import EventInput
from src.service.event.event_service import EventService


@pytest.fixture
def sample_event_data() -> EventInput:
    return EventInput(
        # Add sample data fields here
    )

@pytest.fixture
def updated_event_data() -> EventInput:
    return EventInput(
        # Add updated data fields here
    )

async def test_create_event(session: AsyncSession, sample_event_data: EventInput):
    service = EventService(session)

    # Create a new event
    created_event = await service.create(sample_event_data)

    # Verify the created event has the expected attributes
    assert created_event.field == sample_event_data.field  # Replace 'field' with actual field names

    # Try to create the same event again (should raise HTTPException)
    # with pytest.raises(HTTPException):
    #     await service.create(sample_event_data)

    # Clean up by deleting the created event (if necessary)
    await service.delete(created_event.id)


async def test_get_all_events(session: AsyncSession):
    service = EventService(session)

    # Retrieve all events (expecting at least one)
    all_events = await service.get_all()
    assert len(all_events) > 0

    # Clean up by deleting all events (if necessary)
    for event in all_events:
        await service.delete(event.id)


async def test_get_event_by_id(session: AsyncSession, sample_event_data: EventInput):
    service = EventService(session)

    # Create a new event
    created_event = await service.create(sample_event_data)

    # Retrieve the event by ID
    retrieved_event = await service.get_event(created_event.id)

    # Verify the retrieved event matches the created event
    assert retrieved_event.field == sample_event_data.field  # Replace 'field' with actual field names

    # Try to retrieve a non-existent event (should raise HTTPException)
    with pytest.raises(HTTPException):
        await service.get_event(uuid4())

    # Clean up by deleting the created event
    await service.delete(created_event.id)


async def test_update_event(session: AsyncSession, sample_event_data: EventInput, updated_event_data: EventInput):
    service = EventService(session)

    # Create a new event
    created_event = await service.create(sample_event_data)

    # Update the event's information
    updated_event = await service.update(created_event.id, updated_event_data)

    # Verify the updated event has the new attributes
    assert updated_event.field == updated_event_data.field  # Replace 'field' with actual field names

    # Try to update a non-existent event (should raise HTTPException)
    with pytest.raises(HTTPException):
        await service.update(uuid4(), updated_event_data)

    # Clean up by deleting the created event
    await service.delete(created_event.id)


async def test_delete_event(session: AsyncSession, sample_event_data: EventInput):
    service = EventService(session)

    # Create a new event
    created_event = await service.create(sample_event_data)

    # Delete the event and verify
    result = await service.delete(created_event.id)
    assert result is True

    # Try to delete a non-existent event (should raise HTTPException)
    with pytest.raises(HTTPException):
        await service.delete(uuid4())

    # Clean up by deleting the created event (if necessary)
    # Note: Depending on your implementation, the event might already be deleted in the previous step.

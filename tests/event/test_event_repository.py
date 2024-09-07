import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.event.event_repository import EventRepository
from src.schemas.event.event_schema import EventInput


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


async def test_create(session: AsyncSession, sample_event_data: EventInput):
    event_repository = EventRepository(session=session)
    event = await event_repository.create(sample_event_data)

    assert event.field == sample_event_data.field  # Replace 'field' with actual field names

async def test_get_all(session: AsyncSession, sample_event_data: EventInput):
    event_repository = EventRepository(session=session)
    await event_repository.create(sample_event_data)
    events = await event_repository.get_all()

    assert len(events) > 0
    assert events[0].field == sample_event_data.field  # Replace 'field' with actual field names

async def test_get_event(session: AsyncSession, sample_event_data: EventInput):
    event_repository = EventRepository(session=session)
    created_event = await event_repository.create(sample_event_data)
    event = await event_repository.get_event(created_event.id)

    assert event.field == sample_event_data.field  # Replace 'field' with actual field names
    assert event.id == created_event.id

async def test_get_by_id(session: AsyncSession, sample_event_data: EventInput):
    event_repository = EventRepository(session=session)
    created_event = await event_repository.create(sample_event_data)
    event = await event_repository.get_by_id(created_event.id)

    assert event is not None
    assert event.id == created_event.id

async def test_update(session: AsyncSession, sample_event_data: EventInput, updated_event_data: EventInput):
    event_repository = EventRepository(session=session)
    created_event = await event_repository.create(sample_event_data)
    event = await event_repository.get_by_id(created_event.id)
    updated_event = await event_repository.update(event, updated_event_data)

    assert updated_event.field == updated_event_data.field  # Replace 'field' with actual field names

async def test_delete(session: AsyncSession, sample_event_data: EventInput):
    event_repository = EventRepository(session=session)
    created_event = await event_repository.create(sample_event_data)
    event = await event_repository.get_by_id(created_event.id)
    success = await event_repository.delete(event)

    assert success is True
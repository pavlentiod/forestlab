import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from src.schemas.leg.leg_schema import LegInput
from src.service.leg.leg_service import LegService


@pytest.fixture
def sample_leg_data() -> LegInput:
    return LegInput(
        # Add sample data fields here
    )

@pytest.fixture
def updated_leg_data() -> LegInput:
    return LegInput(
        # Add updated data fields here
    )

async def test_create_leg(session: AsyncSession, sample_leg_data: LegInput):
    service = LegService(session)

    # Create a new leg
    created_leg = await service.create(sample_leg_data)

    # Verify the created leg has the expected attributes
    assert created_leg.field == sample_leg_data.field  # Replace 'field' with actual field names

    # Try to create the same leg again (should raise HTTPException)
    # with pytest.raises(HTTPException):
    #     await service.create(sample_leg_data)

    # Clean up by deleting the created leg (if necessary)
    await service.delete(created_leg.id)


async def test_get_all_legs(session: AsyncSession):
    service = LegService(session)

    # Retrieve all legs (expecting at least one)
    all_legs = await service.get_all()
    assert len(all_legs) > 0

    # Clean up by deleting all legs (if necessary)
    for leg in all_legs:
        await service.delete(leg.id)


async def test_get_leg_by_id(session: AsyncSession, sample_leg_data: LegInput):
    service = LegService(session)

    # Create a new leg
    created_leg = await service.create(sample_leg_data)

    # Retrieve the leg by ID
    retrieved_leg = await service.get_leg(created_leg.id)

    # Verify the retrieved leg matches the created leg
    assert retrieved_leg.field == sample_leg_data.field  # Replace 'field' with actual field names

    # Try to retrieve a non-existent leg (should raise HTTPException)
    with pytest.raises(HTTPException):
        await service.get_leg(uuid4())

    # Clean up by deleting the created leg
    await service.delete(created_leg.id)


async def test_update_leg(session: AsyncSession, sample_leg_data: LegInput, updated_leg_data: LegInput):
    service = LegService(session)

    # Create a new leg
    created_leg = await service.create(sample_leg_data)

    # Update the leg's information
    updated_leg = await service.update(created_leg.id, updated_leg_data)

    # Verify the updated leg has the new attributes
    assert updated_leg.field == updated_leg_data.field  # Replace 'field' with actual field names

    # Try to update a non-existent leg (should raise HTTPException)
    with pytest.raises(HTTPException):
        await service.update(uuid4(), updated_leg_data)

    # Clean up by deleting the created leg
    await service.delete(created_leg.id)


async def test_delete_leg(session: AsyncSession, sample_leg_data: LegInput):
    service = LegService(session)

    # Create a new leg
    created_leg = await service.create(sample_leg_data)

    # Delete the leg and verify
    result = await service.delete(created_leg.id)
    assert result is True

    # Try to delete a non-existent leg (should raise HTTPException)
    with pytest.raises(HTTPException):
        await service.delete(uuid4())

    # Clean up by deleting the created leg (if necessary)
    # Note: Depending on your implementation, the leg might already be deleted in the previous step.

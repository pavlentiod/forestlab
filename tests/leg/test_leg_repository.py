import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.leg.leg_repository import LegRepository
from src.schemas.leg.leg_schema import LegInput


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


async def test_create(session: AsyncSession, sample_leg_data: LegInput):
    leg_repository = LegRepository(session=session)
    leg = await leg_repository.create(sample_leg_data)

    assert leg.field == sample_leg_data.field  # Replace 'field' with actual field names

async def test_get_all(session: AsyncSession, sample_leg_data: LegInput):
    leg_repository = LegRepository(session=session)
    await leg_repository.create(sample_leg_data)
    legs = await leg_repository.get_all()

    assert len(legs) > 0
    assert legs[0].field == sample_leg_data.field  # Replace 'field' with actual field names

async def test_get_leg(session: AsyncSession, sample_leg_data: LegInput):
    leg_repository = LegRepository(session=session)
    created_leg = await leg_repository.create(sample_leg_data)
    leg = await leg_repository.get_leg(created_leg.id)

    assert leg.field == sample_leg_data.field  # Replace 'field' with actual field names
    assert leg.id == created_leg.id

async def test_get_by_id(session: AsyncSession, sample_leg_data: LegInput):
    leg_repository = LegRepository(session=session)
    created_leg = await leg_repository.create(sample_leg_data)
    leg = await leg_repository.get_by_id(created_leg.id)

    assert leg is not None
    assert leg.id == created_leg.id

async def test_update(session: AsyncSession, sample_leg_data: LegInput, updated_leg_data: LegInput):
    leg_repository = LegRepository(session=session)
    created_leg = await leg_repository.create(sample_leg_data)
    leg = await leg_repository.get_by_id(created_leg.id)
    updated_leg = await leg_repository.update(leg, updated_leg_data)

    assert updated_leg.field == updated_leg_data.field  # Replace 'field' with actual field names

async def test_delete(session: AsyncSession, sample_leg_data: LegInput):
    leg_repository = LegRepository(session=session)
    created_leg = await leg_repository.create(sample_leg_data)
    leg = await leg_repository.get_by_id(created_leg.id)
    success = await leg_repository.delete(leg)

    assert success is True
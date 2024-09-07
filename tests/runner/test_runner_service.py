import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from src.schemas.runner.runner_schema import RunnerInput
from src.service.runner.runner_service import RunnerService


@pytest.fixture
def sample_runner_data() -> RunnerInput:
    return RunnerInput(
        # Add sample data fields here
    )

@pytest.fixture
def updated_runner_data() -> RunnerInput:
    return RunnerInput(
        # Add updated data fields here
    )

async def test_create_runner(session: AsyncSession, sample_runner_data: RunnerInput):
    service = RunnerService(session)

    # Create a new runner
    created_runner = await service.create(sample_runner_data)

    # Verify the created runner has the expected attributes
    assert created_runner.field == sample_runner_data.field  # Replace 'field' with actual field names

    # Try to create the same runner again (should raise HTTPException)
    # with pytest.raises(HTTPException):
    #     await service.create(sample_runner_data)

    # Clean up by deleting the created runner (if necessary)
    await service.delete(created_runner.id)


async def test_get_all_runners(session: AsyncSession):
    service = RunnerService(session)

    # Retrieve all runners (expecting at least one)
    all_runners = await service.get_all()
    assert len(all_runners) > 0

    # Clean up by deleting all runners (if necessary)
    for runner in all_runners:
        await service.delete(runner.id)


async def test_get_runner_by_id(session: AsyncSession, sample_runner_data: RunnerInput):
    service = RunnerService(session)

    # Create a new runner
    created_runner = await service.create(sample_runner_data)

    # Retrieve the runner by ID
    retrieved_runner = await service.get_runner(created_runner.id)

    # Verify the retrieved runner matches the created runner
    assert retrieved_runner.field == sample_runner_data.field  # Replace 'field' with actual field names

    # Try to retrieve a non-existent runner (should raise HTTPException)
    with pytest.raises(HTTPException):
        await service.get_runner(uuid4())

    # Clean up by deleting the created runner
    await service.delete(created_runner.id)


async def test_update_runner(session: AsyncSession, sample_runner_data: RunnerInput, updated_runner_data: RunnerInput):
    service = RunnerService(session)

    # Create a new runner
    created_runner = await service.create(sample_runner_data)

    # Update the runner's information
    updated_runner = await service.update(created_runner.id, updated_runner_data)

    # Verify the updated runner has the new attributes
    assert updated_runner.field == updated_runner_data.field  # Replace 'field' with actual field names

    # Try to update a non-existent runner (should raise HTTPException)
    with pytest.raises(HTTPException):
        await service.update(uuid4(), updated_runner_data)

    # Clean up by deleting the created runner
    await service.delete(created_runner.id)


async def test_delete_runner(session: AsyncSession, sample_runner_data: RunnerInput):
    service = RunnerService(session)

    # Create a new runner
    created_runner = await service.create(sample_runner_data)

    # Delete the runner and verify
    result = await service.delete(created_runner.id)
    assert result is True

    # Try to delete a non-existent runner (should raise HTTPException)
    with pytest.raises(HTTPException):
        await service.delete(uuid4())

    # Clean up by deleting the created runner (if necessary)
    # Note: Depending on your implementation, the runner might already be deleted in the previous step.

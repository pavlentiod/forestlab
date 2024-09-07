import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.runner.runner_repository import RunnerRepository
from src.schemas.runner.runner_schema import RunnerInput


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


async def test_create(session: AsyncSession, sample_runner_data: RunnerInput):
    runner_repository = RunnerRepository(session=session)
    runner = await runner_repository.create(sample_runner_data)

    assert runner.field == sample_runner_data.field  # Replace 'field' with actual field names

async def test_get_all(session: AsyncSession, sample_runner_data: RunnerInput):
    runner_repository = RunnerRepository(session=session)
    await runner_repository.create(sample_runner_data)
    runners = await runner_repository.get_all()

    assert len(runners) > 0
    assert runners[0].field == sample_runner_data.field  # Replace 'field' with actual field names

async def test_get_runner(session: AsyncSession, sample_runner_data: RunnerInput):
    runner_repository = RunnerRepository(session=session)
    created_runner = await runner_repository.create(sample_runner_data)
    runner = await runner_repository.get_runner(created_runner.id)

    assert runner.field == sample_runner_data.field  # Replace 'field' with actual field names
    assert runner.id == created_runner.id

async def test_get_by_id(session: AsyncSession, sample_runner_data: RunnerInput):
    runner_repository = RunnerRepository(session=session)
    created_runner = await runner_repository.create(sample_runner_data)
    runner = await runner_repository.get_by_id(created_runner.id)

    assert runner is not None
    assert runner.id == created_runner.id

async def test_update(session: AsyncSession, sample_runner_data: RunnerInput, updated_runner_data: RunnerInput):
    runner_repository = RunnerRepository(session=session)
    created_runner = await runner_repository.create(sample_runner_data)
    runner = await runner_repository.get_by_id(created_runner.id)
    updated_runner = await runner_repository.update(runner, updated_runner_data)

    assert updated_runner.field == updated_runner_data.field  # Replace 'field' with actual field names

async def test_delete(session: AsyncSession, sample_runner_data: RunnerInput):
    runner_repository = RunnerRepository(session=session)
    created_runner = await runner_repository.create(sample_runner_data)
    runner = await runner_repository.get_by_id(created_runner.id)
    success = await runner_repository.delete(runner)

    assert success is True
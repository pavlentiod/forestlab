import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.group.group_repository import GroupRepository
from src.schemas.group.group_schema import GroupInput


@pytest.fixture
def sample_group_data() -> GroupInput:
    return GroupInput(
        # Add sample data fields here
    )

@pytest.fixture
def updated_group_data() -> GroupInput:
    return GroupInput(
        # Add updated data fields here
    )


async def test_create(session: AsyncSession, sample_group_data: GroupInput):
    group_repository = GroupRepository(session=session)
    group = await group_repository.create(sample_group_data)

    assert group.field == sample_group_data.field  # Replace 'field' with actual field names

async def test_get_all(session: AsyncSession, sample_group_data: GroupInput):
    group_repository = GroupRepository(session=session)
    await group_repository.create(sample_group_data)
    groups = await group_repository.get_all()

    assert len(groups) > 0
    assert groups[0].field == sample_group_data.field  # Replace 'field' with actual field names

async def test_get_group(session: AsyncSession, sample_group_data: GroupInput):
    group_repository = GroupRepository(session=session)
    created_group = await group_repository.create(sample_group_data)
    group = await group_repository.get_group(created_group.id)

    assert group.field == sample_group_data.field  # Replace 'field' with actual field names
    assert group.id == created_group.id

async def test_get_by_id(session: AsyncSession, sample_group_data: GroupInput):
    group_repository = GroupRepository(session=session)
    created_group = await group_repository.create(sample_group_data)
    group = await group_repository.get_by_id(created_group.id)

    assert group is not None
    assert group.id == created_group.id

async def test_update(session: AsyncSession, sample_group_data: GroupInput, updated_group_data: GroupInput):
    group_repository = GroupRepository(session=session)
    created_group = await group_repository.create(sample_group_data)
    group = await group_repository.get_by_id(created_group.id)
    updated_group = await group_repository.update(group, updated_group_data)

    assert updated_group.field == updated_group_data.field  # Replace 'field' with actual field names

async def test_delete(session: AsyncSession, sample_group_data: GroupInput):
    group_repository = GroupRepository(session=session)
    created_group = await group_repository.create(sample_group_data)
    group = await group_repository.get_by_id(created_group.id)
    success = await group_repository.delete(group)

    assert success is True
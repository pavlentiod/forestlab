import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from src.schemas.group.group_schema import GroupInput
from src.service.group.group_service import GroupService


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

async def test_create_group(session: AsyncSession, sample_group_data: GroupInput):
    service = GroupService(session)

    # Create a new group
    created_group = await service.create(sample_group_data)

    # Verify the created group has the expected attributes
    assert created_group.field == sample_group_data.field  # Replace 'field' with actual field names

    # Try to create the same group again (should raise HTTPException)
    # with pytest.raises(HTTPException):
    #     await service.create(sample_group_data)

    # Clean up by deleting the created group (if necessary)
    await service.delete(created_group.id)


async def test_get_all_groups(session: AsyncSession):
    service = GroupService(session)

    # Retrieve all groups (expecting at least one)
    all_groups = await service.get_all()
    assert len(all_groups) > 0

    # Clean up by deleting all groups (if necessary)
    for group in all_groups:
        await service.delete(group.id)


async def test_get_group_by_id(session: AsyncSession, sample_group_data: GroupInput):
    service = GroupService(session)

    # Create a new group
    created_group = await service.create(sample_group_data)

    # Retrieve the group by ID
    retrieved_group = await service.get_group(created_group.id)

    # Verify the retrieved group matches the created group
    assert retrieved_group.field == sample_group_data.field  # Replace 'field' with actual field names

    # Try to retrieve a non-existent group (should raise HTTPException)
    with pytest.raises(HTTPException):
        await service.get_group(uuid4())

    # Clean up by deleting the created group
    await service.delete(created_group.id)


async def test_update_group(session: AsyncSession, sample_group_data: GroupInput, updated_group_data: GroupInput):
    service = GroupService(session)

    # Create a new group
    created_group = await service.create(sample_group_data)

    # Update the group's information
    updated_group = await service.update(created_group.id, updated_group_data)

    # Verify the updated group has the new attributes
    assert updated_group.field == updated_group_data.field  # Replace 'field' with actual field names

    # Try to update a non-existent group (should raise HTTPException)
    with pytest.raises(HTTPException):
        await service.update(uuid4(), updated_group_data)

    # Clean up by deleting the created group
    await service.delete(created_group.id)


async def test_delete_group(session: AsyncSession, sample_group_data: GroupInput):
    service = GroupService(session)

    # Create a new group
    created_group = await service.create(sample_group_data)

    # Delete the group and verify
    result = await service.delete(created_group.id)
    assert result is True

    # Try to delete a non-existent group (should raise HTTPException)
    with pytest.raises(HTTPException):
        await service.delete(uuid4())

    # Clean up by deleting the created group (if necessary)
    # Note: Depending on your implementation, the group might already be deleted in the previous step.

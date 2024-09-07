from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import UUID4

from src.database import db_helper
from src.services.group.group_service import GroupService
from src.schemas.group.group_schema import GroupInput, GroupOutput

router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED, response_model=GroupOutput)
async def create_group(
        data: GroupInput,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = GroupService(session)
    return await _service.create(data)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[GroupOutput])
async def get_groups(session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> List[GroupOutput]:
    _service = GroupService(session)
    return await _service.get_all()

@router.get("/{_id}", status_code=status.HTTP_200_OK, response_model=GroupOutput)
async def get_group(
        _id: UUID4,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = GroupService(session)
    return await _service.get_group(_id)

@router.put("/{_id}", status_code=status.HTTP_200_OK, response_model=GroupOutput)
async def update_group(
        _id: UUID4,
        data: GroupInput,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = GroupService(session)
    return await _service.update(_id, data)

@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
        _id: UUID4,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = GroupService(session)
    await _service.delete(_id)
    return {"detail": "group deleted successfully"}
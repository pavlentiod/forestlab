from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import UUID4

from src.database import db_helper
from src.services.runner.runner_service import RunnerService
from src.schemas.runner.runner_schema import RunnerInput, RunnerOutput

router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED, response_model=RunnerOutput)
async def create_runner(
        data: RunnerInput,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = RunnerService(session)
    return await _service.create(data)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[RunnerOutput])
async def get_runners(session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> List[RunnerOutput]:
    _service = RunnerService(session)
    return await _service.get_all()

@router.get("/{_id}", status_code=status.HTTP_200_OK, response_model=RunnerOutput)
async def get_runner(
        _id: UUID4,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = RunnerService(session)
    return await _service.get_runner(_id)

@router.put("/{_id}", status_code=status.HTTP_200_OK, response_model=RunnerOutput)
async def update_runner(
        _id: UUID4,
        data: RunnerInput,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = RunnerService(session)
    return await _service.update(_id, data)

@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_runner(
        _id: UUID4,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = RunnerService(session)
    await _service.delete(_id)
    return {"detail": "runner deleted successfully"}
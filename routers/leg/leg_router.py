from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import UUID4

from src.database import db_helper
from src.services.leg.leg_service import LegService
from src.schemas.leg.leg_schema import LegInput, LegOutput

router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED, response_model=LegOutput)
async def create_leg(
        data: LegInput,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = LegService(session)
    return await _service.create(data)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[LegOutput])
async def get_legs(session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> List[LegOutput]:
    _service = LegService(session)
    return await _service.get_all()

@router.get("/{_id}", status_code=status.HTTP_200_OK, response_model=LegOutput)
async def get_leg(
        _id: UUID4,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = LegService(session)
    return await _service.get_leg(_id)

@router.put("/{_id}", status_code=status.HTTP_200_OK, response_model=LegOutput)
async def update_leg(
        _id: UUID4,
        data: LegInput,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = LegService(session)
    return await _service.update(_id, data)

@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_leg(
        _id: UUID4,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = LegService(session)
    await _service.delete(_id)
    return {"detail": "leg deleted successfully"}
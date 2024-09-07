from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import UUID4

from src.database import db_helper
from src.services.event.event_service import EventService
from src.schemas.event.event_schema import EventInput, EventOutput

router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED, response_model=EventOutput)
async def create_event(
        data: EventInput,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = EventService(session)
    return await _service.create(data)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[EventOutput])
async def get_events(session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> List[EventOutput]:
    _service = EventService(session)
    return await _service.get_all()

@router.get("/{_id}", status_code=status.HTTP_200_OK, response_model=EventOutput)
async def get_event(
        _id: UUID4,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = EventService(session)
    return await _service.get_event(_id)

@router.put("/{_id}", status_code=status.HTTP_200_OK, response_model=EventOutput)
async def update_event(
        _id: UUID4,
        data: EventInput,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = EventService(session)
    return await _service.update(_id, data)

@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
        _id: UUID4,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    _service = EventService(session)
    await _service.delete(_id)
    return {"detail": "event deleted successfully"}
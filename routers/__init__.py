from fastapi import APIRouter

from src.routers.events.events_router import event_router
from src.routers.single_event_data.single_event_data_router import event_data_router
from src.routers.single_event_statistics.single_event_statistics_router import event_statistics_router
from src.routers.track.track_router import track_router

router = APIRouter()
router.include_router(event_router, prefix='/events', tags=['Event'])
router.include_router(event_data_router, prefix='/events', tags=['Events'])
router.include_router(event_statistics_router, prefix='/events', tags=['Event statistics'])
router.include_router(track_router, prefix='/events', tags=['Tracks'])

__all__ = [router]
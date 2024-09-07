from fastapi import APIRouter
from .group.group_router import router as group_router
from .event.event_router import router as event_router
from .runner.runner_router import router as runner_router
router = APIRouter()
router.include_router(group_router, prefix='/group', tags=['Group'])
router.include_router(event_router, prefix='/event', tags=['Event'])
router.include_router(runner_router, prefix='/runner', tags=['Runner'])
from fastapi import APIRouter

from app.api.api_v1.endpoints import root, scheduleblocks, timetables, users

api_router = APIRouter()

api_router.include_router(root.router, tags=["root"])
api_router.include_router(scheduleblocks.router, tags=["scheduleblocks"])
api_router.include_router(timetables.router, tags=["timetables"])
api_router.include_router(users.router, tags=["users"])

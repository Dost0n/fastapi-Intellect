from fastapi import APIRouter
from routers import user_route, intellect_route, login_route, log_route, activity_route

api_router = APIRouter()


api_router.include_router(user_route.router,      prefix="/users",      tags=["users"])
api_router.include_router(intellect_route.router, prefix="/intellect",  tags=["intellect"])
api_router.include_router(login_route.router,     prefix="/login",      tags=["login"])
api_router.include_router(log_route.router,       prefix="/logs",       tags=["log"])
api_router.include_router(activity_route.router,  prefix="/activities", tags=["activities"])
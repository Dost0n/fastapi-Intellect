from fastapi import FastAPI
from routers.base import api_router
from core.config import settings
from db.session import engine
from db.models import Base
from fastapi.middleware.cors import CORSMiddleware



ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://172.16.0.54:3000",
    "http://172.16.0.54:3001",
    "http://172.16.0.30:8080",
    "http://172.16.0.54:8080"

]

def include_router(app):
    app.include_router(api_router, prefix="/api/v1")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    include_router(app)
    create_tables()
    return app 


app = start_application()
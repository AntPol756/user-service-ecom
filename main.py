from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.controllers.user_controller import router as user_router
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.include_router(user_router)

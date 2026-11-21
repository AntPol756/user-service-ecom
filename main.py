from fastapi import FastAPI

from app.config import settings
from app.controllers.user_controller import router as user_router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)
app.include_router(user_router)
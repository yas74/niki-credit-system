from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.settings import settings
from app.core.database import mongo_db
from app.api.health import router as health_router
from app.api.staff import router as staff_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await mongo_db.connect()

    yield

    # Shutdown
    await mongo_db.close()

def create_app():
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan
    )

    app.include_router(health_router)
    app.include_router(staff_router)

    return app


app = create_app()


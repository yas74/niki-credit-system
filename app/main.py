from fastapi import FastAPI

from app.core.settings import settings
from app.api.health import router as health_router


def create_app():
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )

    app.include_router(health_router)

    return app

app = create_app()
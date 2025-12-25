from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.settings import settings
from app.models.staff import Staff
from app.models.user import User
from app.models.session import Session


class MongoDatabase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient | None = None

    async def connect(self) -> None:
        self.client = AsyncIOMotorClient(settings.mongodb_uri)

        await init_beanie(
            database=self.client[settings.mongodb_db],
            document_models=[
                User,
                Session,
                Staff
            ]
        )

    async def close(self) -> None:
        if self.client:
            self.client.close()


mongo_db = MongoDatabase()

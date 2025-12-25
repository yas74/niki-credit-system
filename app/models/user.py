from typing import Optional, Annotated
from enum import Enum
from datetime import datetime

from beanie import Document, Indexed
from pydantic import Field

from app.core.time import utc_now

class UserRole(str, Enum):
    STAFF = "staff"
    SUPERUSER = "superuser"

class User(Document):
    username: Annotated[str, Indexed(unique=True)]
    phone_number: Annotated[str, Indexed(unique=True)]

    first_name: Optional[str] = None
    last_name: Optional[str] = None

    password_hash: str
    role: UserRole = UserRole.STAFF
    is_active: bool = True

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    class Settings:
        name = "users"

    async def save(self, *args, **kwargs):
        self.updated_at = utc_now
        return await super().save(*args, **kwargs)
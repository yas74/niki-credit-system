from typing import Annotated, Optional
from datetime import datetime

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field

from app.core.time import utc_now


class Session(Document):
    user_id: PydanticObjectId

    refresh_token_hash: str
    jti: Annotated[str, Indexed(uinque=True)]

    created_at: datetime = Field(default_factory=utc_now)
    expires_at: datetime 
    revoked_at: Optional[datetime] = None

    user_agent: Optional[str] = None
    ip_address: Optional[str] = None

    class Settings:
        name = "sessions"

    @property
    def is_active(self) -> bool:
        return self.revoked_at is None and self.expires_at > utc_now 
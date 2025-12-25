from datetime import timedelta
from typing import Any, Dict
from uuid import uuid4

import jwt

from app.core.time import utc_now
from app.core.settings import settings


def create_access_token(
        subject: str,
        expires_delta: timedelta | None = None
) -> str:
    expire = utc_now + (expires_delta or timedelta(minutes=5))

    payload: Dict[str, Any] = {
        "sub": subject,
        "type": "access",
        "exp": expire,
        "jti": str(uuid4())
    }

    return jwt.encode(payload, settings.access_token_secret, algorithm="HS256")

def create_refresh_token(
        subject: str,
        expires_delta: timedelta | None = None
) -> tuple[str, str]:
    expire = utc_now + (expires_delta or timedelta(days=7))
    jti = str(uuid4())

    payload: Dict[str, Any] = {
        "sub": subject,
        "type": "refresh",
        "exp": expire,
        "jti": jti
    }
    token = jwt.encode(payload, settings.refresh_token_secret, algorithm="HS256")

    return token, jti

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.access_token_secret, algorithms=["HS256"])

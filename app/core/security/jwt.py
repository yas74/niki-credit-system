from datetime import timedelta
from typing import Any, Dict
from uuid import uuid4

import jwt

from app.core.time import utc_now
from app.core.settings import settings


def create_access_token(
        *,
        subject: str,
        expires_delta: timedelta | None = None
) -> str:
    now = utc_now()
    expire = now + (expires_delta or timedelta(minutes=settings.access_token_exp_minutes))

    payload = {
        "sub": subject,
        "type": "access",
        "exp": expire,
        "iat": now
    }

    return jwt.encode(payload, settings.access_token_secret, algorithm="HS256")

def create_refresh_token(
        subject: str,
        expires_delta: timedelta | None = None
) -> tuple[str, str]:
    now = utc_now()
    expire = now + (expires_delta or timedelta(days=settings.refresh_token_exp_days))
    jti = str(uuid4())

    payload = {
        "sub": subject,
        "type": "refresh",
        "exp": expire,
        "iat": now,
        "jti": jti
    }
    token = jwt.encode(payload, settings.refresh_token_secret, algorithm="HS256")

    return token, jti

def decode_refresh_token(token: str) -> dict:
    # verifies signature + exp automatically
    return jwt.decode(token, settings.refresh_token_secret, algorithms=["HS256"])

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.access_token_secret, algorithms=["HS256"])


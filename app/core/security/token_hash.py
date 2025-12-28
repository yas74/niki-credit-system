import hashlib
import hmac

from app.core.settings import settings


def hash_refresh_token(token: str) -> str:
    """
    Hash refresh tokens before storing in DB.
    We use HMAC-SHA256 with REFRESH_TOKEN_SECRET as a pepper (server secret).
    """
    return hmac.new(
        key=settings.refresh_token_secret.encode("utf-8"),
        msg=token.encode("utf-8"),
        digestmod=hashlib.sha256
    ).hexdigest()
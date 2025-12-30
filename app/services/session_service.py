import uuid
from datetime import timedelta, timezone

from beanie import PydanticObjectId

from app.core.security.jwt import create_access_token, create_refresh_token, decode_refresh_token
from app.core.security.token_hash import hash_refresh_token
from app.models.session import Session
from app.models.user import User
from app.core.time import utc_now


class SessionService:
    @staticmethod
    async def refresh_tokens(*, refresh_token: str) -> tuple[str, str]:
        """
        Rotation:
        - validate refresh JWT
        - find session by jti
        - verify token hash matches CURRENT one
        - revoke old session
        - create new tokens + new session
        """
        try:
            payload = decode_refresh_token(refresh_token)
        except Exception:
            raise ValueError("INVALID_REFRESH_TOKEN")
        
        if payload.get("type") != "refresh":
            raise ValueError("INVALID_REFRESH_TOKEN")
        
        user_id = payload.get("sub")
        jti = payload.get("jti")
        if not user_id or not jti:
            raise ValueError("INVALID_REFRESH_TOKEN")
        
        session = await Session.find_one(Session.jti == jti)
        if session is None:
            raise ValueError("INVALID_REFRESH_TOKEN")
        
        if session.revoked_at is not None:
            raise ValueError("REFRESH_TOKEN_REUSED")
        
        now = utc_now()
        expires_at = session.expires_at.replace(tzinfo=timezone.utc)
        if expires_at <= now:
            # session expired server-side
            raise ValueError("REFRESH_TOKEN_EXPIRED")
        
        # Proof of "current"
        if session.refresh_token_hash != hash_refresh_token(refresh_token):
            raise ValueError("INVALID_REFRESH_TOKEN")
        
         # Ensure user still exists & is active
        user = await User.get(session.user_id)
        if user is None or not user.is_active:
            raise ValueError("USER_INACTIVE")
        
        # Revoke old session (rotation)
        session.revoked_at = now
        await session.save()

        # Issue new tokens
        access_token = create_access_token(subject=str(user.id))
        new_refresh_token, new_jti = create_refresh_token(subject=str(user.id))

         # Create new session
        new_session = Session(
            user_id=user.id,
            jti=new_jti,
            refresh_token_hash=hash_refresh_token(new_refresh_token),
            created_at=now,
            expires_at=now+timedelta(days=7),
            user_agent=session.user_agent,
            ip_address=session.ip_address
        )
        await new_session.insert()

        return access_token, new_refresh_token
    
    @staticmethod
    async def logout(*, refresh_token: str) -> None:

        """
        Logout current device:
        - validate refresh token
        - find session by jti
        - revoke it (or delete)
        """
        try:
             payload = decode_refresh_token(refresh_token)
        except Exception:
             raise ValueError("INVALID_REFRESH_TOKEN")
         
        if payload.get("type") != "refresh":
            raise ValueError("INVALID_REFRESH_TOKEN")
        
        jti = payload.get("jti")
        if not not jti:
            raise ValueError("INVALID_REFRESH_TOKEN")
        
        session = await Session.find_one(Session.jti == jti)
        if session is None:
            # treat as already logged out
            return
         
        if session.revoked_at is None:
            session.revoked_at = utc_now()
            await session.save()
        
    @staticmethod
    async def logout_all(*, refresh_token: str) -> None:
        """
        Logout all devices for the user:
        - validate refresh token
        - extract user_id
        - revoke all sessions for that user
        """
        try:
            payload = decode_refresh_token(refresh_token)
        except Exception:
                raise ValueError("INVALID_REFRESH_TOKEN")
            
        if payload.get("type") != "refresh":
            raise ValueError("INVALID_REFRESH_TOKEN")
        
        user_id = PydanticObjectId(payload.get("sub"))
        if not user_id:
            raise ValueError("INVALID_REFRESH_TOKEN")
        
        now = utc_now()

        await Session.find(
            Session.user_id == user_id, 
            Session.revoked_at == None
        ).update(
            {"$set":{"revoked_at": now}}
        )
        
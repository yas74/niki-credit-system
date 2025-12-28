from datetime import timedelta

from pymongo.errors import DuplicateKeyError

from app.models.user import User, UserRole
from app.models.session import Session
from app.core.time import utc_now
from app.core.security.password import hash_password, verify_password
from app.core.security.token_hash import hash_refresh_token
from app.core.security.jwt import create_access_token, create_refresh_token
from app.core.validators.phone import nomalize_iran_phone


class AuthService:
    @staticmethod
    async def signup(
        *,
        username: str,
        password: str,
        phone_number: str,
        first_name: str | None = None,
        last_name: str | None = None,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> tuple[str, str]:
        
        phone_number = nomalize_iran_phone(phone_number)

        user = User(
            username=username,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            password_hash=hash_password(password),
            role=UserRole.STAFF,
            is_active=True           
        )

        try:
            await user.insert()
        except DuplicateKeyError:
            # Could be username or phone_number
            raise ValueError("USER_ALREADY_EXISTS")
        
        access_token = create_access_token(subject=str(user.id))
        refresh_token, jti = create_refresh_token(subject=str(user.id))

        session = Session(
            user_id=user.id,
            refresh_token_hash=hash_refresh_token(refresh_token),
            jti=jti,
            created_at=utc_now(),
            expires_at= utc_now() + timedelta(days=7),
            user_agent=user_agent,
            ip_address=ip_address
        )
        await session.insert()

        return (access_token, refresh_token)
    
    @staticmethod
    async def login(
        *,
        username: str,
        password: str,
        user_agent: str | None = None,
        ip_address: str | None = None
    ) -> tuple[str, str]:
        user = await User.find_one(User.username == username)
        if user is None:
            raise ValueError("INVALID_CREDENTIALS")
        
        if not user.is_active:
            raise ValueError("USER_INACTIVE")
        
        if not verify_password(password, user.password_hash):
            raise ValueError("INVALID_CREDENTIALS")

        access_token = create_access_token(subject=str(user.id))
        refresh_token, jti = create_refresh_token(subject=str(user.id))

        session = Session(
            user_id=user.id,
            refresh_token_hash=hash_refresh_token(refresh_token),
            jti=jti,
            created_at=utc_now(),
            expires_at= utc_now() + timedelta(days=7),
            user_agent=user_agent,
            ip_address=ip_address
        )
        await session.insert()

        return (access_token, refresh_token)

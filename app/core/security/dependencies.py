from beanie import PydanticObjectId
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.user import User, UserRole
from app.core.security.jwt import decode_access_token
from app.core.time import utc_now


bearer_scheme = HTTPBearer(auto_error=False)

def _unauthorized(detail: str = "Not authenticated") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"www-Authenticate": "Bearer"}
    )

async def get_current_user(
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise _unauthorized("Authorization header required")
    
    token = credentials.credentials
    
    try:
        payload = decode_access_token(token)
    except Exception:
        raise _unauthorized("Invalid access token")
    
    if payload.get("type") != "access":
        raise _unauthorized("Invalid access token")
    
    sub = payload.get("sub")
    if not sub:
        raise _unauthorized("Invalid access token")
    
    try:
        user_id = PydanticObjectId(sub)
    except Exception:
        raise _unauthorized("Invalid access token")
    user = await User.get(user_id)
    if user is None:
        raise _unauthorized("Invalid access token")
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User us inactive"
        )   
    
    return user

async def require_superuser(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.SUPERUSER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return user
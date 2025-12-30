from fastapi import APIRouter, status, Request, HTTPException

from app.schemas.auth import TokenPairResponse
from app.services.session_service import SessionService


router = APIRouter(prefix="/auth", tags=["auth"])


def _extract_bearer_tokens(request: Request) -> str:
    auth = request.headers.get("authorization")
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
    
    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")
    
    return parts[1]

@router.post("/refresh", response_model=TokenPairResponse)
async def refresh(request: Request):
    refresh_token = _extract_bearer_tokens(request)

    try:
        access_token, new_refresh_token = await SessionService.refresh_tokens(refresh_token=refresh_token)
    except ValueError as exc:
        msg = str(exc)
        if msg in {"INVALID_REFRESH_TOKEN", "REFRESH_TOKEN_EXPIRED"}:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
        if msg == "REFRESH_TOKEN_REUSED":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token already used")
        
        if msg == "USER_INACTIVE":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User inactive")
        
        raise

    return TokenPairResponse(access_token=access_token, refresh_token=new_refresh_token)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: Request):
    refresh_token = _extract_bearer_tokens(request)

    try:
        await SessionService.logout(refresh_token=refresh_token)
    except ValueError:
        pass
    
    return None

@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(request: Request):
    refresh_token = _extract_bearer_tokens(request)

    try:
        await SessionService.logout_all(refresh_token=refresh_token)
    except ValueError:
        pass
    return None

        
        

    
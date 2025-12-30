from fastapi import APIRouter, status, Request, HTTPException

from app.schemas.auth import SignUpRequest, LoginRequest, TokenPairResponse
from app.services.auth_service import AuthService 


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/signup",
    response_model=TokenPairResponse,
    status_code=status.HTTP_201_CREATED
)
async def signup(payload: SignUpRequest, request: Request):
    try:
        access_token, refresh_token = await AuthService.signup(
            username=payload.username,
            password=payload.password,
            phone_number=payload.phone_number,
            first_name=payload.first_name,
            last_name=payload.last_name,
            user_agent=request.headers.get("user-agent"),
            ip_address=request.client.host if request.client else None
        )

    except ValueError as exc:
        if str(exc) == "INVALID_PHONE_NUMBER":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Iranian phone number"
            )

        if str(exc) == "USER_ALREADY_EXISTS":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or phone number already exists"
            )
        raise
    
    return TokenPairResponse(access_token=access_token, refresh_token=refresh_token)

@router.post("/login", response_model=TokenPairResponse)
async def login(payload: LoginRequest, request: Request):
    try:
        access_token, refresh_token = await AuthService.login(
            username=payload.username,
            password=payload.password,
            user_agent=request.headers.get("user-agent"),
            ip_address=request.client.host if request.client else None
        )
    except ValueError as exc:
        if str(exc) == "INVALID_CREDENTIALS":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        if str(exc) == "USER_INACTIVE":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive"
            )
        raise

    return TokenPairResponse(access_token=access_token, refresh_token=refresh_token)




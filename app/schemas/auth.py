from pydantic import BaseModel, Field


class SignUpRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    phone_number: str = Field(min_length=11, max_length=13)
    password: str = Field(min_length=8, max_length=128)

    first_name: str | None = None
    last_name: str | None = None

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
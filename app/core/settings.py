from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "niki"
    app_env: str = "local"
    debug: bool = True

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "niki"

    access_token_secret: str
    refresh_token_secret: str

    class Config:
        env_file = ".env"


settings = Settings()
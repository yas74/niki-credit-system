from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "niki"
    app_env: str = "local"
    debug: bool = True

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "niki"

    class Config:
        env_file = ".env"


settings = Settings()
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()

assert settings.SECRET_KEY, "SECRET_KEY is not set"

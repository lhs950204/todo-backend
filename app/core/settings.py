from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DB_URI: str = ""

    MEDIA_URL: str = "media"
    MEDIA_ROOT: str = "../media"


settings = Settings()

assert settings.SECRET_KEY, "SECRET_KEY is not set"
assert settings.DB_URI, "DB_URI is not set"

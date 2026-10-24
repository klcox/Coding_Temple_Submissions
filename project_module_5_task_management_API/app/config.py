from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Task Management API"
    debug: bool = True  # Set to False for production

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ADMIN_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
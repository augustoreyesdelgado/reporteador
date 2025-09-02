from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "development"
    CORS_ORIGINS: str = ""

    class Config:
        env_file = ".env.dev"

settings = Settings()

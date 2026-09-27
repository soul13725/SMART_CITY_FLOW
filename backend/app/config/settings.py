from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Smart City Big Data Traffic Analytics Platform"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    BACKEND_HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:5173"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

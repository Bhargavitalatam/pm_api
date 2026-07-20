from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://pm_user:pm_password@db:5432/pm_database"
    SECRET_KEY: str = "super-secret-key-for-jwt-signing-2026"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()

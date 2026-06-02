import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding="utf-8",
                                      extra="ignore")

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24
    jwt_refresh_expire_days: int = 30

    @property
    def database_url(self) -> str:
        # Получаем переменную из окружения
        pg_conn = os.getenv("POSTGRES_CONNECTION_STRING")
        
        if pg_conn:
            # Если строка начинается с postgres:// или postgresql://
            if pg_conn.startswith("postgres://"):
                pg_conn = pg_conn.replace("postgres://", "postgresql+asyncpg://", 1)
            elif pg_conn.startswith("postgresql://") and "+asyncpg" not in pg_conn:
                pg_conn = pg_conn.replace("postgresql://", "postgresql+asyncpg://", 1)
            return pg_conn
        
        # Fallback для локальной разработки
        return "postgresql+asyncpg://postgres:postgres@localhost:5433/auth_db"

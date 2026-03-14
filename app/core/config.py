from functools import lru_cache
from typing import Optional
from urllib.parse import quote_plus, urlencode
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    INSTANCE_CONNECTION_NAME: Optional[str] = None
    DB_SOCKET_DIR: str = "/cloudsql"
    DB_HOST: Optional[str] = None
    DB_PORT: int = 5432
    DB_NAME: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_SSLMODE: str = "prefer"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    API_V1_STR: str = "/api/v1"
    SEED_ADMIN_ON_STARTUP: bool = False
    ADMIN_SEED_NOMBRE: str = "Admin"
    ADMIN_SEED_APELLIDOS: str = "Flowdex"
    ADMIN_SEED_EMAIL: str = "admin@flowdex.es"
    ADMIN_SEED_PASSWORD: Optional[str] = None

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL

        required = {
            "DB_NAME": self.DB_NAME,
            "DB_USER": self.DB_USER,
            "DB_PASSWORD": self.DB_PASSWORD,
        }
        missing = [key for key, value in required.items() if not value]
        if missing:
            missing_fields = ", ".join(missing)
            raise ValueError(
                f"Database settings incomplete. Missing: {missing_fields}"
            )

        user = quote_plus(self.DB_USER or "")
        password = quote_plus(self.DB_PASSWORD or "")

        if self.INSTANCE_CONNECTION_NAME:
            socket_host = f"{self.DB_SOCKET_DIR.rstrip('/')}/{self.INSTANCE_CONNECTION_NAME}"
            query = urlencode({"host": socket_host})
            return f"postgresql+asyncpg://{user}:{password}@/{self.DB_NAME}?{query}"

        if not self.DB_HOST:
            raise ValueError(
                "Database settings incomplete. Missing: DB_HOST or INSTANCE_CONNECTION_NAME"
            )

        query = urlencode({"sslmode": self.DB_SSLMODE})
        return (
            f"postgresql+asyncpg://{user}:{password}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?{query}"
        )


@lru_cache()
def get_settings() -> Settings:
    return Settings()

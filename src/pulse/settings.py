"""Application settings for Pulse"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[".env.local", ".env"],
        env_prefix="PULSE_",
        extra="ignore",  # Load .env.local first, then .env
    )

    # Core application settings
    app_name: str = "pulse"
    env: str = "dev"  # dev | staging | prod
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8200

    # Database
    database_url: str = "sqlite+aiosqlite:///./pulse.db"

    # Authentication
    secret_key: str = "change-this-secret-key-in-production"
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"

    # CORS settings
    cors_allow_origins: list[str] = ["http://localhost:3200"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    # Logging
    log_level: str = "INFO"  # DEBUG|INFO|WARNING|ERROR
    json_logs: bool = True


settings = Settings()

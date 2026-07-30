from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="HEIMDALL_",
        env_file=".env",
        extra="ignore",
    )

    app_name: str = "Phitopolis Heimdall CMS"
    debug: bool = False
    database_url: str = "sqlite+aiosqlite:///./phitopolis_heimdall.db"
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:80",
    ]
    seed_on_startup: bool = True
    admin_secret_key: str = "heimdall-secret-key-change-in-production"


settings = Settings()

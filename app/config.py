from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Document Q&A Assistant"
    max_file_size_mb: int = 10
    top_k_results: int = 3
    upload_dir: Path = Path("data/uploads")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
settings.upload_dir.mkdir(parents=True, exist_ok=True)


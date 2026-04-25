from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FastAPI Error Handling Lab"
    log_level: str = "INFO"
    log_file: str = "app.log"

    model_config = SettingsConfigDict(env_file=".env")
settings = Settings()

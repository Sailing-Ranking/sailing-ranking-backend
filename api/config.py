from pydantic import BaseSettings


class Settings(BaseSettings):
    """App settings."""

    # app settings
    fastapi_app: str
    fastapi_port: int


settings = Settings()

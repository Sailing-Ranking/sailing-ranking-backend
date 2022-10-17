from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings
from api.database import Base, get_db

app = FastAPI()


def create_app():
    """Intialize the application."""

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", status_code=status.HTTP_200_OK)
    def read_root() -> dict[str, str]:
        return {"message": "Hello World!"}

    @app.get("/health-check", status_code=status.HTTP_200_OK)
    def health_check() -> dict[str, bool]:
        return {"healthy": True}

    return app

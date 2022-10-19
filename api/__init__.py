from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from api import config, database, models, routes, schemas
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

    from api.routes import competition

    app.include_router(competition.router)

    from api.routes import competitor

    app.include_router(competitor.router)

    from api.routes import race

    app.include_router(race.router)

    @app.get("/health-check", status_code=status.HTTP_200_OK)
    def health_check() -> dict[str, bool]:
        return {"healthy": True}

    return app

import logging

import tensorflow as tf
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from . import config, database, models, routes, schemas
from .config import settings
from .database import Base, get_db

model = tf.keras.models.load_model("api/ai/cnn_model")

app = FastAPI()
logger = logging.getLogger("uvicorn.error")


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

    from api.routes import position

    app.include_router(position.router)

    from api.routes import country

    app.include_router(country.router)

    from api.routes import club

    app.include_router(club.router)

    @app.get("/health-check", status_code=status.HTTP_200_OK)
    def health_check() -> dict[str, bool]:
        return {"healthy": True}

    return app

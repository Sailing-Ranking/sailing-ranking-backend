import datetime
import uuid

import pytz
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

from api.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    """Represent a base sqlalchemy model with common fields."""

    __name__: str

    # all models have an unique id
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # all data models have a creation date
    created_at = sa.Column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.now(tz=pytz.utc),
    )

    # all data models have an update date
    created_at = sa.Column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.now(tz=pytz.utc),
        onupdate=datetime.datetime.now(tz=pytz.utc),
    )

    # generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


def get_db():
    """Rerunt a database connection handler."""

    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

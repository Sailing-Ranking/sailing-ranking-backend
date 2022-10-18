from enum import Enum

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from api.database import Base


class Race(Base):
    """Representing a race as a database table."""

    # the race number
    race_nr = sa.Column(sa.BigInteger, nullable=False, autoincrement=True)
    # the finishing positions in the race
    postitions = relationship(
        "Position",
        back_populates="race",
        lazy="dynamic",
    )

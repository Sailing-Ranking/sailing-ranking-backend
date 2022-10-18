import sqlalchemy as sa
from sqlalchemy.orm import relationship

from api.database import Base


class Race(Base):
    """Representing a race as a database table."""

    # the race number
    race_nr = sa.Column(sa.BigInteger, nullable=False, index=True)
    # the finishing positions in the race
    postitions = relationship(
        "Position",
        back_populates="race",
        lazy="dynamic",
    )

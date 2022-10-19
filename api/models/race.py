import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from api.database import Base


class Race(Base):
    """Representing a race as a database table."""

    # the race number
    race_nr = sa.Column(sa.BigInteger, nullable=False, index=True)
    # the competition id for the race
    competition_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("competition.id"))
    # the competition for the race
    competition = relationship("Competition", back_populates="races")
    # the finishing positions in the race
    positions = relationship(
        "Position",
        back_populates="race",
        lazy="dynamic",
    )

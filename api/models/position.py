import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from api.database import Base


class Position(Base):
    """Representing a finishig postion of a competitor and related points as a database table."""

    # the points for the finishing position
    points = sa.Column(sa.BigInteger, nullable=False)
    # the race id for the finishing position
    race_id = sa.Column(UUID, sa.ForeignKey("race.id"))
    # the race object for the finishin position
    race = relationship("Race", back_populates="positions")
    # the competitor id for the finishing position
    competitor_id = sa.Column(UUID, sa.ForeignKey("competitor.id"))
    # the competitor object for the finishing position
    competitor = relationship("Competitor", back_populates="positions")

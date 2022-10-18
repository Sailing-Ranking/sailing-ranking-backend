from enum import Enum

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from api.database import Base


class Country(str, Enum):
    """Representing a country as an enum."""

    GER = "GER"  # Germany
    GRE = "GRE"  # Greece
    ITA = "ITA"  # Italy
    NL = "NL"  # Netherlands

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.value


class Club(str, Enum):
    """Representing a sailing club as an enum."""

    NOC = "NOC"
    ANOG = "ANOG"
    SEANATK = "SEANATK"

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.value


class Competitor(Base):
    """Representing a competitor as a database table."""

    # competitor first name
    first_name = sa.Column(sa.VARCHAR(length=128), nullable=False)
    # competitor last name
    last_name = sa.Column(sa.VARCHAR(length=256), nullable=False)
    # competitor country of national team
    country = sa.Column(sa.Enum(Country), nullable=False)
    # competitor sail number
    sail_nr = sa.Column(sa.BigInteger, nullable=False, index=True)
    # competitor total points in competition
    total_points = sa.Column(
        sa.BigInteger, nullable=False, default=0, server_default="0"
    )
    # competitor net points in competition
    net_points = sa.Column(sa.BigInteger, nullable=False, default=0, server_default="0")
    # competitor club
    club = sa.Column(sa.Enum(Club), nullable=False, index=True)
    # the competition id in which the competitor takes part
    competition_id = sa.Column(UUID, sa.ForeignKey("competition.id"))
    # the competition object in which the competitor takes part
    competition = relationship("Competition", back_populates="competitors")
    # the competitor's position finishes
    positions = relationship(
        "Position",
        back_populates="competitor",
        lazy="dynamic",
    )

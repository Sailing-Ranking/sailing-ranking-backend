from enum import Enum

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from api.database import Base


class Boat(str, Enum):
    """Representing a boat type as an enum."""

    ILCA_4 = "ILCA_4"
    ILCA_6 = "ILCA_6"
    ILCA_7 = "ILCA_7"

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.value


class Competition(Base):
    """Representing a competition as a database table."""

    # title of a competition
    title = sa.Column(sa.VARCHAR(length=128), nullable=False)
    # the type of boat of a competition
    boat = sa.Column(sa.Enum(Boat), nullable=False)
    # the start date of a competition
    start_date = sa.Column(sa.Date, nullable=False, index=True)
    # the end date of a competition
    end_date = sa.Column(sa.Date, nullable=False, index=True)
    # the races executed during the competition
    races = relationship(
        "Race",
        back_populates="competition",
        lazy="dynamic",
    )
    # the associated competitors of a competition
    competitors = relationship(
        "Competitor",
        back_populates="competition",
        lazy="dynamic",
    )

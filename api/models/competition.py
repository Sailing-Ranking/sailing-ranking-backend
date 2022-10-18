import sqlalchemy as sa
from sqlalchemy.orm import relationship

from api.database import Base


class Competition(Base):
    """Representing a competition as a database table."""

    # title of a competition
    title = sa.Column(sa.VARCHAR(length=128), nullable=False)
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

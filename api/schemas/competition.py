import datetime
from typing import List

from pydantic import UUID4, BaseModel, constr

from api.models import Boat
from api.schemas.competitor import Club, Country
from api.schemas.position import PositionOut


class CompetitionBase(BaseModel):
    """Representing a sailing competition as schema."""

    title: constr(strip_whitespace=True, min_length=1, max_length=128)
    boat: Boat
    start_date: datetime.date
    end_date: datetime.date

    class Config:
        orm_mode = True
        use_enum_values = True


class CompetitionOut(CompetitionBase):
    """Representing a sailing competition that is returned to a user as schema."""

    id: UUID4

    created_at: datetime.datetime
    updated_at: datetime.datetime


class CompetitionCreate(CompetitionBase):
    """Representing a sailing competition to be created as schema."""

    pass


class CompetitionUpdate(CompetitionBase):
    """Representing a sailing competition to be updated as schema."""

    pass


class Result(BaseModel):
    """Representing a sailing competition results as a schema."""

    first_name: str
    last_name: str
    country: Country
    club: Club
    sail_nr: int
    total_points: int

    positions: List[PositionOut]

    class Config:
        orm_mode = True
        use_enum_values = True

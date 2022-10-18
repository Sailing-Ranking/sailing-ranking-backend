import datetime

from pydantic import UUID4, BaseModel, constr

from api.models import Boat


class CompetitionBase(BaseModel):
    """Representing a sailing competition as schema."""

    title: constr(strip_whitespace=True, min_length=5, max_length=128)
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

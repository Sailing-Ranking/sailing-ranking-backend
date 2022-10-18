import datetime

from pydantic import UUID4, BaseModel, constr

from api.models import Club, Country


class CompetitorBase(BaseModel):
    """Representing a sailing competitor as schema."""

    first_name: constr(strip_whitespace=True, min_length=5, max_length=128)
    last_name: constr(strip_whitespace=True, min_length=5, max_length=256)
    country: Country
    sail_nr: int
    total_points: int = 0
    net_points: int = 0
    club: Club
    competition_id: UUID4

    class Config:
        orm_mode = True
        use_enum_values = True


class CompetitorOut(CompetitorBase):
    """Representing a sailing competitor that is returned to a user as schema."""

    id: UUID4

    created_at: datetime.datetime
    updated_at: datetime.datetime


class CompetitorCreate(CompetitorBase):
    """Representing a sailing competitor to be created as schema."""

    pass


class CompetitorUpdated(CompetitorBase):
    """Representing a sailing competition to be updated as schema."""

    pass

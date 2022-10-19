import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class RaceBase(BaseModel):
    """Representing a sailing competition race as schema."""

    race_nr: Optional[int]
    competition_id: UUID4

    class Config:
        orm_mode = True


class RaceOut(RaceBase):
    """Representing a sailing competition race that is returned to a user as schema."""

    id: UUID4

    created_at: datetime.datetime
    updated_at: datetime.datetime


class RaceCreate(RaceBase):
    """Representing a sailing competition race to be created as schema."""

    pass


class RaceUpdate(RaceBase):
    """Representing a sailing competition race to be updated as schema."""

    pass

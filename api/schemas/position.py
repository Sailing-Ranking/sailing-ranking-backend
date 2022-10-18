import datetime

from pydantic import UUID4, BaseModel


class PositionBase(BaseModel):
    """Representing a finishing position as schema."""

    points: int
    race_id: UUID4
    sail_nr: int

    class Config:
        orm_mode = True


class PositionOut(PositionBase):
    """Representing a finishing position that is returned to a user as schema."""

    id: UUID4

    created_at: datetime.datetime
    updated_at: datetime.datetime


class PositionCreate(PositionBase):
    """Representing a finishing position to be created as schema."""

    pass


class PositionUpdate(PositionBase):
    """Representing a finishing position to be updated as schema."""

    pass

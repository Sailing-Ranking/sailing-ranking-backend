import datetime
import json

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

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class PositionUpdate(PositionBase):
    """Representing a finishing position to be updated as schema."""

    pass

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from api import get_db
from api.models import Competition, Race
from api.schemas import RaceCreate, RaceOut, RaceUpdate, PositionOut

router = APIRouter(prefix="/races", tags=["Races"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[RaceOut])
async def read(db: Session = Depends(get_db)):
    """Handle returning all races to the user."""

    races: Race = db.query(Race).all()
    return races


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=RaceOut)
async def get_by_id(id: UUID4, db: Session = Depends(get_db)):
    """Handle returning one race by id to the user."""
    race: Race = db.query(Race).get(id)

    if not race:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="race not found"
        )

    return race


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RaceOut)
async def create(create_race: RaceCreate, db: Session = Depends(get_db)):
    """Handle creating a race."""
    new_race: Race = Race(**create_race.dict())

    if not db.query(Competition).get(new_race.competition_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competition not found"
        )

    new_race.race_nr = (
        db.query(Race).filter(Race.competition_id == new_race.competition_id).count()
        + 1
    )

    db.add(new_race)
    db.commit()

    print(new_race.__dict__)

    return new_race


@router.put("/{id}", status_code=status.HTTP_501_NOT_IMPLEMENTED, response_model=Any)
async def update(id: UUID4, update_race: RaceUpdate, db: Session = Depends(get_db)):
    """Handle updating a race."""
    # race_query = db.query(Race).filter(Race.id == id)
    # race: Race = race_query.first()

    # if not race:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="race not found")

    # race_query.update(update_race.dict())

    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID4, db: Session = Depends(get_db)):
    """Handle deleting a race."""
    race: Race = db.query(Race).get(id)

    if not race:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="race not found"
        )

    db.delete(race)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{id}/positions", status_code=status.HTTP_200_OK, response_model=List[PositionOut])
async def get_by_id(id: UUID4, db: Session = Depends(get_db)):
    """Handle returning one race by id to the user."""
    race: Race = db.query(Race).get(id)

    if not race:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="race not found"
        )

    return race.positions.all()

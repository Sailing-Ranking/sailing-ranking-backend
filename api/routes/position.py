from typing import Any, List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from api import get_db
from api.models import Competitor, Position, Race
from api.schemas import PositionCreate, PositionOut, PositionUpdate
from api.services import update_ranking

router = APIRouter(prefix="/positions", tags=["Positions"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PositionOut])
async def read(db: Session = Depends(get_db)):
    """Handle returning all positions to the user."""
    positions = db.query(Position).all()
    return positions


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PositionOut)
async def get_by_id(id: UUID4, db: Session = Depends(get_db)):
    """Handle returning one position by id to the user."""
    position = db.query(Position).get(id)

    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="position not found"
        )

    return position


@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_model=PositionOut)
async def create(
    create_position: PositionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Handle creating a position."""

    if not db.query(Race).get(create_position.race_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="race does not exist"
        )

    if (
        not db.query(Competitor)
        .filter(Competitor.sail_nr == create_position.sail_nr)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"competitor with sail number {create_position.sail_nr} does not exist",
        )

    if (
        db.query(Position)
        .filter(
            Position.race_id == create_position.race_id,
            Position.sail_nr == create_position.sail_nr,
        )
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"competitor with sail number {create_position.sail_nr} has already finnished",
        )

    # set up background task to calculate new points and positions
    background_tasks.add_task(update_ranking, create_position, db)

    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.put("/{id}", status_code=status.HTTP_501_NOT_IMPLEMENTED, response_model=Any)
async def update(
    id: UUID4, update_position: PositionUpdate, db: Session = Depends(get_db)
):
    """Handle updating a position."""
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID4, db: Session = Depends(get_db)):
    """Handle deleting a position."""
    position = db.query(Position).get(id)

    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="position not found"
        )

    db.delete(position)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

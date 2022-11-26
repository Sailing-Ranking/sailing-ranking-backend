from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from api import get_db
from api.models import Competitor
from api.schemas.competitor import CompetitorCreate, CompetitorOut, CompetitorUpdated
from api.schemas.position import PositionOut

router = APIRouter(prefix="/competitors", tags=["Competitors"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CompetitorOut])
async def read(db: Session = Depends(get_db)):
    """Handle returning all competitors to the user."""
    competitors: List[Competitor] = db.query(Competitor).all()
    return competitors


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CompetitorOut)
async def get_by_id(id: UUID4, db: Session = Depends(get_db)):
    """Handle returning one competitor to the user by id."""
    competitor: Competitor = db.query(Competitor).get(id)

    if not competitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competitor not found"
        )

    return competitor


@router.get(
    "/{id}/positions", status_code=status.HTTP_200_OK, response_model=List[PositionOut]
)
async def get_competitor_positions(id: UUID4, db: Session = Depends(get_db)):
    """Handle returning all competitor positions to the user."""
    competitor: Competitor = db.query(Competitor).get(id)

    if not competitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competitor not found"
        )

    return competitor.positions.all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CompetitorOut)
async def create(create_competitor: CompetitorCreate, db: Session = Depends(get_db)):
    """Handle creating a competitor."""

    if (
        db.query(Competitor)
        .filter(Competitor.sail_nr == create_competitor.sail_nr)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"competitor with sail number {create_competitor.sail_nr} alreay exists",
        )

    new_competitor: Competitor = Competitor(**create_competitor.dict())
    db.add(new_competitor)
    db.commit()

    return new_competitor


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=CompetitorOut)
async def update(
    id: UUID4, update_competitor: CompetitorUpdated, db: Session = Depends(get_db)
):
    """Handle updating a competitor."""
    competitor_query = db.query(Competitor).filter(Competitor.id == id)
    competitor: Competitor = competitor_query.first()

    if not competitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competitor not found"
        )

    competitor_query.update(update_competitor.dict())
    db.commit()

    return competitor_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID4, db: Session = Depends(get_db)):
    """Handle deleting a competitor."""
    competitor: Competitor = db.query(Competitor).get(id)

    if not competitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competitor not found"
        )

    db.delete(competitor)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

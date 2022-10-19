from typing import List

import pandas as pd
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Response,
    UploadFile,
    status,
)
from pydantic import UUID4
from sqlalchemy.orm import Session

from api import get_db
from api.models import Boat, Club, Competition, Competitor, Country
from api.schemas import (
    CompetitionCreate,
    CompetitionOut,
    CompetitionUpdate,
    CompetitorCreate,
    CompetitorOut,
)

router = APIRouter(prefix="/competitions", tags=["Competitions"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CompetitionOut])
async def read(db: Session = Depends(get_db)):
    """Handle returning all competiions to the user."""
    competitions = db.query(Competition).all()
    return competitions


@router.get("/boats", status_code=status.HTTP_200_OK, response_model=List[Boat])
def get_boat_types():
    return list(Boat)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CompetitionOut)
async def get_by_id(id: UUID4, db: Session = Depends(get_db)):
    """Handle returning a competition by id to the user."""
    competition = db.query(Competition).get(id)

    if not competition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competition not found"
        )

    return competition


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CompetitionOut)
async def create(create_competition: CompetitionCreate, db: Session = Depends(get_db)):
    """Handle creating a competition."""
    new_competition = Competition(**create_competition.dict())
    db.add(new_competition)
    db.commit()

    return new_competition


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=CompetitionOut)
async def update(
    id: UUID4, update_competition: CompetitionUpdate, db: Session = Depends(get_db)
):
    """Handle updating a competition."""
    competition_query = db.query(Competition).filter(Competition.id == id)
    competition: Competition = competition_query.first()

    if not competition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competition not found"
        )

    competition_query.update(update_competition.dict())
    db.commit()

    return competition_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID4, db: Session = Depends(get_db)):
    """Handle deleting a competition."""
    competition = db.query(Competition).get(id)

    if not competition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competition not found"
        )

    db.delete(competition)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{id}/csv", status_code=status.HTTP_201_CREATED, response_model=List[CompetitorOut]
)
async def add_competitors_by_csv(
    id: UUID4, competitors: UploadFile = File(...), db: Session = Depends(get_db)
):

    competition = db.query(Competition).get(id)

    if not ("csv" in competitors.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="file needs to be a csv file",
        )

    if not competition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competition not found"
        )

    df = pd.read_csv(competitors.file)
    df = df.reset_index()

    new_competitors = list()
    for _, row in df.iterrows():

        if db.query(Competitor).filter(Competitor.sail_nr == int(row.sail_nr)).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"competitor with sail number {row.sail_nr} alreay exists",
            )

        create_competitor = CompetitorCreate(
            first_name=row.first_name,
            last_name=row.last_name,
            country=Country(row.country),
            sail_nr=row.sail_nr,
            club=Club(row.club),
            competition_id=id,
        )
        new_competitors.append(Competitor(**create_competitor.dict()))

    db.add_all(new_competitors)
    db.commit()

    return new_competitors


@router.post(
    "/{id}/xlsx",
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    response_model=List[CompetitorOut],
)
async def add_competitors_by_xlsx(
    id: UUID4, competitors: UploadFile = File(...), db: Session = Depends(get_db)
):
    competition = db.query(Competition).get(id)

    if not ("excel" in competitors.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="file needs to be a excel file",
        )

    if not competition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competition not found"
        )

    df = pd.read_excel(competitors.file)
    df = df.reset_index()

    new_competitors = list()
    for _, row in df.iterrows():

        if db.query(Competitor).filter(Competitor.sail_nr == int(row.sail_nr)).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"competitor with sail number {row.sail_rn} alreay exists",
            )

        create_competitor = CompetitorCreate(
            first_name=row.first_name,
            last_name=row.last_name,
            country=Country(row.country),
            sail_nr=row.sail_nr,
            club=Club(row.club),
            competition_id=id,
        )
        new_competitors.append(Competitor(**create_competitor.dict()))

    db.add_all(new_competitors)
    db.commit()

    return new_competitors


@router.post(
    "/{id}/json",
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    response_model=List[CompetitorOut],
)
async def add_competitors_by_json(
    id: UUID4, competitors: UploadFile = File(...), db: Session = Depends(get_db)
):
    competition = db.query(Competition).get(id)

    if not ("json" in competitors.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="file needs to be a json file",
        )

    if not competition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competition not found"
        )

    df = pd.read_json(competitors.file)
    df = df.reset_index()

    new_competitors = list()
    for _, row in df.iterrows():

        if db.query(Competitor).filter(Competitor.sail_nr == int(row.sail_nr)).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"competitor with sail number {row.sail_rn} alreay exists",
            )

        create_competitor = CompetitorCreate(
            first_name=row.first_name,
            last_name=row.last_name,
            country=Country(row.country),
            sail_nr=row.sail_nr,
            club=Club(row.club),
            competition_id=id,
        )
        new_competitors.append(Competitor(**create_competitor.dict()))

    db.add_all(new_competitors)
    db.commit()

    return new_competitors

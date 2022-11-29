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
from api.schemas.competition import CompetitionCreate, CompetitionOut, CompetitionUpdate
from api.schemas.competitor import CompetitorCreate, CompetitorOut
from api.schemas.race import RaceOut

router = APIRouter(prefix="/competitions", tags=["Competitions"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CompetitionOut])
async def read(db: Session = Depends(get_db)):
    """Handle returning all competitions to the user."""
    competitions: List[Competition] = (
        db.query(Competition).order_by(Competition.start_date.desc()).all()
    )
    return competitions


@router.get("/boats", status_code=status.HTTP_200_OK, response_model=List[Boat])
async def get_boat_types():
    """Handle returning all cometition boat types to the user."""
    return list(Boat)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CompetitionOut)
async def get_by_id(id: UUID4, db: Session = Depends(get_db)):
    """Handle returning one competition by id to the user."""
    competition: Competition = db.query(Competition).get(id)

    if not competition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competition not found"
        )

    return competition


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CompetitionOut)
async def create(create_competition: CompetitionCreate, db: Session = Depends(get_db)):
    """Handle creating a competition."""
    new_competition: Competition = Competition(**create_competition.dict())
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
    competition: Competition = db.query(Competition).get(id)

    if not competition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competition not found"
        )

    db.delete(competition)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{id}/competitors",
    status_code=status.HTTP_200_OK,
    response_model=List[CompetitorOut],
)
async def get_competition_competitors(id: UUID4, db: Session = Depends(get_db)):
    """Handle returning all competition competitors to the user."""
    competition: Competition = db.query(Competition).get(id)

    if not competition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competition not found"
        )

    return competition.competitors.all()


@router.get("/{id}/races", status_code=status.HTTP_200_OK, response_model=List[RaceOut])
async def get_competiton_races(id: UUID4, db: Session = Depends(get_db)):
    """Handle returning all competition races to the user."""
    competition: Competition = db.query(Competition).get(id)

    if not competition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competition not found"
        )

    return competition.races.all()


@router.get(
    "/{id}/results", status_code=status.HTTP_200_OK, response_model=List[CompetitorOut]
)
async def get_competition_results(id: UUID4, db: Session = Depends(get_db)):
    """Handle returning the results of the competition to the user."""

    competition: Competition = db.query(Competition).get(id)

    if not competition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="competition not found"
        )

    return competition.competitors.order_by(Competitor.total_points).all()


@router.post(
    "/{id}/csv", status_code=status.HTTP_201_CREATED, response_model=List[CompetitorOut]
)
async def add_competitors_by_csv(
    id: UUID4, competitors: UploadFile = File(...), db: Session = Depends(get_db)
):

    competition: Competition = db.query(Competition).get(id)

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
    competition: Competition = db.query(Competition).get(id)

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
    "/{id}/json",
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    response_model=List[CompetitorOut],
)
async def add_competitors_by_json(
    id: UUID4, competitors: UploadFile = File(...), db: Session = Depends(get_db)
):
    competition: Competition = db.query(Competition).get(id)

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

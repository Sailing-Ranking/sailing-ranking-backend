import difflib
from typing import Any, List

import cv2
import numpy as np
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    Response,
    UploadFile,
    status,
)
from pydantic import UUID4
from sqlalchemy.orm import Session

from api import get_db, model
from api.models import Competitor, Position, Race
from api.schemas import PositionOut, PositionUpdate
from api.services import (
    combine_digits_to_full_number,
    get_countours,
    seperate_number_into_digits,
    sort_contours,
    update_ranking,
)

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
    race_id: UUID4,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Handle creating a position."""
    if file.content_type not in ["image/jpg", "image/jpeg"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="the file must be a jpg or jpeg",
        )

    if not db.query(Race).get(race_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="race does not exist"
        )

    # set up background task to calculate new points and positions
    background_tasks.add_task(update_ranking, race_id, file, db)

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


@router.post("/recognize", status_code=status.HTTP_200_OK)
async def recognize(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if file.content_type not in ["image/jpg", "image/jpeg"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="the file must be a jpg or jpeg",
        )

    contents = file.file.read()
    nparr = np.array(bytearray(contents), dtype="uint8")
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    contours, image = get_countours(image=image)

    # put in function to get sorted countours
    digit_boxes = sort_contours(contours)

    # put in function to get single digits to predict
    digits = seperate_number_into_digits(image, digit_boxes)

    # model predicts
    predictions = model.predict(digits)

    # pu in function to get full number prediction
    predicted_number = combine_digits_to_full_number(predictions)
    possibilities = [
        str(competitor.sail_nr)
        for competitor in db.query(Competitor)
        .filter(Competitor.competition_id == "b4761f7d-cdc1-4d25-94bf-1f777837b4ce")
        .all()
    ]
    closest_numbers = difflib.get_close_matches(predicted_number, possibilities)

    return {"closest_match": closest_numbers, "prediction": predicted_number}

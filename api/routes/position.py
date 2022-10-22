from typing import Any, List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response, status, UploadFile, File, Body
from pydantic import UUID4
from sqlalchemy.orm import Session

from api import get_db, model
from api.models import Competitor, Position, Race, Competition
from api.schemas import PositionCreate, PositionOut, PositionUpdate
from api.services import update_ranking

import cv2
import numpy as np
import difflib


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
    background_tasks: BackgroundTasks,
    create_position: PositionCreate = Body(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Handle creating a position."""
    if not file.content_type in ["image/jpg", "image/jpeg"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="the file must be a jpg or jpeg"
        )

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


@router.post("/recognize", status_code=status.HTTP_200_OK)
async def recognize(file: UploadFile = File(...), db: Session = Depends(get_db),):
    if not file.content_type in ["image/jpg", "image/jpeg"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="the file must be a jpg or jpeg"
        )

    contents = file.file.read()
    nparr = np.fromstring(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    image = cv2.resize(image, (400, 400))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.adaptiveThreshold(image, 255, 1, 1, 11, 2)
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    digit_boxes = []
    padding = 10
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x-padding, y-padding), (x + w + padding, y + h + padding), (0, 0, 255), 1)
        digit_boxes.append((x-padding, y-padding, w+padding, h+padding))

    digit_boxes.sort(key=lambda r: r[0])

    digits = []
    for contour in digit_boxes:
        _image = image[contour[1]:contour[1]+contour[3],contour[0]:contour[0]+contour[2]]
        _image = cv2.resize(_image, (28, 28), interpolation=cv2.INTER_AREA)
        digits.append(_image)

    digits = np.array(digits)

    predictions = model.predict(digits)

    predicted_number = ""
    for pred in predictions:
        digit = str(np.argmax(pred))
        predicted_number += digit

    possibilities = [str(competitor.sail_nr) for competitor in db.query(Competitor.sail_nr).filter(Competition.id == "b4761f7d-cdc1-4d25-94bf-1f777837b4ce").all()]

    closest_numbers = difflib.get_close_matches(predicted_number, possibilities)
    return closest_numbers

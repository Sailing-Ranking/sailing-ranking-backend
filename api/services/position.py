import difflib
from typing import List

import cv2
import numpy as np
from fastapi import UploadFile
from pydantic import UUID4
from sqlalchemy import desc
from sqlalchemy.orm import Session

from api import logger, model
from api.models import Competition, Competitor, Position, Race


def get_countours(image):
    image = cv2.resize(image, (400, 400))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.adaptiveThreshold(image, 255, 1, 1, 11, 2)
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return contours, image


def sort_contours(contours, padding=10):
    digit_boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        digit_boxes.append((x - padding, y - padding, w + padding, h + padding))

    digit_boxes.sort(key=lambda r: r[0])

    return digit_boxes


def seperate_number_into_digits(image, digit_boxes):
    digits = []
    for contour in digit_boxes:
        _image = image[
            contour[1] : contour[1] + contour[3], contour[0] : contour[0] + contour[2]
        ]
        _image = cv2.resize(_image, (28, 28), interpolation=cv2.INTER_AREA)
        digits.append(_image)

    return np.array(digits)


def combine_digits_to_full_number(predictions):
    predicted_number = ""
    for pred in predictions:
        digit = str(np.argmax(pred))
        predicted_number += digit

    return predicted_number


def update_ranking(race_id: UUID4, file: UploadFile, db: Session):
    """Handle calculating the total and net points."""
    race: Race = db.query(Race).get(race_id)

    # convert bytes to opencv image object
    contents = file.file.read()
    nparr = np.fromstring(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # define the contours of image
    contours, image = get_countours(image=image)
    # put contours in right order
    digit_boxes = sort_contours(contours)
    # define array of the single digits of number
    digits = seperate_number_into_digits(image, digit_boxes)
    # generate a prediction on all digits
    predictions = model.predict(digits)
    # combine predicted digits into whole number
    predicted_number = combine_digits_to_full_number(predictions)
    # get all possibilities of sail numbers for this competition
    possibilities = [
        str(competitor.sail_nr)
        for competitor in db.query(Competitor.sail_nr)
        .filter(Competition.id == race.competition_id)
        .all()
    ]

    logger.info(f"predicted number: {predicted_number}")

    # get the clossest match
    if predicted_number not in possibilities:
        matches = difflib.get_close_matches(predicted_number, possibilities)
        if matches:
            predicted_number = difflib.get_close_matches(
                predicted_number, possibilities
            )[0]

    logger.info(f"clossest number: {predicted_number}")

    new_position = Position(
        race_id=race_id,
        sail_nr=predicted_number,
    )

    if not (
        db.query(Position)
        .filter(
            Position.race_id == new_position.race_id,
            Position.sail_nr == new_position.sail_nr,
        )
        .first()
    ):
        new_points = (
            db.query(Position).filter(Position.race_id == new_position.race_id).count()
            + 1
        )

        new_position.points = new_points

        competitor: Competitor = (
            db.query(Competitor)
            .filter(Competitor.sail_nr == new_position.sail_nr)
            .first()
        )
        competitor.total_points += new_points

        db.add(new_position)

        subtract_total = competitor.total_points - competitor.net_points
        race_count = db.query(Race).count()
        if (race_count > 0) and (race_count % 4 == 0):
            subtract_count = int(race_count / 4)

            all_competitor_positions: List[Position] = competitor.positions.order_by(
                desc(Position.points)
            ).all()
            subtract_total = 0
            for i in range(subtract_count):
                subtract_total += all_competitor_positions[i].points

        competitor.net_points = competitor.total_points - subtract_total

        db.commit()

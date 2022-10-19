from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from api.models import Competitor, Position, Race
from api.schemas import PositionCreate


def update_ranking(create_position: PositionCreate, db: Session):
    """Handle calculating the total and net points."""
    new_position = Position(**create_position.dict())

    new_points = (
        db.query(Position).filter(Position.race_id == new_position.race_id).count() + 1
    )

    new_position.points = new_points

    competitor: Competitor = (
        db.query(Competitor).filter(Competitor.sail_nr == new_position.sail_nr).first()
    )
    competitor.total_points += new_points

    db.add(new_position)

    subtract_total = 0
    race_count = db.query(Race).count()
    if (race_count > 0) and (race_count % 4 == 0):
        subtract_count = int(race_count / 4)

        all_competitor_positions: List[Position] = competitor.positions.order_by(
            desc(Position.points)
        ).all()
        for i in range(subtract_count):
            subtract_total += all_competitor_positions[i].points

    competitor.net_points = competitor.total_points - subtract_total

    db.commit()

import collections
from typing import Literal

import sqlalchemy as sa
from sqlalchemy.orm import Session

from app import models, schemas


def building_report(*, db: Session, building_id: str) -> schemas.BuildingReport | None:
    building: models.Building = db.query(models.Building).filter(models.Building.building_id == building_id).first()
    if not building:
        return None

    room_info_result = (
        db.query(models.Room.function, sa.func.count().label("cnt"))
        .filter(models.Room.building_id == building_id)
        .group_by(models.Room.function)
        .all()
    )
    room_distribution = schemas.RoomDistribution.parse_obj({row.function: row.cnt for row in room_info_result})

    return schemas.BuildingReport(
        building_id=building.building_id,
        building_name=building.building_name,
        building_type=building.building_type,
        street=building.street,
        house=building.house,
        room_distribution=room_distribution,
    )


def street_report(
    *,
    db: Session,
    order_by_room_function: schemas.RoomFunction,
    order_direction: Literal["asc", "desc"] = "desc",
    building_type: schemas.BuildingType | None = None,
    limit: int = 100,
) -> list[schemas.StreetReport]:
    query = db.query(models.Building.street, models.Room.function, sa.func.count().label("cnt")).join(
        models.Room, models.Room.building_id == models.Building.building_id
    )
    if building_type:
        query.filter(models.Building.building_type == building_type)

    result = query.group_by(models.Building.street, models.Room.function).all()

    # with more time this should happen in sql
    result_model: dict = collections.defaultdict(dict)
    for row in result:
        result_model[row.street][row.function] = row.cnt
    return sorted(
        [
            schemas.StreetReport(
                street=street,
                room_distribution=schemas.RoomDistribution(
                    meeting=result_model[street].get("meeting", 0),
                    office=result_model[street].get("office", 0),
                    recreation=result_model[street].get("recreation", 0),
                    other=result_model[street].get("other", 0),
                ),
            )
            for street in result_model
        ],
        key=lambda a: getattr(a.room_distribution, order_by_room_function),
        reverse=order_direction == "desc",
    )[:limit]

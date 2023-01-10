import datetime
import logging

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import Session
from typing_extensions import assert_never

from app import database, models
from app.schemas import base, events

logger = logging.getLogger(__file__)


class CRUDRoom:
    @classmethod
    def parse_event(cls, *, db: Session, crud_event: events.ResourceEventRoom):
        if isinstance(crud_event, events.ResourceEventRoomDelete):
            return cls.parse_delete_event(db=db, crud_event=crud_event)
        elif isinstance(crud_event, (events.ResourceEventRoomCreate, events.ResourceEventRoomUpdate)):
            return cls.parse_upsert_event(db=db, crud_event=crud_event)
        else:
            assert_never(crud_event)

    @classmethod
    def parse_upsert_event(
        cls, *, db: Session, crud_event: events.ResourceEventRoomCreate | events.ResourceEventRoomUpdate
    ):
        stmt = pg.insert(models.Room).values(
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
            event_timestamp=crud_event.timestamp,
            room_id=str(crud_event.payload.room_id),
            building_id=str(crud_event.payload.building_id),
            name=crud_event.payload.name,
            floor_number=crud_event.payload.floor_number,
            function=base.RoomFunction.parse(crud_event.payload.name),
        )
        on_update_stmt = stmt.on_conflict_do_update(
            index_elements=["room_id"],
            set_={
                "updated_at": stmt.excluded.updated_at,
                "event_timestamp": stmt.excluded.event_timestamp,
                "room_id": stmt.excluded.room_id,
                "building_id": stmt.excluded.building_id,
                "name": stmt.excluded.name,
                "floor_number": stmt.excluded.floor_number,
                "function": stmt.excluded.function,
            },
            where=(
                sa.and_(
                    models.Room.event_timestamp <= stmt.excluded.event_timestamp,
                    models.Room.deleted_at.is_not(None),
                )
            ),
        )
        db.execute(on_update_stmt)
        db.commit()

    @classmethod
    def parse_delete_event(cls, *, db: Session, crud_event: events.ResourceEventRoomDelete) -> models.Room:
        return db.execute(
            sa.update(models.Room)
            .where(models.Room.room_id == str(crud_event.payload.room_id))
            .values(
                event_timestamp=crud_event.timestamp,
                deleted_at=datetime.datetime.utcnow(),
            )
        )


class CRUDBuilding:
    @classmethod
    def parse_event(cls, *, db: Session, crud_event: events.ResourceEventBuilding):
        if isinstance(crud_event, events.ResourceEventBuildingDelete):
            return cls.parse_delete_event(db=db, crud_event=crud_event)
        elif isinstance(crud_event, (events.ResourceEventBuildingCreate, events.ResourceEventBuildingUpdate)):
            return cls.parse_upsert_event(db=db, crud_event=crud_event)
        else:
            assert_never(crud_event)

    @classmethod
    def parse_upsert_event(
        cls, *, db: Session, crud_event: events.ResourceEventBuildingCreate | events.ResourceEventBuildingUpdate
    ):
        # We don't distinguish between create or update, because we can't guarantee order,
        # i. e. that update comes after create
        for idx, char in enumerate(crud_event.payload.name):
            if char.isnumeric():
                street = crud_event.payload.name[:idx].strip()
                house = crud_event.payload.name[idx:].strip()
                break
        else:
            street = crud_event.payload.name
            house = None

        stmt = pg.insert(models.Building).values(
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
            event_timestamp=crud_event.timestamp,
            building_id=str(crud_event.payload.building_id),
            building_name=crud_event.payload.name,
            building_type=crud_event.payload.type,
            street=street,
            house=house,
        )
        on_update_stmt = stmt.on_conflict_do_update(
            index_elements=["building_id"],
            set_={
                "updated_at": stmt.excluded.updated_at,
                "event_timestamp": stmt.excluded.event_timestamp,
                "building_name": stmt.excluded.building_name,
                "building_type": stmt.excluded.building_type,
                "street": stmt.excluded.street,
                "house": stmt.excluded.house,
            },
            where=(
                sa.and_(
                    models.Building.event_timestamp <= stmt.excluded.event_timestamp,
                    models.Building.deleted_at.is_not(None),
                )
            ),
        )
        db.execute(on_update_stmt)
        db.commit()

    @classmethod
    def parse_delete_event(cls, *, db: Session, crud_event: events.ResourceEventBuildingDelete):
        db.execute(
            sa.update(models.Building)
            .where(models.Building.building_id == str(crud_event.payload.building_id))
            .values(
                event_timestamp=crud_event.timestamp,
                deleted_at=datetime.datetime.utcnow(),
            )
        )
        db.commit()


def parse_crud_event(crud_event: events.ResourceEvent):
    db = next(database.get_db())
    try:
        if isinstance(crud_event, events.RoomEventBase):
            return CRUDRoom.parse_event(db=db, crud_event=crud_event)
        if isinstance(crud_event, events.BuildingEventBase):
            return CRUDBuilding.parse_event(db=db, crud_event=crud_event)
        raise NotImplementedError("received unexpected event")
    except Exception as e:
        db.close()
        logger.exception(str(e))
        raise

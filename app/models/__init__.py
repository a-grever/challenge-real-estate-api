import sqlalchemy as sa

from app.database import Base
from app.schemas import base


@sa.orm.declarative_mixin
class TimestampableMixin:
    @sa.orm.declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    created_at = sa.Column(sa.DateTime)
    updated_at = sa.Column(sa.DateTime)
    deleted_at = sa.Column(sa.DateTime)


class Building(TimestampableMixin, Base):
    event_timestamp = sa.Column(sa.BigInteger)
    building_id = sa.Column(sa.String, primary_key=True)
    building_name = sa.Column(sa.String, nullable=False)
    building_type = sa.Column(sa.Enum(base.BuildingType), nullable=False)
    street = sa.Column(sa.String, nullable=False)
    house = sa.Column(sa.String, nullable=True)


class Room(TimestampableMixin, Base):
    event_timestamp = sa.Column(sa.BigInteger, nullable=False)
    room_id = sa.Column(sa.String, primary_key=True)
    #  not a ForeignKey because we can't guarantee that building event is processed before Room event
    building_id = sa.Column(sa.String)
    name = sa.Column(sa.String, nullable=False)
    floor_number = sa.Column(sa.Integer, nullable=False)
    function = sa.Column(sa.Enum(base.RoomFunction), nullable=False)

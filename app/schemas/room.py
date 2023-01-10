from .base import ResourcePayloadBase


class ResourcePayloadRoomBase(ResourcePayloadBase):
    room_id: str


class ResourcePayloadRoomCreate(ResourcePayloadRoomBase):
    building_id: str
    name: str
    floor_number: int


class ResourcePayloadRoomUpdate(ResourcePayloadRoomCreate):
    ...


class ResourcePayloadRoomDelete(ResourcePayloadRoomBase):
    ...

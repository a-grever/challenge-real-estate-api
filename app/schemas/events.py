from typing import Annotated, Generic, Literal, TypeVar, Union

import pydantic
from pydantic import Field, generics

from . import building, room
from .base import EventAction, ResourceType

TResourcePayloadRoom = TypeVar("TResourcePayloadRoom", bound=room.ResourcePayloadRoomBase)
TResourcePayloadBuilding = TypeVar("TResourcePayloadBuilding", bound=building.ResourcePayloadBuildingBase)


class ResourceEventBase(pydantic.BaseModel):
    message_id: str
    timestamp: int
    action: EventAction
    resource: ResourceType


# room events
class RoomEventBase(generics.GenericModel, Generic[TResourcePayloadRoom], ResourceEventBase):
    resource: Literal[ResourceType.room]
    payload: TResourcePayloadRoom


class ResourceEventRoomCreate(RoomEventBase[room.ResourcePayloadRoomCreate]):
    action: Literal[EventAction.created]


class ResourceEventRoomUpdate(RoomEventBase[room.ResourcePayloadRoomUpdate]):
    action: Literal[EventAction.updated]


class ResourceEventRoomDelete(RoomEventBase[room.ResourcePayloadRoomDelete]):
    action: Literal[EventAction.deleted]


ResourceEventRoom = Annotated[
    Union[
        ResourceEventRoomCreate,
        ResourceEventRoomUpdate,
        ResourceEventRoomDelete,
    ],
    Field(discriminator="action"),
]


# building events
class BuildingEventBase(pydantic.generics.GenericModel, Generic[TResourcePayloadBuilding], ResourceEventBase):
    resource: Literal[ResourceType.building]
    payload: TResourcePayloadBuilding


class ResourceEventBuildingCreate(BuildingEventBase[building.ResourcePayloadBuildingCreate]):
    action: Literal[EventAction.created]


class ResourceEventBuildingUpdate(BuildingEventBase[building.ResourcePayloadBuildingUpdate]):
    action: Literal[EventAction.updated]


class ResourceEventBuildingDelete(BuildingEventBase[building.ResourcePayloadBuildingDelete]):
    action: Literal[EventAction.deleted]


ResourceEventBuilding = Annotated[
    Union[
        ResourceEventBuildingCreate,
        ResourceEventBuildingUpdate,
        ResourceEventBuildingDelete,
    ],
    Field(discriminator="action"),
]

ResourceEvent = Annotated[
    Union[
        ResourceEventBuilding,
        ResourceEventRoom,
    ],
    Field(discriminator="resource"),
]

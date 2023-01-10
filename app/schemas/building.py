from .base import BuildingType, ResourcePayloadBase


class ResourcePayloadBuildingBase(ResourcePayloadBase):
    building_id: str


class ResourcePayloadBuildingCreate(ResourcePayloadBuildingBase):
    name: str
    type: BuildingType


class ResourcePayloadBuildingUpdate(ResourcePayloadBuildingCreate):
    ...


class ResourcePayloadBuildingDelete(ResourcePayloadBuildingBase):
    ...

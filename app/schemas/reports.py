import pydantic


class RoomDistribution(pydantic.BaseModel):
    meeting: int = 0
    office: int = 0
    recreation: int = 0
    other: int = 0


class BuildingReport(pydantic.BaseModel):
    building_id: str
    building_name: str
    building_type: str
    street: str
    house: str
    room_distribution: RoomDistribution


class StreetReport(pydantic.BaseModel):
    street: str
    room_distribution: RoomDistribution

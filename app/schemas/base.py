from __future__ import annotations

import enum

import pydantic


class StrEnum(str, enum.Enum):
    def _generate_next_value_(name, *_):
        return name


class EventAction(StrEnum):
    created = enum.auto()
    updated = enum.auto()
    deleted = enum.auto()


class ResourceType(StrEnum):
    room = enum.auto()
    building = enum.auto()


class ResourcePayloadBase(pydantic.BaseModel):
    ...


class BuildingType(StrEnum):
    Commercial_Office = "Commercial/Office"
    Commercial_Other = "Commercial/Other"
    Commercial_Retail = "Commercial/Retail"
    Cultural = "Cultural"
    Educational = "Educational"
    Government = "Government"
    Healthcare = "Healthcare"
    Hospitality = "Hospitality"
    Residential_Multi_Family = "Residential/Multi-Family"
    Residential_Single_Family = "Residential/Single Family"


class RoomFunction(StrEnum):
    office = enum.auto()
    meeting = enum.auto()
    recreation = enum.auto()
    other = enum.auto()

    @classmethod
    def parse(cls, room_function_str: str) -> RoomFunction:
        if room_function_str.startswith("Office"):
            return cls.office
        if room_function_str.startswith("Meeting"):
            return cls.meeting
        if room_function_str.startswith(("Lunch", "Break")):
            return cls.recreation
        return cls.recreation

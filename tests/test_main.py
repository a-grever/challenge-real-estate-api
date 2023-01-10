import pydantic
import pytest
from fastapi.testclient import TestClient

from app import crud, main, schemas


@pytest.fixture
def building_create_event():
    return {
        "message_id": "test",
        "timestamp": 1000000,
        "action": "created",
        "resource": "building",
        "payload": {
            "building_id": "1",
            "name": "main street 2",
            "type": "Healthcare",
            "floor_number": "1",
        },
    }


@pytest.fixture
def room_events():
    return (
        {
            "message_id": "test",
            "timestamp": 1000000,
            "action": "created",
            "resource": "room",
            "payload": {"room_id": "1", "building_id": "1", "name": "Office 1", "floor_number": "1"},
        },
        {
            "message_id": "test",
            "timestamp": 1000000,
            "action": "created",
            "resource": "room",
            "payload": {"room_id": "2", "building_id": "1", "name": "Office 2", "floor_number": "1"},
        },
        {
            "message_id": "test",
            "timestamp": 1000000,
            "action": "created",
            "resource": "room",
            "payload": {"room_id": "3", "building_id": "1", "name": "Meeting room 1", "floor_number": "1"},
        },
    )


def test_get_building_report(test_db, building_create_event, room_events):
    crud.parse_crud_event(crud_event=pydantic.parse_obj_as(schemas.ResourceEvent, building_create_event))
    for room_event in room_events:
        crud.parse_crud_event(crud_event=pydantic.parse_obj_as(schemas.ResourceEvent, room_event))

    expected = {
        "building_id": building_create_event["payload"]["building_id"],
        "building_name": building_create_event["payload"]["name"],
        "building_type": building_create_event["payload"]["type"],
        "street": "main street",
        "house": "2",
        "room_distribution": {
            "meeting": 1,
            "office": 2,
            "recreation": 0,
            "other": 0,
        },
    }
    with TestClient(main.app) as client:
        response = client.get("/api/v1/building_report/1")
        assert response.status_code == 200
        assert expected == response.json()


def test_get_street_report(test_db, building_create_event, room_events):
    crud.parse_crud_event(crud_event=pydantic.parse_obj_as(schemas.ResourceEvent, building_create_event))
    for room_event in room_events:
        crud.parse_crud_event(crud_event=pydantic.parse_obj_as(schemas.ResourceEvent, room_event))

    expected = [
        {
            "street": "main street",
            "room_distribution": {
                "meeting": 1,
                "office": 2,
                "recreation": 0,
                "other": 0,
            },
        }
    ]

    with TestClient(main.app) as client:
        response = client.get("/api/v1/street_report", params={"order_by_room_function": "office"})
        assert response.status_code == 200
        assert expected == response.json()

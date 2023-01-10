import random

import pika
import pydantic

from app.config import settings
from app.schemas import base, events

DATA_SET = {
    "street-one 1": {
        "building11": ("room111", "room112"),
        "building12": ("room121", "room121"),
    },
    "street-two 2": {
        "building21": ("room211", "room212"),
        "building22": ("room221", "room221"),
    },
    "street-three 3": {
        "building31": ("room311", "room312"),
        "building32": ("room321", "room321"),
    },
}

ROOM_NAMES = (
    "Office",
    "Meeting room",
    "Break room",
    "Conference room",
)


def generate_crud_event_room():
    street = random.choice(list(DATA_SET))
    building = random.choice(list(DATA_SET[street]))
    room = random.choice(list(DATA_SET[street][building]))
    room_name = f"{random.choice(ROOM_NAMES)} {random.randint(0, 100)}"

    action = random.choice([events.EventAction.created, events.EventAction.updated])

    message_body = {
        "message_id": "test",
        "timestamp": random.randint(10000, 1000000),
        "action": action,
        "resource": "room",
        "payload": {
            "room_id": room,
            "building_id": building,
            "name": room_name,
            "floor_number": random.randint(0, 20),
        },
    }

    return pydantic.parse_obj_as(events.ResourceEvent, message_body)


def generate_crud_event_building():
    street = random.choice(list(DATA_SET))
    building = random.choice(list(DATA_SET[street]))
    building_type = random.choice(list(base.BuildingType))

    action = random.choice([events.EventAction.created, events.EventAction.updated])

    message_body = {
        "message_id": "test",
        "timestamp": random.randint(10000, 1000000),
        "action": action,
        "resource": "building",
        "payload": {
            "building_id": building,
            "name": street,
            "type": building_type,
            "floor_number": random.randint(0, 20),
        },
    }

    return pydantic.parse_obj_as(events.ResourceEvent, message_body)


if __name__ == "__main__":
    credentials = pika.PlainCredentials(settings.rabbit_mq.user, settings.rabbit_mq.password)
    # parameters = pika.ConnectionParameters(
    #     settings.rabbit_mq.host, settings.rabbit_mq.port, "/", credentials=credentials
    # )
    parameters = pika.ConnectionParameters(settings.rabbit_mq.host)
    print(parameters)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=settings.rabbit_mq.queue)
    for _ in range(50):
        event = generate_crud_event_building()
        channel.basic_publish(exchange="", routing_key=settings.rabbit_mq.queue, body=event.json().encode("utf8"))
    for _ in range(500):
        event = generate_crud_event_room()
        channel.basic_publish(exchange="", routing_key=settings.rabbit_mq.queue, body=event.json().encode("utf8"))
    connection.close()

import logging
from signal import SIGINT, SIGTERM, signal

import crud
import pika
import pydantic

from app.config import settings
from app.schemas import events

logger = logging.getLogger(__name__)


class SignalHandler:
    def __init__(self):
        self.received_signal = False
        signal(SIGINT, self._signal_handler)
        signal(SIGTERM, self._signal_handler)

    def _signal_handler(self, signal, frame):
        logger.info(f"handling signal {signal}, exiting gracefully")
        self.received_signal = True


def callback(ch, method, properties, body):
    crud.parse_crud_event(crud_event=pydantic.parse_raw_as(events.ResourceEvent, body.decode()))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume():
    credentials = pika.PlainCredentials(settings.rabbit_mq.user, settings.rabbit_mq.password)
    parameters = pika.ConnectionParameters(
        settings.rabbit_mq.host, settings.rabbit_mq.port, "/", credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=settings.rabbit_mq.queue)
    logger.info("start consuming")
    signal_handler = SignalHandler()
    while not signal_handler.received_signal:
        channel.basic_consume(queue=settings.rabbit_mq.queue, on_message_callback=callback)
        try:
            channel.start_consuming()
        except Exception as e:
            logger.exception(e)
    requeued_messages = channel.cancel()
    print("Requeued %i messages" % requeued_messages)
    connection.close()


if __name__ == "__main__":
    consume()

import json
import typing

from aiokafka import AIOKafkaProducer

from src.application.ports.message_broker import MessageBroker


class KafkaMessageBroker(MessageBroker):
    def __init__(self, producer: AIOKafkaProducer, topic: str) -> None:
        self._producer = producer
        self._topic = topic

    async def send(
        self,
        payload: dict[str, typing.Any],
        headers: dict[str, str] | None = None,
    ) -> None:
        kafka_headers = [(k, v.encode()) for k, v in (headers or {}).items()]
        await self._producer.send_and_wait(self._topic, payload, headers=kafka_headers)


def serialize(value: dict[str, typing.Any]) -> bytes:
    return json.dumps(value, ensure_ascii=False).encode("utf-8")

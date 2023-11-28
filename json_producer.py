import time

from confluent_kafka import KafkaError, Message, Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka.serialization import MessageField, SerializationContext

from config import config, sr_config


class Temperature:
    """
    Temperature record.

    Args:
        city (str): City's name.
        reading(int): Temperature's reading.
        unit (str): Temperature's unit.
        timestamp (float): Timestamp.
    """

    def __init__(self, city: str, reading: int, unit: str, timestamp: float):
        self.city = city
        self.reading = reading
        self.unit = unit
        self.timestamp = timestamp


schema_str = """{
"$schema": "https://json-schema.org/draft/2020-12/schema",
"title": "Temperature",
"description": "Temperature sensor reading",
"type": "object",
"properties": {
    "city": {
        "description": "City name",
        "type": "string"
    },
    "reading": {
        "description": "Current temperature reading",
        "type": "number"
    },
    "unit": {
        "description": "Temperature unit (C/F)",
        "type": "string"
    },
    "timestamp": {
        "description": "Time of reading in ms since epoch",
        "type": "number"
    }
}
}
"""


def temp_to_dict(temp: Temperature, ctx: SerializationContext) -> dict:
    """
    Returns a dict representation of a User instance for serialization.

    Args:
        temp (Temperature): Temperature instance.
        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.

    Returns:
        dict: Dict populated with temperature attributes to be serialized.
    """
    return {
        "city": temp.city,
        "reading": temp.reading,
        "unit": temp.unit,
        "timestamp": temp.timestamp,
    }


data = [
    Temperature("London", 12, "C", round(time.time() * 1000)),
    Temperature("Chicago", 63, "F", round(time.time() * 1000)),
    Temperature("Berlin", 14, "C", round(time.time() * 1000)),
    Temperature("Madrid", 18, "C", round(time.time() * 1000)),
    Temperature("Udia", 88, "F", round(time.time() * 1000)),
]


def delivery_report(err: KafkaError, msg: Message):
    if err is not None:
        print(f'Delivery failed on reading for {msg.key().decode("utf8")}: {err}')
    else:
        print(f'Temp reading for {msg.key().decode("utf8")} produced to {msg.topic()}')


if __name__ == "__main__":
    topic = "temp_readings"
    schema_registry_client = SchemaRegistryClient(sr_config)

    json_serializer = JSONSerializer(schema_str, schema_registry_client, temp_to_dict)

    producer = Producer(config)
    for temp in data:
        producer.produce(
            topic=topic,
            key=str(temp.city),
            value=json_serializer(
                temp, SerializationContext(topic, MessageField.VALUE)
            ),
            on_delivery=delivery_report,
        )
    producer.flush()

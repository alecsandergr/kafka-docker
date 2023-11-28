from typing import Optional

from confluent_kafka import Consumer
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka.serialization import MessageField, SerializationContext

from config import config


class Temperature:
    """
    Temperature record.

    Args:
        city (str, optional): City's name.
        reading(int, optional): Temperature's reading.
        unit (str, optional): Temperature's unit.
        timestamp (float, optional): Timestamp.
    """

    def __init__(
        self,
        city: Optional[str] = None,
        reading: Optional[int] = None,
        unit: Optional[str] = None,
        timestamp: Optional[float] = None,
    ) -> None:
        self.city = city
        self.reading = reading
        self.unit = unit
        self.timestamp = timestamp


def set_consumer_config():
    config["group.id"] = "temp_group"
    config["auto.offset.reset"] = "earliest"


def dict_to_temp(obj: dict, ctx: SerializationContext) -> Temperature:
    """
    Converts object literal(dict) to a Temperature instance.

    Args:
        obj (dict): Object literal(dict).
        ctx (SerializationContext): Metadata pertaining to the serialization operation.

    Returns:
        Temperature: temperature instance.
    """

    if obj is None:
        return None

    return Temperature(
        city=obj["city"],
        reading=obj["reading"],
        unit=obj["unit"],
        timestamp=obj["timestamp"],
    )


schema_str = """{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Temperature",
    "description": "Temperature sensor reading",
    "type": "object",
    "properties": {
        "city": {
            "description": "City's name",
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
}"""


def main():
    topic = "temp_readings"

    json_deserializer = JSONDeserializer(schema_str, from_dict=dict_to_temp)

    set_consumer_config()
    consumer = Consumer(config)
    consumer.subscribe([topic])

    while True:
        try:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            temp = json_deserializer(
                msg.value(), SerializationContext(topic, MessageField.VALUE)
            )

            if temp is not None:
                print(f"Latest temp in {temp.city} is {temp.reading} {temp.unit}.")
        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == "__main__":
    main()

from typing import Optional

from confluent_kafka import Consumer
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka.serialization import MessageField, SerializationContext

from config import config


class User:
    """
    User record.

    Args:
        name (str, optional): User's name. Defaults to None.
        favorite_number (int, optional): User's favorite number. Defaults to None.
        favorite_color (str, optional): User's favorite color. Defaults to None.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        favorite_number: Optional[int] = None,
        favorite_color: Optional[str] = None,
    ) -> None:
        self.name = name
        self.favorite_number = favorite_number
        self.favorite_color = favorite_color


def set_consumer_config():
    config["group.id"] = "user_group"
    config["auto.offset.reset"] = "earliest"


def dict_to_user(obj: dict, ctx: SerializationContext) -> User:
    """
    Converts object literal(dict) to a User instance.

    Args:
        obj (dict): Object literal(dict).
        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.

    Returns:
        User: User instance.
    """
    if obj is None:
        return None

    return User(
        name=obj["name"],
        favorite_number=obj["favorite_number"],
        favorite_color=obj["favorite_color"],
    )


schema_str = """{
    "$schema": "https://json-schema.org/draft-07/schema#",
    "title": "User",
    "description": "A Confluent Kafka Python User",
    "type": "object",
    "properties": {
        "name": {
            "description": "User's name",
            "type": "string"
        },
        "favorite_number": {
            "description": "User's favorite number",
            "type": "number"
        },
        "favorite_color": {
            "description": "User's favorite color",
            "type": "string"
        }
    },
    "required": [ "name", "favorite_number", "favorite_color" ]
}"""


def main():
    topic = "user_json"

    json_deserializer = JSONDeserializer(schema_str, from_dict=dict_to_user)

    set_consumer_config()
    consumer = Consumer(config)
    consumer.subscribe([topic])

    while True:
        try:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            user = json_deserializer(
                msg.value(), SerializationContext(topic, MessageField.VALUE)
            )

            if user is not None:
                print(
                    f"User record {msg.key()}: \n\tname: {user.name}\n"
                    f"\tfavorite_number: {user.favorite_number}\n"
                    f"\tfavorite_color: {user.favorite_color}\n"
                )
        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == "__main__":
    main()

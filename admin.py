from confluent_kafka.admin import AdminClient, ConfigResource, NewTopic

from config import config


def topic_exists(admin: AdminClient, topic: str) -> bool:
    """Returns true if the given topic exists"""
    metadata = admin.list_topics()
    for t in iter(metadata.topics.values()):
        if t.topic == topic:
            return True
    return False


def create_topic(
    admin: AdminClient, topic: str, num_partitions: int = 3, replication_factor: int = 1
):
    """
    Generate a topic.

    Args:
        admin (AdminClient): AdminClient instance.
        topic (str): Topic's name.
        num_partitions (int, optional): Number of partitions.. Defaults to 3.
        replication_factor (int, optional): Replication factor. Defaults to 1.
    """

    new_topic = NewTopic(
        topic, num_partitions=num_partitions, replication_factor=replication_factor
    )
    result_dict = admin.create_topics([new_topic])
    for topic, future in result_dict.items():
        try:
            future.result()
            print(f"Topic {topic} created")
        except Exception as e:
            print(f"Failed to create topic {topic}: {e}")


def get_max_size(admin: AdminClient, topic: str) -> str:
    """
    Get the max size in bytes of the message topic.

    Args:
        admin (AdminClient): AdminClient instance.
        topic (str): Topic's name.

    Returns:
        str: max size in bytes.
    """
    resource = ConfigResource("topic", topic)
    result_dict = admin.describe_configs([resource])
    config_entries = result_dict[resource].result()
    max_size = config_entries["max.message.bytes"]
    print(type(max_size.value))
    return max_size.value


def set_max_size(admin: AdminClient, topic: str, max_k: int):
    """
    Defines the maximum size of the message in the given topic.

    Args:
        admin (AdminClient): AdminClient instance.
        topic (str): Topic's name.
        max_k (int): max size in bytes.
    """

    config_dict = {"max.message.bytes": str(max_k * 1024)}
    resource = ConfigResource("topic", topic, config_dict)
    result_dict = admin.alter_configs([resource])
    result_dict[resource].result()


if __name__ == "__main__":
    # Create Admin client
    admin = AdminClient(config)
    topic_name = "my_topic"
    max_msg_k = 50

    # Create topic if it doesn't exist
    if not topic_exists(admin, topic_name):
        create_topic(admin, topic_name)

    # Check max.message.bytes config and set if needed
    current_max = get_max_size(admin, topic_name)
    if current_max != str(max_msg_k * 1024):
        print(f"Topic, {topic_name} max.message.bytes is {current_max}.")
        set_max_size(admin, topic_name, max_msg_k)

    # Verify config was set
    new_max = get_max_size(admin, topic_name)
    print(f"Now max.message.bytes for topic {topic_name} is {new_max}")

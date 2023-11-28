from typing import Optional

from confluent_kafka.admin import AdminClient, NewTopic

from config import config

# Specify the Kafka broker(s) in the KAFKA_BOOTSTRAP_SERVERS configuration
# KAFKA_BOOTSTRAP_SERVERS = config["kafka_bootstrap_servers"]


# Create an AdminClient instance
def create_admin_client(servers: Optional[list] = None) -> AdminClient:
    """
    Defines the admin client.

    Args:
        servers (list, optional): list of brokers. Defaults to KAFKA_BOOTSTRAP_SERVERS.

    Returns:
        AdminClient: admin
    """

    if servers is not None:
        config["bootstrap.servers"] = ",".join(servers)
    admin_client = AdminClient(config)
    return admin_client


# return True if topic exists and False if not
def topic_exists(admin: AdminClient, topic: str) -> bool:
    """
    Check if topic exists.

    Args:
        admin (AdminClient): admin client.
        topic (str): name of the topic.

    Returns:
        bool: if topic exists.
    """
    metadata = admin.list_topics()
    for t in iter(metadata.topics.values()):
        if t.topic == topic:
            return True
    return False


def create_topic(
    topic: str,
    admin_client: AdminClient,
    num_partitions: int = 1,
    replication_factor: int = 1,
):
    """
    Generate a topic.

    Args:
        topic_name (str): Name of the topic.
        num_partitions (int): Number of partitions.
        replication_factor (int): Replication factor (number of brokers).
        admin_client (AdminClient): AdminClient instance.
    """

    new_topic = NewTopic(
        topic=topic,
        num_partitions=num_partitions,
        replication_factor=replication_factor,
    )
    result_dict = admin_client.create_topics([new_topic])

    for topic, future in result_dict.items():
        try:
            future.result()  # The result itself is None
            print(f"Topic {topic} created")
        except Exception as e:
            print(f"Failed to create topic {topic}: {e}")


if __name__ == "__main__":
    # Create Admin client
    admin = create_admin_client()
    topic_name = "bulhufas"

    # Create topic if it doesn't exist
    if not topic_exists(admin, topic_name):
        create_topic(topic_name, admin, replication_factor=3)
        create_topic(topic_name, admin, replication_factor=3)

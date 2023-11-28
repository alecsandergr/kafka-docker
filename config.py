kafka_bootstrap_servers = ["127.0.0.1:9092", "127.0.0.1:9093", "127.0.0.1:9094"]
kafka_schema_registry = "http://0.0.0.0:8081"

config = {"bootstrap.servers": ",".join(kafka_bootstrap_servers)}

sr_config = {"url": kafka_schema_registry}

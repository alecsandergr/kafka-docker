# Apache Kafka First Steps <!-- omit in toc -->

Author: Alecsander Guimarães Rodrigues 

[Github](http://github.com/alecsandergr)

[LinkedIn](http://linkedin.com/in/alecsandergr)

## Table of Contents <!-- omit in toc -->

- [Summary](#summary)
- [Creating the containers](#creating-the-containers)
- [Creating the virtual environment](#creating-the-virtual-environment)
- [Using Kakfa](#using-kakfa)

## Summary

This repository contains some examples of how to use Kafka, like how to create a topic, a producer and a consumer. For that, you must have installed Docker, if you yet don't have Docker installed, check the [website](https://docs.docker.com/get-docker/).

If you want to learn more about Kafka, you can check out this [repository](https://github.com/confluentinc/confluent-kafka-python) or the [Introduction to Python for Apache Kafka](https://developer.confluent.io/courses/kafka-python/intro/). 

## Creating the containers

You can check the docker-compose file [here](docker-compose.yml), but all you need to do, once you have installed the Docker, is to replicate the commands below.

```sh
# Run the commands to start the container and the network
docker network create docker_streaming
docker-compose -f docker-compose.yml up -d
# Stop the container when finished
docker-compose -f docker-compose.yml down
```

## Creating the virtual environment

For this project, if you have poetry installed, follow the instructions below:

```bash
# Create the virtual environment and install all dependencies
poetry install
# Activate the virtual environment
poetry shell
```

If you don't have, you can use venv:
```bash
# if you use macOS/Unix
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
# if you use Windows
py -m venv .venv
.venv\bin\Activate.bat
py -m pip install -r requirements.txt
```
## Using Kakfa

Below are some examples of how you can use Kafka.

- [Creating a topic](topic.py) 
- [Consumer](consumer.py)
- [Producer](producer.py)
- [Consumer using Schema Registry](json_consumer.py)
- [Producer using Schema Registry](json_producer.py)
- [Admin Client functionality](admin.py)
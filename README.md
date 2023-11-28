# Apache Kafka First Steps <!-- omit in toc -->

Author: Alecsander Guimarães Rodrigues 

[Github](http://github.com/alecsandergr)

[LinkedIn](http://linkedin.com/in/alecsandergr)

## Table of Contents <!-- omit in toc -->

- [Summary](#summary)
- [Creating the containers](#creating-the-containers)
- [Creating the virtual environment](#creating-the-virtual-environment)
- [Using Kafka](#using-kafka)

## Summary

This repository contains some examples of how to use Kafka, like how to create a topic, a producer and a consumer. For that, you must have installed Docker, if you don't have Docker installed yet, check the [website](https://docs.docker.com/get-docker/).

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

```sh
# Install Poetry using the official installer
curl -sSL https://install.python-poetry.org | python3 -
# Navigate to your project's directory
cd your_project_directory
# Install the dependencies
poetry install
# Activate the virtual environment
poetry shell
```

You can also check the official documentation [here](https://python-poetry.org/docs/), if you would like to install it.

If you don't have, you can use venv:
```sh
# if you use macOS/Unix
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
# if you use Windows
py -m venv .venv
.venv\bin\Activate.bat
py -m pip install -r requirements.txt
```

## Using Kafka

Below are some examples of how you can use Kafka.

- [Creating a topic](topic.py) 
- [Consumer](consumer.py)
- [Producer](producer.py)
- [Consumer using Schema Registry](json_consumer.py)
- [Producer using Schema Registry](json_producer.py)
- [Admin Client functionality](admin.py)
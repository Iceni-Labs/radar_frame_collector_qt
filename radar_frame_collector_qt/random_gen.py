import random
from time import sleep
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import os
import sys

ARRAY_LEN = 468
FPS = int(sys.argv[1]) or 10

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "safescan_1/random_data"


def start():
    print(f"Running in a loop at {FPS} fps")
    while True:
        random_array = [random.randint(-1000, 1000) for _ in range(ARRAY_LEN)]
        json_out = json.dumps(random_array)
        publish.single(
            topic=MQTT_TOPIC,
            payload=json_out,
            hostname=MQTT_BROKER,
        )
        sleep(1 / FPS)


if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        exit(0)

import random
from time import sleep
import paho.mqtt.publish as publish
import json
import sys

ARRAY_LEN = int(sys.argv[1]) or 468
FPS = int(sys.argv[2]) or 10
MIN_MAX = (-1000, 1000)

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "safescan_1/random_data"


def start():
    print(f"Generating {ARRAY_LEN} numbers between {MIN_MAX[0]}:{MIN_MAX[1]} in a loop at {FPS} fps")
    while True:
        random_array = [random.randint(*MIN_MAX) for _ in range(ARRAY_LEN)]
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

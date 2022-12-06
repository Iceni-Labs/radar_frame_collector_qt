import json
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage
from queue import Queue
from typing import Any, Iterable

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_SUB_TOPIC = "xethru/radar_data"

DATA_QUEUE: Queue = Queue()


def start_consumer():
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()


def on_connect(client: mqtt.Client, userdata: Any, flags: Any, rc: Any):
    print(f"Connected to {MQTT_BROKER}:{MQTT_PORT} with result code {str(rc)}")
    client.subscribe(MQTT_SUB_TOPIC)


def on_message(client: mqtt.Client, userdata: Any, msg: MQTTMessage) -> None:
    data = json.loads(msg.payload)
    add_data(data["data"])


def add_data(data, queue: Queue = DATA_QUEUE) -> int:
    queue.put_nowait(data)
    if (size := queue.qsize()) > 2:
        print(f"queue size: {size}")
    return size


def get_data(queue: Queue = DATA_QUEUE) -> tuple[Iterable, Iterable]:
    """Return (x, y) tuple"""
    y = queue.get(block=True)
    x = range(len(y))
    return x, y


if __name__ == "__main__":
    try:
        start_consumer()
    except KeyboardInterrupt:
        exit(0)

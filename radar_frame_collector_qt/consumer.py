import json
import paho.mqtt.client as mqtt
from queue import Queue

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_SUB_TOPIC = "safescan_1/#"

DATA_QUEUE = Queue()


def start_consumer():
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()


def on_connect(client, userdata, flags, rc):
    print(f"Connected to {MQTT_BROKER}:{MQTT_PORT} with result code {str(rc)}")
    client.subscribe(MQTT_SUB_TOPIC)


def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    add_data(data)


def add_data(data, queue: Queue = DATA_QUEUE):
    queue.put_nowait(data)
    if (size := queue.qsize()) > 2:
        print(f"queue size: {size}")


def get_data(queue: Queue = DATA_QUEUE):
    return queue.get(block=True)

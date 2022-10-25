from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
import pyqtgraph as pg
import sys
from random import randint
from paho.mqtt import client as mqtt_client
import json

broker = '127.0.0.1'
port = 1883
topic = "safescan_1/#"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{randint(0, 100)}'
# username = 'emqx'
# password = 'public'

class MainWindow(QMainWindow):

    def __init__(self):

        self.x_axis_range = 468

        self.m_decode = []
        self.decodedArrays = []
        super(MainWindow, self).__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.x = list(range(self.x_axis_range))  # 100 time points
        self.y = [randint(-10, 10) for _ in range(self.x_axis_range)]  # 100 data points

        self.graphWidget.setBackground('w')

        title_style = {'color': 'b', 'size': '40px'}
        self.graphWidget.setTitle("SafeScan Radar Visualisation", **title_style)

        styles = {'color': 'b', 'font-size': '20px'}
        self.graphWidget.setLabel('left', 'Radar Signal', **styles)
        self.graphWidget.setLabel('bottom', 'Distance from Radar', **styles)
        self.graphWidget.setXRange(0, self.x_axis_range, padding=0)
        self.graphWidget.setYRange(-1000, 1000, padding=0)

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)

        self.connect_mqtt()
        self.client = self.connect_mqtt()

        self.timer = QTimer()
        self.timer.setInterval(5)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):

        self.subscribe(self.client)
        self.client.loop(0.001)
        self.y = self.m_decode[0:self.x_axis_range]
        self.data_line.setData(self.x, self.y)  # Update the data.

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(client_id)
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client

    def subscribe(self, client: mqtt_client):

        def on_message(client, userdata, msg):
            # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

            self.msg_decode = str(msg.payload.decode("utf-8", "ignore"))
            self.m_decode = json.loads(self.msg_decode)

        self.client.subscribe(topic)
        self.client.on_message = on_message


app = QApplication(sys.argv)
main = MainWindow()
main.show()
app.exec()

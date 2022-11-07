from random import randint
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
import pyqtgraph as pg
import sys

from . import consumer

X_RANGE = (0, 468)
Y_RANGE = (-1000, 1000)


def start():
    app = QApplication(sys.argv)
    main = MainWindow(x_range=X_RANGE, y_range=Y_RANGE)
    consumer.start_consumer()
    main.show()
    app.exec()


class MainWindow(QMainWindow):
    def __init__(self, x_range: tuple, y_range: tuple):
        super(MainWindow, self).__init__()

        self.x_min, self.x_max = x_range
        self.y_min, self.y_max = y_range

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.x = list(range(self.x_max))  # 100 time points
        self.y = [randint(-10, 10) for _ in range(self.x_max)]  # 100 data points

        self.graphWidget.setBackground("w")

        title_style = {"color": "b", "size": "40px"}
        self.graphWidget.setTitle("SafeScan Radar Visualisation", **title_style)

        styles = {"color": "b", "font-size": "20px"}
        self.graphWidget.setLabel("left", "Radar Signal", **styles)
        self.graphWidget.setLabel("bottom", "Distance from Radar", **styles)
        self.graphWidget.setXRange(self.x_min, self.x_max, padding=0)
        self.graphWidget.setYRange(self.y_min, self.y_max, padding=0)

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)

        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        new_data = consumer.get_data()
        self.y = new_data[0 : self.x_max]
        self.data_line.setData(self.x, self.y)  # Update the data.


if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        exit(0)

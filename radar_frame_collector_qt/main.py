from typing import Callable
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer, QProcess
import pyqtgraph as pg
import sys

from . import consumer

X_RANGE = (0, 500)
Y_RANGE = (-1000, 1000)


def start():
    app = QApplication(sys.argv)
    main = MainWindow(x_range=X_RANGE, y_range=Y_RANGE, get_data_func=consumer.get_data)
    consumer.start_consumer()
    main.show()
    sys.exit(app.exec())


class MainWindow(QMainWindow):
    def __init__(self, x_range: tuple, y_range: tuple, get_data_func: Callable):
        super().__init__()

        self.x_min, self.x_max = x_range
        self.y_min, self.y_max = y_range
        self.get_data = get_data_func

        # plot stuff
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.graphWidget.setBackground("w") 

        title_style = {"color": "b", "size": "40px"}
        self.setWindowTitle("SafeScan Radar Visualisation")
        self.graphWidget.setTitle("SafeScan Radar Visualisation", **title_style)

        styles = {"color": "b", "font-size": "20px"}
        self.graphWidget.setLabel("left", "Radar Signal", **styles)
        self.graphWidget.setYRange(self.y_min, self.y_max, padding=0)
        self.graphWidget.setLabel("bottom", "Distance from Radar", **styles)
        self.graphWidget.setXRange(self.x_min, self.x_max, padding=0)

        pen = pg.mkPen(color=(255, 0, 0))
        x = range(self.x_max)
        y = [0] * self.x_max
        self.data_line = self.graphWidget.plot(x=x, y=y, pen=pen)

        self.timer = self.set_up_timer()
        self.timer.start()

    def set_up_timer(self, millis: int = 1) -> QTimer:
        timer = QTimer()
        timer.setInterval(millis)
        timer.timeout.connect(self.update_plot_data)
        return timer

    def update_plot_data(self) -> bool:
        x, y = self.get_data()  # this should be a blocking function

        len_x, len_y = (len(x), len(y))

        if not len_x == len_y:
            return False

        if not len_x == self.x_max:
            print(f"Data size changed ({len_x} != {self.x_max}). Re-creating x-axis.")
            self.x_max = len_x
            self.graphWidget.setXRange(self.x_min, self.x_max)

        self.data_line.setData(x, y)  # Update the data
        return True


if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        exit(0)

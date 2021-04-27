import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtWidgets import QInputDialog, QColorDialog
from PyQt5.QtCore import Qt
import os
import datetime as dt
from pyqtgraph import *
from predict_figure import *


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window()

    def main_window(self):
        # первое окно с оновными функциями программы
        uic.loadUi('main.ui', self)
        self.form_prediction.clicked.connect(self.predict_form_window)
        self.cast_curve_buid.clicked.connect(self.cast_curve_buid_window)
        
    def predict_form_window(self):
        uic.loadUi('predict_form.ui', self)
        self.get_result.clicked.connect(self.get_model_result)
        self.back.clicked.connect(self.main_window)
    
    def cast_curve_buid_window(self):
        uic.loadUi('cast_curve_buid.ui', self)
        self.create_model.clicked.connect(self.user_model)
        self.figure.addItems(['cube', 'circle', 'clock'])
        self.back.clicked.connect(self.main_window)
        self.before.setValue(3)
        self.after.setValue(3)
        self.length.setValue(30)
        self.radius.setText('0.3')
    
    def user_model(self):
        try:
            radius = float(self.radius.text())
            before = self.before.value()
            after = self.after.value()
            length = self.length.value()
            figure = str(self.figure.currentText())
            model_photos(radius, length, figure, before=before, after=after)
            jpg_to_clear_data(f'for_model_{figure}', 'model')
            data = get_clear_data(f'model\\for_model_{figure}_data.txt')

            self.custom_graph.clear()
            self.custom_graph.plot([i for i in range(len(data))], data, pen='r')
        except Exception as e:
            self.error.setText('произошла ошибка ' + str(e))
    
    def graph(self, data, circle, cube, clock):
        self.circle.clear()
        self.circle.plot([i for i in range(len(data))], data, pen='r')
        self.circle.plot([i for i in range(len(circle))], circle, pen='b')

        self.cube.clear()
        self.cube.plot([i for i in range(len(data))], data, pen='r')
        self.cube.plot([i for i in range(len(cube))], cube, pen='b')

        self.clock.clear()
        self.clock.plot([i for i in range(len(data))], data, pen='r')
        self.clock.plot([i for i in range(len(clock))], clock, pen='b')

    def get_model_result(self):
        directory = self.directory.text()
        maxx_name, data, circle, cube, clock = for_app(directory, button=self.is_now)
        self.result.setText(maxx_name)
        self.graph(data, circle, cube, clock)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

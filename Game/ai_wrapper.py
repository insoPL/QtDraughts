# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
from .AI import ai


class ThreadAI(QThread):
    finished_calculation = pyqtSignal()

    def __init__(self, pieces):
        self.pieces = pieces
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.value = ai(*self.pieces.two_lists)
        self.finished_calculation.emit()




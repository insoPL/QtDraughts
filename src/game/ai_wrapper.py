# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
from .AI import ai


class ThreadAI(QThread):
    finished_calculation = pyqtSignal()

    def __init__(self, pieces, settings):
        self.pieces = pieces
        self.settings = settings
        QThread.__init__(self)
        self.best_move = None

    def __del__(self):
        self.wait()

    def run(self):
        self.best_move = ai(*self.pieces.two_lists, settings=self.settings)

        self.finished_calculation.emit()




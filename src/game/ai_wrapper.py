# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
from .ai import ai


class ThreadAI(QThread):
    finished_calculation = pyqtSignal()

    def __init__(self, pieces, settings, force_move):
        self.pieces = pieces
        self.settings = settings
        self.force_move = force_move
        QThread.__init__(self)
        self.best_move = None

    def __del__(self):
        self.wait()

    def run(self):
        self.best_move = ai(self.pieces.list_of_pieces, self.settings, self.force_move)

        self.finished_calculation.emit()




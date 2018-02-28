# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon


class MainButton(QAction):
    def __init__(self, main_window):
        self.main_window = main_window
        QAction.__init__(self, 'New game', main_window)
        self.setShortcut('Ctrl+N')
        self.update()

    def update(self):
        if self.main_window.game.whoseTurn is None:
            self.setIcon(QIcon('graphics/start.png'))
        elif self.main_window.game.settings.ai and self.main_window.game.whoseTurn:
            self.setIcon(QIcon('graphics/computer.png'))
        elif self.main_window.game.whoseTurn:
            self.setIcon(QIcon('graphics/light_gray.png'))
        else:
            self.setIcon(QIcon('graphics/black.png'))


# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon


class MainButton:
    def __init__(self, mainWindow):
        self.qAction = QAction(QIcon('graphics/start.png'), 'New Game', mainWindow)
        self.qAction.setShortcut('Ctrl+N')

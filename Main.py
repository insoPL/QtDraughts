# -*- coding: utf-8 -*-

import logging
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QColorDialog

from Game import Game
from settingsWindow import SettingsWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.debug("Initialization...")
        self.init_ui()
        self.game = Game(self)
        self.show()

        logging.debug("Initialization complete")

    def init_toolbar(self):
        self.toolbar = self.addToolBar("Bar")
        self.toolbar.setMovable(False)
        # New Game
        new_game_act = QAction(QIcon('graphics/start.png'), 'New Game', self)
        new_game_act.setShortcut('Ctrl+N')
        self.toolbar.addAction(new_game_act)
        
        # Options
        options_act = QAction(QIcon('graphics/settings.png'), 'Options', self)
        options_act.setShortcut('Ctrl+O')
        options_act.triggered.connect(self.showSettings)
        self.toolbar.addAction(options_act)


        # Exit Game
        exit_act = QAction(QIcon('graphics/exit.png'), 'Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(qApp.quit)

        self.toolbar.addAction(exit_act)

    def init_ui(self):
        self.setMinimumSize(300,300)
        self.setWindowTitle('Draughts')
        self.init_toolbar()

    def paintEvent(self, e):
        self.game.update_drawing()

    def showSettings(self):
        self.settings = SettingsWindow()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QWidget
from PyQt5.QtGui import QIcon
import logging
from Game import Game


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        logging.info("Initialization...")
        self.init_ui()
        self.game = Game(self)
        self.show()

        logging.info("Initialization complete")

    def init_toolbar(self):
        self.toolbar = self.addToolBar("Bar")
        self.toolbar.setMovable(False)
        # New Game
        new_game_act = QAction(QIcon('start.png'), 'New Game', self)
        new_game_act.setShortcut('Ctrl+N')
        self.toolbar.addAction(new_game_act)
        
        # Options
        options_act = QAction(QIcon('settings.png'), 'Options', self)
        options_act.setShortcut('Ctrl+O')
        self.toolbar.addAction(options_act)


        # Exit Game
        exit_act = QAction(QIcon('exit.png'), 'Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(qApp.quit)

        self.toolbar.addAction(exit_act)

    def init_ui(self):
        self.setMinimumSize(300,300)
        self.setWindowTitle('Draughts')
        self.init_toolbar()

    def paintEvent(self, e):
        logging.debug("PaintEvent")
        self.game.update_drawing()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

import logging
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QColorDialog, QWidget, QSizePolicy
from PyQt5.QtCore import QSize

from Game import Game
from settingsWindow import SettingsWindow
from settings import Settings
from mainButton import MainButton


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.debug("Initialization...")
        self.init_ui()
        self.settings = Settings()
        self.game = Game(self, self.settings)
        self.main_button = MainButton(self)
        self.show()

        logging.info("Game Ready!")

    def init_toolbar(self):
        self.toolbar = self.addToolBar("Bar")
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(28, 28))

        # Options
        options_act = QAction(QIcon('graphics/settings.png'), 'Options', self)
        options_act.setShortcut('Ctrl+O')
        options_act.triggered.connect(self.show_settings_window)
        self.toolbar.addAction(options_act)

        # Blank Space
        spacer_widget = QWidget(self)
        spacer_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer_widget)

        # Main Button
        self.main_button = MainButton(self)
        self.toolbar.addAction(self.main_button.qAction)

        # Blank Space
        spacer_widget2 = QWidget(self)
        spacer_widget2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer_widget2)

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

    def show_settings_window(self):
        self.settings_windows = SettingsWindow(self.settings)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())

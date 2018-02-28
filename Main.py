# -*- coding: utf-8 -*-

import logging
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QColorDialog, QWidget, QSizePolicy, QMessageBox
from PyQt5.QtCore import QSize

from Game import Game
from settingsWindow import SettingsWindow
from settings import Settings
from MainButton import MainButton


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.debug("Initialization...")
        self.settings = Settings()
        self.game = Game(self, self.settings)
        self.init_ui()
        self.show()

        logging.info("Game Ready!")

    def init_toolbar(self):
        self.toolbar = self.addToolBar("Bar")
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(28, 28))

        # Surrender
        self.surrender_button = QAction(QIcon('graphics/surrender.png'), 'Surrender', self)
        self.surrender_button.triggered.connect(self.surrender_button_clicked)
        self.surrender_button.setDisabled(True)
        self.toolbar.addAction(self.surrender_button)

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
        self.main_button.triggered.connect(self.start_button_clicked)
        self.toolbar.addAction(self.main_button)

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
        self.settings_window = SettingsWindow(self.settings)

    def start_button_clicked(self):
        if self.game.pieces is None:
            self.game.start_match()

    def surrender_button_clicked(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Player surrendered")
        if self.settings.ai:
            msgBox.setText("You lost.\n Do You want to play again?")
        else:
            pass
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.buttonClicked.connect(self.surrender_button_clicked_answered)
        msgBox.exec_()

    def surrender_button_clicked_answered(self, i):
        if i.text() == "&Yes":
            self.game.end_math()
            self.game.start_match()
        elif i.text() == "&No":
            self.surrender_button.setDisabled(True)
            self.game.end_math()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())

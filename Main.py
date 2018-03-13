    # -*- coding: utf-8 -*-

import logging
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QWidget, QSizePolicy, QMessageBox

from game import Game
from MainButton import MainButton
from settings import Settings
from settingsWindow import SettingsWindow
from connectionWindow import ConnectionWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.debug("Initialization...")
        self.setWindowIcon(QIcon('graphics\start.png'))
        self.settings = Settings()
        self.game = Game(self, self.settings)
        self.init_ui()

        if self.settings.always_on_top:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.show()

        logging.info("game Ready!")

    def init_toolbar(self):
        self.toolbar = self.addToolBar("Bar")
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(28, 28))

        # Surrender
        self.surrender_button = QAction(QIcon('graphics/surrender.png'), 'Surrender', self)
        self.surrender_button.triggered.connect(self.surrender_button_clicked)
        self.surrender_button.setDisabled(True)
        self.toolbar.addAction(self.surrender_button)

        # Multiplayer
        self.multiplayer_button = QAction(QIcon('graphics/internet.png'), 'Surrender', self)
        self.multiplayer_button.triggered.connect(self.establish_internet_connection)
        self.toolbar.addAction(self.multiplayer_button)

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

        # Options
        options_act = QAction(QIcon('graphics/settings.png'), 'Options', self)
        options_act.setShortcut('Ctrl+O')
        options_act.triggered.connect(self.show_settings_window)
        self.toolbar.addAction(options_act)

        # Exit game
        exit_act = QAction(QIcon('graphics/exit.png'), 'Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(qApp.quit)

        self.toolbar.addAction(exit_act)

    def init_ui(self):
        self.setMinimumSize(300, 300)
        self.setWindowTitle('Draughts')
        self.init_toolbar()

    # noinspection PyUnusedLocal
    def paintEvent(self, e):
        self.game.update_drawing()

    def show_settings_window(self):
        self.settings_window = SettingsWindow(self.settings)

    def start_button_clicked(self):
        if self.game.pieces is None:
            self.game.start_match()

    def surrender_button_clicked(self):
        if self.game.multiplayer:
            self.game.network_thread.send_special_action("surrender")
            self.game.end_match()
            self.game.network_thread.close()
            return
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Player surrendered")
        msg_box.setText("Do You want to play again?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.buttonClicked.connect(self.surrender_button_clicked_answered)
        msg_box.exec_()

    def surrender_button_clicked_answered(self, i):
        if i.text() == "&Yes":
            self.game.end_match()
            self.game.start_match()
        elif i.text() == "&No":
            self.surrender_button.setDisabled(True)
            self.game.end_match()

    def establish_internet_connection(self):
        self.connection_window = ConnectionWindow()
        self.connection_window.got_connection.connect(self.connection_established)
        self.connection_window.exec()

    def connection_established(self):
        self.game.start_multiplayer_match(self.connection_window.network_thread)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())

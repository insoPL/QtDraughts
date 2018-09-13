# -*- coding: utf-8 -*-

import logging
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QWidget, QSizePolicy, QMessageBox

import resources_rc
from game import Game
from mainButton import MainButton
from settings import Settings
from settingsWindow import SettingsWindow
from connectionWindow import ConnectionWindow


class Main(QMainWindow):
    """
    Main Window of program. \n
    Inherits: :class:`PyQt5.QtWidgets.QMainWindow`
    """
    def __init__(self):
        super().__init__()

        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.debug("Initialization...")

        self.settings = Settings()
        self.game = Game(self, self.settings)
        self.init_ui()

        logging.info("Game Ready!")

    def init_ui(self):
        """
        Initialize user interface in Main Window. Intended to use only inside constructor.
        """

        if self.settings.always_on_top:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.setWindowIcon(QIcon(":/graphics/start.png"))
        self.setMinimumSize(300, 300)
        self.setWindowTitle('Draughts')

        # Initialize Toolbar
        self.toolbar = self.addToolBar("Bar")
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(28, 28))

        # Surrender
        self.surrender_button = QAction(QIcon(':/graphics/surrender.png'), 'Surrender', self)
        self.surrender_button.triggered.connect(self.surrender_button_clicked)
        self.surrender_button.setDisabled(True)
        self.toolbar.addAction(self.surrender_button)

        # Multiplayer
        self.multiplayer_button = QAction(QIcon(':/graphics/internet.png'), 'Multiplayer', self)
        self.multiplayer_button.triggered.connect(self.establish_internet_connection)
        self.toolbar.addAction(self.multiplayer_button)

        # Blank Space
        spacer_widget = QWidget(self)
        spacer_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer_widget)

        # Main Button
        self.main_button = MainButton(self)
        self.main_button.triggered.connect(self.main_button_clicked)
        self.toolbar.addAction(self.main_button)

        # Blank Space
        spacer_widget2 = QWidget(self)
        spacer_widget2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer_widget2)

        # Options
        options_act = QAction(QIcon(':/graphics/settings.png'), 'Options', self)
        options_act.setShortcut('Ctrl+O')
        options_act.triggered.connect(self.show_settings_window)
        self.toolbar.addAction(options_act)

        # Exit game
        exit_act = QAction(QIcon(':/graphics/exit.png'), 'Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(qApp.quit)

        self.toolbar.addAction(exit_act)

    # noinspection PyUnusedLocal
    def paintEvent(self, e):
        """
        Overwrites method from :class:`PyQt5.QtWidgets.QMainWindow`
        """
        self.game.update_drawing()

    def show_settings_window(self):
        """
        Shows QWidget with settings window :class:`settingsWindow.SettingsWindow`
        Function called on option_act trigger event.
        """
        self.settings_window = SettingsWindow(self.settings,mp = self.game.multiplayer)
        self.settings_window.show()

    def main_button_clicked(self):
        """
        Starts game.
        Function called on main_button trigger event.
        main_button is in the middle of toolbar.
        """
        if self.game.pieces is None:
            self.game.start_match()

    def surrender_button_clicked(self):
        """
        Shows :class:`QMessageBox` to check if user didn't make misclick.
        Function called on surrender_button trigger event.
        """
        if self.game.multiplayer:
            self.game.connection.send_special_action("surrender")
            self.game.end_match()
            self.game.connection.close()
            return
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Player surrendered")
        msg_box.setText("Do You want to play again?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.buttonClicked.connect(self.surrender_button_clicked_answered)
        msg_box.exec_()

    def surrender_button_clicked_answered(self, i):
        """
        Surrenders the game.
        Function called from msg_box inside :func:`surrender_button_clicked`
        """
        if i.text() == "&Yes":
            self.game.end_match()
            self.game.start_match()
        elif i.text() == "&No":
            self.surrender_button.setDisabled(True)
            self.game.end_match()

    def establish_internet_connection(self):
        """
        Shows QWidget with host/connect options :class:`connectionWindow.ConnectionWindow`
        Function called on multiplayer_button trigger event.
        """
        self.connection_window = ConnectionWindow()
        self.connection_window.got_connection.connect(self.connection_established)
        self.connection_window.exec()

    def connection_established(self):
        """
        Starts multiplayer match and sends settings dump to other side.
        Called after successful connection established in :class:`connectionWindow.ConnectionWindow`
        """
        self.game.start_multiplayer_match(self.connection_window.connection)
        self.connection_window.connection.send_special_action("[settings]"+self.settings.json_dump_for_mp_connection())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QLineEdit, QHBoxLayout, QPushButton, QProgressDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt

from Network import Server, Client

import logging
import socket


class ConnectionWindow(QDialog):
    got_connection = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(QIcon('graphics\internet.png'))
        self.setWindowTitle("Multiplayer")
        self.resize(400, 300)

        grid = QVBoxLayout()
        grid.addLayout(self.client())
        grid.addLayout(self.server())
        grid.addStretch(1)
        self.setLayout(grid)

        self.waiting_window = None
        self.connection = None

    def server(self):
        self.server_ip_address = QLineEdit(socket.gethostbyname(socket.gethostname()))

        self.server_port = QLineEdit("25565")
        self.server_port.setMaximumWidth(80)

        host_button = QPushButton("Host")

        host_button.clicked.connect(self.host_button_clicked)

        hbox = QHBoxLayout()
        hbox.addWidget(self.server_ip_address)
        hbox.addWidget(self.server_port)
        hbox.addWidget(host_button)
        return hbox

    def host_button_clicked(self):
        if self.connection:
            return
        self.connection = Server()

        self.waiting_window = QProgressDialog("Waiting for Network...", "Cancel", 0, 0)
        self.waiting_window.setWindowTitle("Waiting")
        self.waiting_window.setWindowIcon(QIcon('graphics\internet.png'))
        self.waiting_window.setWindowFlags(self.waiting_window.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        self.connection.got_connection.connect(self.waiting_window.deleteLater)
        self.connection.got_connection.connect(self.got_connection)
        self.connection.got_connection.connect(self.deleteLater)

        self.connection.connection_error.connect(self.connection_error)
        self.connection.connection_error.connect(self.waiting_window.deleteLater)

        self.waiting_window.canceled.connect(self.connection.close)

        self.connection.start(self.server_ip_address.text(), self.server_port.text())
        self.waiting_window.exec()

    def client(self):
        self.client_ip_address = QLineEdit(socket.gethostbyname(socket.gethostname()))

        self.client_port = QLineEdit("25565")
        self.client_port.setMaximumWidth(80)

        connect_button = QPushButton("Connect")

        connect_button.clicked.connect(self.connect_button_clicked)

        hbox = QHBoxLayout()
        hbox.addWidget(self.client_ip_address)
        hbox.addWidget(self.client_port)
        hbox.addWidget(connect_button)
        return hbox

    def connect_button_clicked(self):
        if self.connection:
            return
        self.connection = Client()

        self.waiting_window = QProgressDialog("Waiting for server...", "Cancel", 0, 0)
        self.waiting_window.setWindowTitle("Connecting")
        self.waiting_window.setWindowFlags(self.waiting_window.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        self.waiting_window.setWindowIcon(QIcon('graphics\internet.png'))

        self.connection.got_connection.connect(self.waiting_window.close)
        self.connection.got_connection.connect(self.got_connection)
        self.connection.got_connection.connect(self.deleteLater)

        self.connection.connection_error.connect(self.connection_error)
        self.connection.connection_error.connect(self.waiting_window.deleteLater)

        self.connection.start(self.client_ip_address.text(), self.client_port.text())
        self.waiting_window.exec()

    def connection_error(self, err):
        logging.debug(err)
        QMessageBox.warning(self, 'Connection Error', "      Connection Error.      ")

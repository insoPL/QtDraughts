# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QPushButton, QProgressDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal


from network_thread import NetworkThread

import PyQt5.QtCore
import socket


class ConnectionWindow(QWidget):
    got_connection = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('graphics\internet.png'))
        self.setWindowTitle("Multiplayer")
        self.resize(400, 300)

        grid = QVBoxLayout()
        grid.addLayout(self.client())
        grid.addLayout(self.server())
        grid.addStretch(1)
        self.setLayout(grid)

        self.show()

        self.waiting_window = None
        self.network_thread = None

    def server(self):
        self.ip_address = QLineEdit(socket.gethostbyname(socket.gethostname()))

        self.port = QLineEdit("25565")
        self.port.setMaximumWidth(80)

        host_button = QPushButton("Host")

        host_button.clicked.connect(self.host_button_clicked)

        hbox = QHBoxLayout()
        hbox.addWidget(self.ip_address)
        hbox.addWidget(self.port)
        hbox.addWidget(host_button)
        return hbox

    def host_button_clicked(self):
        pass

    def client(self):
        self.ip_address = QLineEdit(socket.gethostbyname(socket.gethostname()))
        #ip_address.setPlaceholderText("192.168.1.1")

        self.port = QLineEdit("25565")
        self.port.setMaximumWidth(80)

        connect_button = QPushButton("Connect")

        connect_button.clicked.connect(self.connect_button_clicked)

        hbox = QHBoxLayout()
        hbox.addWidget(self.ip_address)
        hbox.addWidget(self.port)
        hbox.addWidget(connect_button)
        return hbox

    def connect_button_clicked(self):
        self.waiting_window = QProgressDialog("Waiting for server...", "Cancel", 0, 0)
        self.waiting_window.setWindowTitle("Connecting")
        self.waiting_window.setWindowFlags(PyQt5.QtCore.Qt.WindowSystemMenuHint)
        self.waiting_window.show()

        self.network_thread = NetworkThread(self.ip_address.text(), "client")

        self.network_thread.got_connection.connect(self.waiting_window.close)
        self.network_thread.got_connection.connect(self.got_connection)
        self.network_thread.got_connection.connect(self.close)

        self.network_thread.connection_error.connect(self.connection_error)
        self.network_thread.connection_error.connect(self.waiting_window.close)

        self.network_thread.start()

    def connection_error(self):
        QMessageBox.warning(self, 'Connection Error', "      Connection Error.      ")


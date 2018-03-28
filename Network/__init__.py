# -*- coding: utf-8 -*-

from .connection import Connection
from.network_thread import NetworkThread


class Server(Connection):
    def __init__(self):
        super().__init__()

    def start(self, ip_address, port, passwd="12345"):
        self.passwd = passwd
        self.networkThread = NetworkThread(ip_address, port, "server")
        self.networkThread.got_connection.connect(self.got_connection)
        self.networkThread.connection_error.connect(self.connection_error)
        self.networkThread.new_msg.connect(self._new_msg)
        self.networkThread.start()


class Client(Connection):
    def __init__(self):
        super().__init__()

    def start(self, ip_address, port, passwd="12345"):
        self.passwd = passwd
        self.networkThread = NetworkThread(ip_address, port, "client")
        self.networkThread.got_connection.connect(self.got_connection)
        self.networkThread.connection_error.connect(self.connection_error)
        self.networkThread.new_msg.connect(self._new_msg)
        self.networkThread.start()

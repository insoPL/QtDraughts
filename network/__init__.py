# -*- coding: utf-8 -*-

from .connection import Connection
from.network_thread import NetworkClient, NetworkServer


class Server(Connection):
    def __init__(self):
        super().__init__()

    def start(self, ip_address, port, passwd):
        self.networkThread = NetworkServer(ip_address, port, passwd)
        Connection.start(self, ip_address, port, passwd)
        self.networkThread.start()


class Client(Connection):
    def __init__(self):
        super().__init__()

    def start(self, ip_address, port, passwd):
        self.networkThread = NetworkClient(ip_address, port, passwd)
        Connection.start(self, ip_address, port, passwd)
        self.networkThread.start()

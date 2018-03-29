# -*- coding: utf-8 -*-

import socket
from PyQt5.QtCore import QThread, pyqtSignal
import logging
import nacl.utils
import nacl.secret
import nacl.hash


class _NetworkThread(QThread):
    got_connection = pyqtSignal()
    connection_error = pyqtSignal(str)
    new_msg = pyqtSignal(str)

    def __init__(self, target_ip, port, passwd):
        QThread.__init__(self)
        self.port = int(port)
        self.mode = None
        self.target_ip = target_ip
        self.socket = None
        self.running = True
        self.server_socket = None
        keyhash = nacl.hash.blake2b(passwd.encode('ascii'), digest_size=16)
        self.secret_box = nacl.secret.SecretBox(keyhash)

    def send_raw(self, msg):
        # logging.debug("[raw network pocket send] "+msg)
        msg = self.secret_box.encrypt(msg.encode('ascii'))
        self.socket.send(msg)

    def recive_raw(self):
        msg = self.socket.recv(1024)
        msg = self.secret_box.decrypt(msg)
        msg = msg.decode('ascii')
        # logging.debug("[raw network pocket recived] "+msg)
        return msg

    def __del__(self):
        self.quit()
        self.wait()


class NetworkClient(_NetworkThread):
    def run(self):
        self.mode = "client"
        logging.info("Connecting to :" + str(self.target_ip))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.target_ip, self.port))
            logging.debug("Connection sucessful")

            if self.recive_raw() != "welcome":  self.close()
            self.send_raw("welcomeback")

            self.got_connection.emit()
            self.socket.settimeout(1)
            while self.running:
                try:
                    msg = self.recive_raw()
                    if msg == "":
                        break
                    self.new_msg.emit(msg)
                except socket.timeout:
                    continue
        except socket.error as err:
            logging.debug("SOCKET ERROR: %s" % err)
            self.connection_error.emit(str(err))
            return
        finally:
            self.socket.close()
            logging.debug("Server Closed")


class NetworkServer(_NetworkThread):
    def run(self):
        self.mode = "server"
        logging.info("Hosting :" + str(self.target_ip))

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.bind((self.target_ip, self.port))
            logging.debug("Server ready for network")
            self.server_socket.settimeout(1)
            self.server_socket.listen(1)
            while self.running:
                try:
                    self.socket, clienta_ddr = self.server_socket.accept()
                except socket.timeout:
                    continue
                break
            if not self.running:
                logging.debug("Hosting canceled")
                return
            logging.debug("Connection established.")

            self.send_raw("welcome")
            if self.recive_raw() != "welcomeback": self.close()

            self.got_connection.emit()
            self.socket.settimeout(1)
            while self.running:
                try:
                    msg = self.recive_raw()
                    if msg == "":
                        break
                    self.new_msg.emit(msg)
                except socket.timeout:
                    continue
        except socket.error as err:
            logging.debug("SOCKET ERROR: %s" % err)
            self.server_socket.close()
            self.server_socket = None
            self.connection_error.emit(str(err))
        finally:
            if self.socket is not None:
                self.socket.close()
            if self.server_socket is not None:
                self.server_socket.close()
            logging.debug("Server Closed")

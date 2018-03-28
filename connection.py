# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal, QObject
import logging
import socket


def move_decode(msg):
    list_of_cords = msg.split(' ')
    ret_list = list()
    for cord in list_of_cords:
        x,y = cord.split(",")
        x=int(x)
        y=int(y)
        ret_list.append((x,y))
    return ret_list


class Connection(QObject):
    got_connection = pyqtSignal()
    connection_error = pyqtSignal(str)
    new_move = pyqtSignal(list)
    special_action = pyqtSignal(str)
    close = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.networkThread = None

    def host(self, ip_address, port):
        self.networkThread = _NetworkThread(ip_address, port, "server")
        self.connect_signals()
        self.networkThread.start()

    def connect_to(self, ip_address, port):
        self.networkThread = _NetworkThread(ip_address, port, "client")
        self.connect_signals()
        self.networkThread.start()

    def connect_signals(self):
        self.networkThread.got_connection.connect(self.got_connection)
        self.networkThread.connection_error.connect(self.connection_error)
        self.networkThread.new_msg.connect(self.new_msg)

    def __bool__(self):
        if self.networkThread is None:
            return False
        if not self.networkThread.isRunning():
            return False
        return True

    def new_msg(self, msg):
        msg_type, msg = msg.split(chr(30))
        logging.debug("new message [" + msg_type + "] " + msg)
        if msg_type == "move":
            self.new_move.emit(move_decode(msg))
        elif msg_type == "action":
            self.special_action.emit(msg)

    def send_move(self, piece_cords, dest_cords, *destroyed_pieces):
        piece_cords_str = "%i,%i"%piece_cords
        dest_cords_str = "%i,%i"%dest_cords
        msg = "move" + chr(30) + piece_cords_str+" "+dest_cords_str
        for destroyed_piece in destroyed_pieces:
            msg += " "+"%i,%i"%destroyed_piece
        self.networkThread.socket.send(msg.encode('ascii'))

    def send_special_action(self, string):
        msg = "action" + chr(30) + string
        self.networkThread.socket.send(msg.encode('ascii'))

    def close(self):
        logging.debug("NetworkThread close signal")
        self.networkThread.running = False


class _NetworkThread(QThread):
    got_connection = pyqtSignal()
    connection_error = pyqtSignal(str)
    new_msg = pyqtSignal(str)

    def __init__(self, target_ip, port, mode):
        QThread.__init__(self)
        self.port = int(port)
        self.mode = mode
        self.target_ip = target_ip
        self.socket = None
        self.running = True
        self.server_socket = None

    def __del__(self):
        self.quit()
        self.wait()

    def run(self):
        if self.mode == "client":
            logging.info("Connecting to :" + str(self.target_ip))
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.socket.connect((self.target_ip, self.port))
                logging.debug("Connection sucessful")
                self.got_connection.emit()
                self.socket.settimeout(1)
                while self.running:
                    try:
                        msg = self.socket.recv(1024)
                        msg = msg.decode('ascii')
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

        elif self.mode == "server":
            logging.info("Hosting :" + str(self.target_ip))

            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.server_socket.bind((self.target_ip, self.port))
                logging.debug("Server ready for connection")
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
                logging.debug("Connection sucessful")
                self.got_connection.emit()
                self.socket.settimeout(1)
                while self.running:
                    try:
                        msg = self.socket.recv(1024)
                        msg = msg.decode('ascii')
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


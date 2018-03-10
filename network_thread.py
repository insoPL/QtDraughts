# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal
import logging
import socket


def move_decode(msg):
    home, dest = msg.split(' ')
    homex, homey = home.split(",")
    home = (int(homex), int(homey))
    destx, desty = dest.split(",")
    dest = (int(destx), int(desty))
    return home, dest


class NetworkThread(QThread):
    got_connection = pyqtSignal()
    connection_error = pyqtSignal()
    new_move = pyqtSignal(tuple)

    def __init__(self, target_ip, mode):
        QThread.__init__(self)
        self.mode = mode
        self.target_ip = target_ip
        self.socket = None
        self.running = True

    def __del__(self):
        self.quit()
        self.wait()

    def run(self):
        if self.mode == "client":
            logging.info("Connecting to :" + str(self.target_ip))
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.socket.connect((self.target_ip, 25565))
                logging.debug("Connection sucessful")
                self.got_connection.emit()
                self.socket.settimeout(1)
                while self.running:
                    msg = self.socket.recv(1024)
                    msg = msg.decode('ascii')
                    msg_type, msg = msg.split(chr(30))
                    logging.debug("new message ["+msg_type+"] "+msg)
                    if msg_type == "move":
                        self.new_move.emit(move_decode(msg))
            except socket.error as err:
                logging.debug("SOCKET ERROR: %s" % err)
                self.connection_error.emit()
                return
            finally:
                self.socket.close()
                logging.debug("Server Closed")

        elif self.mode == "server":
            logging.info("Hosting :" + str(self.target_ip))

            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.server_socket.bind((self.target_ip, 25565))
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
                while self.running:
                    try:
                        logging.debug("rcv")
                        msg = self.socket.recv(1024)
                        msg = msg.decode('ascii')
                        msg_type, msg = msg.split(chr(30))
                        logging.debug("new message [" + msg_type + "] " + msg)
                        if msg_type == "move":
                            self.new_move.emit(move_decode(msg))
                    except socket.timeout:
                        continue
            except socket.error as err:
                logging.debug("SOCKET ERROR: %s" % err)
                self.server_socket.close()
                self.server_socket = None
                self.connection_error.emit()
            finally:
                self.socket.close()
                self.server_socket.close()
                logging.debug("Server Closed")

    def send_move(self, piece_cords, dest_cords):
        piece_cords_str = "%i,%i"%piece_cords
        dest_cords_str = "%i,%i"%dest_cords
        msg = "move" + chr(30) + piece_cords_str+" "+dest_cords_str
        self.socket.send(msg.encode('ascii'))

    def close(self):
        logging.debug("cancel signal")
        self.running = False


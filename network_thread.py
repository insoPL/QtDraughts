# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal
import logging
import socket


class NetworkThread(QThread):
    got_connection = pyqtSignal()
    connection_error = pyqtSignal()
    new_move = pyqtSignal(str)

    def __init__(self, target_ip, mode):
        QThread.__init__(self)
        self.mode = mode
        self.taget_ip = target_ip

    def __del__(self):
        self.wait()

    def run(self):
        if self.mode == "client":
            logging.info("Connecting to :"+str(self.taget_ip))
            #self.sleep(1)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((self.taget_ip, 25565))
                logging.debug("Connection sucessful")
                self.got_connection.emit()
                while True:
                    msg = s.recv(1024)
                    msg = msg.decode('ascii')
                    msg_type, msg = msg.split(chr(30))
                    logging.debug("new message ["+msg_type+"] "+msg)
                    if msg_type == "move":
                        self.new_move.emit(msg)

            except socket.error as err:
                logging.debug("SOCKET ERROR: %s" % err)
                self.connection_error.emit()
                return
            finally:
                s.close()

        elif self.mode == "server":
            pass




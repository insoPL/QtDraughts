# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal
import logging
import socket


class NetworkThread(QThread):
    got_connection = pyqtSignal()
    connection_error = pyqtSignal()

    def __init__(self, target_ip, mode):
        QThread.__init__(self)
        self.mode = mode
        self.taget_ip = target_ip
        self.best_move = None

    def __del__(self):
        self.wait()

    def run(self):
        if self.mode == "client":
            logging.debug("Connecting to :"+str(self.taget_ip))
            #self.sleep(1)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((self.taget_ip, 25565))

                msg = s.recv(1024)
            except socket.error as err:
                logging.debug("SOCKET ERROR: %s" % err)
                self.connection_error.emit()
                return
            finally:
                s.close()
            logging.debug(msg.decode('ascii'))
            self.got_connection.emit()

        elif self.mode == "server":
            pass




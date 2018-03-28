# -*- coding: utf-8 -*-
import logging

from PyQt5.QtCore import QObject, pyqtSignal


class Connection(QObject):
    got_connection = pyqtSignal()
    connection_error = pyqtSignal(str)
    new_move = pyqtSignal(list)
    special_action = pyqtSignal(str)
    close = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.networkThread = None
        self.passwd = None

    def start(self):
        pass

    def __bool__(self):
        if self.networkThread is None:
            return False
        if not self.networkThread.isRunning():
            return False
        return True

    def _new_msg(self, msg):
        msg_type, msg = msg.split(chr(30))
        logging.debug("new message [" + msg_type + "] " + msg)
        if msg_type == "move":
            self.new_move.emit(_move_decode(msg))
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

def _move_decode(msg):
    list_of_cords = msg.split(' ')
    ret_list = list()
    for cord in list_of_cords:
        x, y = cord.split(",")
        x = int(x)
        y = int(y)
        ret_list.append((x, y))
    return ret_list


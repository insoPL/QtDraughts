# -*- coding: utf-8 -*-
from tools import *
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import *
import logging
from PyQt5.QtGui import QPainter


class DrawPiece(QFrame):
    def __init__(self, game, cords, color):
        logging.info("Piece %s Constructor at %s", str(color), str(cords))
        self.game = game
        self.board = game.board
        self.__cords = cords
        self.color = color
        QFrame.__init__(self, game.screen)
        self.dragging = False

    @property
    def cords(self):
        return self.__cords

    @cords.setter
    def cords(self, new_cords):
        self.__cords = new_cords
        self.paintEvent(None)

    @property
    def size_of_piece(self):
        return self.board.size_of_one_tile

    def paintEvent(self, e):
        logging.debug("PaintEvent inside piece")
        self.resize(self.size_of_piece, self.size_of_piece)
        pen = QPen()
        pen.setWidth(4)
        if self.color == Color.white:
            pen.setColor(Qt.lightGray)
        qp = QPainter()
        qp.setRenderHint(QPainter.HighQualityAntialiasing)
        qp.begin(self)
        qp.setPen(pen)
        qp.drawEllipse(5, 5, self.size_of_piece-10, self.size_of_piece-10)
        qp.end()
        if self.dragging is False:
            to = self.board.cords_to_pos(self.cords)
            self.move(*to)

    def mousePressEvent(self, e):
        logging.info("click")
        if self.cords in self.game.list_of_pieces_which_can_move_or_attack():
            self.offset = e.pos()
            self.dragging = True

    def mouseReleaseEvent(self, e):
        if self.dragging:
            self.dragging = False
            glob_pos = e.globalPos()
            pos = self.board.mapFromGlobal(glob_pos)
            dest_cords = self.board.pos_to_cords(pos)
            logging.info("Trying to place "+str(self.cords)+" pieces on "+str(dest_cords))
            self.game.try_to_make_a_move(self, dest_cords)
            self.paintEvent(None)

    def mouseMoveEvent(self, e):
        if self.dragging:
            self.move(self.mapToParent(e.pos()-self.offset))

    def __reduce__(self):
        QFrame.__reduce__()

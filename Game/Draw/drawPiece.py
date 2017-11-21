# -*- coding: utf-8 -*-
from tools import *
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import *
import logging
from PyQt5.QtGui import QPainter


class DrawPiece(QFrame):
    def __init__(self, board, cords, color):
        logging.info("Piece Constructor at " + str(cords))
        self.board = board
        QFrame.__init__(self, board.drawnBoard.screen)

    @property
    def size_of_piece(self):
        return self.board.size_of_one_tile

    def paintEvent(self, e):
        logging.debug("PaintEvent inside piece")
        self.resize(self.size_of_piece, self.size_of_piece)
        pen = QPen()
        pen.setWidth(4)
        qp = QPainter()
        qp.setRenderHint(QPainter.HighQualityAntialiasing)
        qp.begin(self)
        qp.setPen(pen)
        qp.drawEllipse(5, 5, self.size_of_piece-10,self.size_of_piece-10)
        qp.end()

    def mousePressEvent(self, e):
        logging.info("you clicked "+str(self.board.pos_to_cords(e.pos())))
        self.offset = e.pos()

    def mouseMoveEvent(self, e):
        self.move(self.mapToParent(e.pos()-self.offset))



# -*- coding: utf-8 -*-
from tools import *
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import *
import logging
from PyQt5.QtGui import QPainter
from .game_logic import mozliwe_ruchy_i_bicia


class DrawPiece(QFrame):
    def __init__(self, board, cords, color):
        logging.info("Piece Constructor at " + str(cords))
        self.board = board
        self.cords = cords
        self.color = color
        QFrame.__init__(self, board.drawnBoard.screen)
        self.dragging = False

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
        qp.drawEllipse(5, 5, self.size_of_piece-10, self.size_of_piece-10)
        qp.end()
        if self.dragging is False:
            to = self.board.cords_to_pos(self.cords)
            self.move(*to)

    def mousePressEvent(self, e):
        self.offset = e.pos()
        self.dragging = True

    def mouseReleaseEvent(self, e):
        self.dragging = False
        dest_cords = self.board.global_pos_to_cords(e.globalPos())
        logging.info("Trying to place "+str(self.cords)+" piece on "+str(dest_cords))
        mrib = mozliwe_ruchy_i_bicia(self.cords, self.color, *self.board.piece.two_lists)
        for foo in mrib.keys():
            if foo == dest_cords:
                self.paintEvent(None)
                self.cords = dest_cords
                if mrib[foo] != 0:
                    logging.info("bij")
        self.paintEvent(None)

    def mouseMoveEvent(self, e):
        self.move(self.mapToParent(e.pos()-self.offset))

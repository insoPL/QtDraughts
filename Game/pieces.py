# -*- coding: utf-8 -*-
from .Draw.drawPiece import DrawPiece
from tools import *
import logging


class Pieces:
    def __init__(self, board):
        logging.info("Pieces constructor")
        self.board = board
        self._pieces_list = list()
        for foo in range(0, 8, 2):
            self.add_piece((foo+1, 7), Color.black)
            self.add_piece((foo, 6), Color.black)
            self.add_piece((foo+1, 5), Color.black)

            self.add_piece((foo, 2), Color.white)
            self.add_piece((foo+1, 1), Color.white)
            self.add_piece((foo, 0), Color.white)

    def add_piece(self, cords, color):
        self._pieces_list.append(DrawPiece(self.board, cords, color))

    def remove_piece(self, cords):
        piece = self.get_piece(cords)
        self._pieces_list.remove(piece)
        del piece

    def get_piece(self, cords):  # --> Piece
        for foo in self._pieces_list:
            if foo.cords == cords:
                return foo
        raise ValueError
        return False

    @property
    def two_lists(self):
        white = list()
        black = list()
        for foo in self._pieces_list:
            if foo.color == Color.black:
                black.append(foo.cords)
            if foo.color == Color.white:
                white.append(foo.cords)
        return white, black

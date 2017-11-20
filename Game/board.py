# -*- coding: utf-8 -*-
from .Draw.drawBoard import DrawBoard
from .piece import Piece


class Board:
    def __init__(self, screen):
        self.drawnBoard = DrawBoard(screen)
        self.piece = Piece(screen, self.size_of_one_tile)

    def redraw(self):
        self.drawnBoard.draw_board()
        self.piece.setSize(self.size_of_one_tile)

    @property
    def size_of_one_tile(self):
        return self.drawnBoard.size_of_one_tile

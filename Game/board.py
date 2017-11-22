# -*- coding: utf-8 -*-
from .Draw.drawBoard import DrawBoard
from .pieces import Pieces
import logging


class Board:
    def __init__(self, screen):
        logging.info("Board constructor")
        self.drawnBoard = DrawBoard(screen)
        self.piece = Pieces(self)

    def redraw(self):
        self.drawnBoard.draw_board()

    def global_pos_to_cords(self, pos):
        return self.drawnBoard.global_pos_to_cords(pos)

    def cords_to_pos(self, cords):
        return self.drawnBoard.global_pos_to_cords(cords)

    @property
    def size_of_one_tile(self):
        return self.drawnBoard.size_of_one_tile

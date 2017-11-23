# -*- coding: utf-8 -*-
import logging

from Game.drawBoard import DrawBoard
from .pieces import Pieces


class Board:
    def __init__(self, screen):
        logging.info("Board constructor")
        self.drawnBoard = DrawBoard(screen)
        self.piece = Pieces(self)

    def redraw(self):
        self.drawnBoard.draw_board()

    def global_pos_to_cords(self, global_pos):
        pos = self.drawnBoard.mapFromGlobal(global_pos)
        return self.drawnBoard.pos_to_cords(pos)

    def cords_to_pos(self, cords):
        return self.drawnBoard.cords_to_pos(cords)

    @property
    def size_of_one_tile(self):
        return self.drawnBoard.size_of_one_tile
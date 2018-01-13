# -*- coding: utf-8 -*-
import logging

from .board import Board
from .pieces import Pieces
from .game_logic import mozliwe_ruchy_i_bicia


class Game:
    def __init__(self, screen):
        logging.info("Game constructor")
        self.screen = screen
        self.board = Board(screen)
        self.pieces = Pieces(self)

    def move_piece(self, piece, cords):
        mrib = mozliwe_ruchy_i_bicia(piece.cords, piece.color, *self.pieces.two_lists)
        for foo in mrib.keys():
            if foo == cords:
                piece.cords = cords
                if mrib[foo] != 0:
                    logging.info("bij " + str(mrib[foo]))
                    self.pieces.remove_piece(mrib[foo])

    def update_drawing(self):
        self.board.redraw()

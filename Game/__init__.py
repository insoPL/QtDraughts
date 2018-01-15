# -*- coding: utf-8 -*-
import logging

from .board import Board
from .pieces import Pieces
from .game_logic import mozliwe_ruchy_i_bicia
from tools import Color
from .settings import Settings

class Game:
    def __init__(self, screen):
        logging.info("Game constructor")
        self.settings = Settings()
        self.screen = screen
        self.board = Board(screen)
        self.pieces = Pieces(self)
        self.whoseTurn = self.settings.who_starts

    def try_to_make_a_move(self, piece, dest_cords):
        if piece.color == self.whoseTurn:
            if self.can_i_attack():
                possible_attacks = game_logic.mozliwe_bicia(piece.cords, piece.color, *self.pieces.two_lists)
                for possible_dest_cord, possible_destroyed_piece in possible_attacks.items():
                    if possible_dest_cord == dest_cords:
                        self.pieces.remove_piece(possible_destroyed_piece)
                        piece.cords = dest_cords
                        self.whoseTurn = Color.opposite(self.whoseTurn)
                if self.settings.force_attack:
                    return
            mrib = game_logic.mozliwe_ruchy(piece.cords, piece.color, *self.pieces.two_lists)
            for foo in mrib.keys():
                if foo == dest_cords:
                    piece.cords = dest_cords
                    if mrib[foo] != 0:
                        self.pieces.remove_piece(mrib[foo])
                    self.whoseTurn = Color.opposite(self.whoseTurn)

    def can_i_attack(self):
        for piece in self.pieces:
            if piece.color == self.whoseTurn:
                possible_attacks = game_logic.mozliwe_bicia(piece.cords, piece.color, *self.pieces.two_lists)
                for attack in possible_attacks.values():
                    return True
        return False

    def update_drawing(self):
        self.board.redraw()

# -*- coding: utf-8 -*-
from game.drawPiece import DrawPiece
from tools import Color
from game.gameLogic.listOfPieces import ListOfPieces
from game.gameLogic.move import Move
import logging


class Pieces:
    def __init__(self, game):
        logging.debug("Pieces constructor")
        self.game = game
        self._pieces_list = list()
        on_top = Color.white
        for foo in range(0, 8, 2):
            self.add_piece((foo + 1, 7), on_top)
            self.add_piece((foo, 6), on_top)
            self.add_piece((foo + 1, 5), on_top)

            self.add_piece((foo, 2), Color.opposite(on_top))
            self.add_piece((foo + 1, 1), Color.opposite(on_top))
            self.add_piece((foo, 0), Color.opposite(on_top))

    def __del__(self):
        for piece in self:
            piece.setParent(None)
            piece.destroy()
            del piece

    def __iter__(self):
        return self._pieces_list.__iter__()

    def add_piece(self, cords, color):
        self._pieces_list.append(DrawPiece(self.game, cords, color))

    def remove_piece(self, cords):
        if cords is tuple():
            return
        piece = self.get_piece(cords)
        self._pieces_list.remove(piece)
        piece.setParent(None)
        piece.destroy()
        del piece

    def get_piece(self, cords):  # -> Piece
        for foo in self._pieces_list:
            if foo.cords == cords:
                return foo
        raise ValueError

    def apply_move(self, move):
        piece = self.get_piece(move.cords)
        piece.cords = move.dest
        self.remove_piece(move.destroyed)

    @property
    def two_lists(self) -> (list, list):
        """:return two lists of cords of pieces. First list is list of pieces on top of the board"""
        white = list()
        black = list()
        for foo in self._pieces_list:
            if foo.color == Color.black:
                black.append(foo.cords)
            if foo.color == Color.white:
                white.append(foo.cords)
        return white, black

    @property
    def list_of_pieces(self) -> ListOfPieces:
        """:return two lists of cords of pieces. First list is list of pieces on top of the board"""
        white = list()
        black = list()
        for foo in self._pieces_list:
            if foo.color == Color.black:
                black.append(foo.cords)
            if foo.color == Color.white:
                white.append(foo.cords)
        return ListOfPieces(white,black)

# -*- coding: utf-8 -*-
import logging

from Game.Draw import drawBoard
from .piece import Piece


class Game:
    def __init__(self,screen):
        logging.debug("init Game...")
        self.draw = drawBoard.DrawBoard(screen)
        self.piece = Piece(screen, self.draw.size_of_one_tile)
        logging.debug("init Game complete")

    def updateDrawing(self):
        self.draw.redraw()
        self.piece.setSize(self.draw.size_of_one_tile)



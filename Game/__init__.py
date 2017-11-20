# -*- coding: utf-8 -*-
import logging

from .board import Board
from .piece import Piece


class Game:
    def __init__(self,screen):
        logging.debug("init Game...")
        self.draw = Board(screen)
        logging.debug("init Game complete")

    def update_drawing(self):
        self.draw.redraw()



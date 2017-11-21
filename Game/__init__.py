# -*- coding: utf-8 -*-
import logging

from .board import Board
from .pieces import Pieces


class Game:
    def __init__(self,screen):
        logging.info("Game constructor")
        self.board = Board(screen)

    def update_drawing(self):
        self.board.redraw()



# -*- coding: utf-8 -*-
import logging

from Game.Draw import Draw


class Game:
    def __init__(self,screen):
        logging.debug("init Game...")
        self.draw = Draw(screen)

        logging.debug("init Game complete")

    def updateDrawing(self):
        self.draw.redraw()



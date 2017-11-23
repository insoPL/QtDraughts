# -*- coding: utf-8 -*-
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import Qt
import logging
from .pieces import Pieces


class Board:
    def __init__(self,screen):
        logging.info("Board constructor")
        self.toolbar_margines = 35
        self.screen = screen
        self.redraw()
        self.pieces = Pieces(self)

    @property
    def size_of_one_tile(self):
        height = self.screen.height()-10
        width = self.screen.width()-self.toolbar_margines-10
        height -= 25  # correction for toolbar
        if height < width:
            height = height
            return round(height/8)
        else:
            width = width
            return round(width/8)

    @property
    def height_margines(self):
        return ((self.screen.height()-self.toolbar_margines)/2)-(4*self.size_of_one_tile)

    @property
    def width_margines(self):
        return (self.screen.width() / 2) - (4 * self.size_of_one_tile)

    def pos_to_cords(self, pos):
        x = pos.x()
        y = pos.y()
        x -= self.width_margines
        x /= self.size_of_one_tile
        y -= self.height_margines
        y -= self.toolbar_margines
        y /= self.size_of_one_tile
        return int(x), int(y)

    def cords_to_pos(self, cords):
        x, y = cords
        x = self.width_margines + x * self.size_of_one_tile
        y = self.toolbar_margines + self.height_margines + y * self.size_of_one_tile
        return x, y

    def mapFromGlobal(self, glob_pos):
        return self.screen.mapFromGlobal(glob_pos)

    def redraw(self):
        tile_size = self.size_of_one_tile
        qp = QPainter()
        qp.begin(self.screen)
        color = False
        for foo in range(8):
            for bar in range(8):
                if color:
                    qp.setBrush(Qt.gray)
                else:
                    qp.setBrush(Qt.transparent)
                color = not color
                qp.setPen(Qt.black)
                qp.drawRect(*self.cords_to_pos((foo, bar)), tile_size, tile_size)
            color = not color
        qp.end()
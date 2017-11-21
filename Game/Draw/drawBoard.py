# -*- coding: utf-8 -*-
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import Qt
import logging


class DrawBoard:
    def __init__(self,screen):
        logging.debug("init Draw")
        self.toolbar_margines = 35
        self.screen = screen
        self.draw_board()
        logging.debug("init DrawBoard complete")

    @property
    def size_of_one_tile(self):
        height = self.screen.height()-10
        width = self.screen.width()-self.toolbar_margines-10
        height -= 25  # correction for toolbar
        if height < width:
            height = height
            return height/8
        else:
            width = width
            return width/8

    @property
    def anchor_point(self):
        x = (self.screen.width() / 2) - (4 * self.size_of_one_tile)
        y = ((self.screen.height()-self.toolbar_margines)/2)-(4*self.size_of_one_tile)
        return x, y

    def draw_board(self):
        tile_size = self.size_of_one_tile
        width_margines, height_margines = self.anchor_point
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
                qp.drawRect(width_margines + bar * tile_size,
                            self.toolbar_margines + height_margines + foo * tile_size,
                            tile_size,
                            tile_size)
            color = not color
        qp.end()

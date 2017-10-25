# -*- coding: utf-8 -*-
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import Qt
import logging


class Draw:
    def __init__(self,screen):
        logging.debug("init Draw")
        self.screen = screen
        self.margines = 30
        logging.debug("init Draw complete")

    @property
    def size_of_one_tile(self):
        height = self.screen.height()
        width = self.screen.width()
        height -= 25  # correction for toolbar
        if height < width:
            height = height - self.margines*2
            return height/8
        else:
            width = width - self.margines*2
            return width/8

    def draw_board(self):
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
                qp.drawRect(self.margines + bar * tile_size, self.margines + foo * tile_size + 25, tile_size,
                            tile_size)
            color = not color
        qp.end()

    def redraw(self):
        self.draw_board()


# -*- coding: utf-8 -*-
from .Draw.drawPiece import DrawPiece


class Piece(DrawPiece):
    def __init__(self, screen, size_of_one_tile, anchor_point):
        DrawPiece.__init__(self, screen, size_of_one_tile)
        self.anchor_point = anchor_point

    def set_anchor_point(self, anchor_point):
        self.anchor_point = anchor_point

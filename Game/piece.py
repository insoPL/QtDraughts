# -*- coding: utf-8 -*-
from .Draw.drawPiece import DrawPiece


class Piece(DrawPiece):
    def __init__(self,screen,size_of_one_tile):
        DrawPiece.__init__(self,screen,size_of_one_tile)

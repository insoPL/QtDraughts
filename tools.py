# -*- coding: utf-8 -*-


class Color:
    black = 0
    white = 1

    @staticmethod
    def to_str(color):
        if color == Color.white:
            return "white"
        elif color == Color.black:
            return "black"
        else:
            raise ValueError(str(color))

    @staticmethod
    def opposite(color):
        if color == Color.white:
            return Color.black
        elif color == Color.black:
            return Color.white
        else:
            raise ValueError(str(color))


class NoPossibleMove(Exception):
    def __init__(self, who_win):
        self.who_win = who_win

    def __str__(self):
        return "No More Possible Moves Winner is:" + str(self.who_win)

# -*- coding: utf-8 -*-


class Color:
    """
    Static Enum class used form marking colors of pieces

    In main program values are stored as int. This class is used only as static enum class to make code cleaner and
    to avoid magic numbers.
    """
    black = 0
    white = 1

    @staticmethod
    def to_str(color):
        """
        Changes color to readable string

        :param int color: value representing color
        :return: name of color
        :rtype: str
        """
        if color == Color.white:
            return "white"
        elif color == Color.black:
            return "black"
        else:
            raise ValueError(str(color))

    @staticmethod
    def opposite(color):
        """
        Returns opposite color.

        :param int color: value representing color
        :return: opposite color
        :rtype: int
        """
        if color == Color.white:
            return Color.black
        elif color == Color.black:
            return Color.white
        else:
            raise ValueError(str(color))

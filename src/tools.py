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


def cords_list_to_str(list_of_white_pieces: list, list_of_black_pieces: list):
    """
    Creates nice looking string to visalize list of cords on the board,
    usefull for debugging and tests

    :param list list_of_white_pieces: list of cords of white pieces
    :param list list_of_black_pieces: list of cords of black pieces
    :return: str_board
    :rtype: str
    """

    empty_board = [
         '+---------------+',
         '| | | | | | | | |',
         '|-+-+-+-+-+-+-+-+',
         '| | | | | | | | |',
         '|-+-+-+-+-+-+-+-+',
         '| | | | | | | | |',
         '|-+-+-+-+-+-+-+-+',
         '| | | | | | | | |',
         '|-+-+-+-+-+-+-+-+',
         '| | | | | | | | |',
         '|-+-+-+-+-+-+-+-+',
         '| | | | | | | | |',
         '|-+-+-+-+-+-+-+-+',
         '| | | | | | | | |',
         '|-+-+-+-+-+-+-+-+',
         '| | | | | | | | |',
         '+---------------+']

    list_of_pieces = list_of_black_pieces + list_of_white_pieces

    for cord in list_of_pieces:
        x, y = cord

        x = x*2
        x = 15-x

        y = y*2
        y = y+1

        line = empty_board[x]
        line = list(line)

        if cord in list_of_white_pieces:
            line[y] = 'w'
        elif cord in list_of_black_pieces:
            line[y] = 'b'

        line = "".join(line)
        empty_board[x] = line

    return '\n'.join(empty_board)


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

        y = y*2
        y = 15-y

        x = x*2
        x = x+1

        line = empty_board[y]
        line = list(line)

        if cord in list_of_white_pieces:
            line[x] = 'w'
        elif cord in list_of_black_pieces:
            line[x] = 'b'

        line = "".join(line)
        empty_board[y] = line

    return '\n'.join(empty_board)


def str_to_cords(str_board: str):
    """
    Creates list od cords out of string visual representation.
    Does opposite of :func:`cords_list_to_str`

    :param str str_board: string with visual representation of board
    :return two lists of pieces
    :rtype: tuple
    """

    list_of_white_pieces = list()
    list_of_black_pieces = list()

    str_board = str_board.split("\n")
    for y in range(16):
        if y % 2 == 0:
            continue
        line = str_board[y]

        y-=1
        y/=2
        y-=7
        y = int(y)
        y=abs(y)

        line = list(line)

        def remove_letter(letter):
            ret_list = list()
            while letter in line:
                index = line.index(letter)
                line[index] = ' '

                index-=1
                index/=2
                index = int(index)

                ret_list.append((index,y))
            return ret_list

        list_of_black_pieces.extend(remove_letter('b'))
        list_of_white_pieces.extend(remove_letter('w'))

    return list_of_white_pieces, list_of_black_pieces

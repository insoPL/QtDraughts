from .move import Move


class ListOfPieces:
    """
    New class intended to replace old way of storing info about pieces
    Old way of storing was a tuple two_pieces - (black_pieces, white_pieces)
    where:
        white_pieces - list of cords of white pieces
        black_pieces - list of cords of black pieces
    """
    def __init__(self, white_pieces: list, black_pieces: list):
        assert isinstance(white_pieces, list)
        assert isinstance(black_pieces, list)

        self.white_pieces = set(white_pieces)
        self.black_pieces = set(black_pieces)

    def __iter__(self):
        combined = self.black_pieces | self.white_pieces
        return iter(combined)

    def apply_move(self, move: Move):
        """
        Applies Move to ListOfPieces.
        Works in place

        :param move move: move to be applied
        """
        if move.cords in self.black_pieces:
            self.black_pieces.remove(move.cords)
            self.black_pieces.add(move.dest)
        elif move.cords in self.white_pieces:
            self.white_pieces.remove(move.cords)
            self.white_pieces.add(move.dest)

        for destroyed_piece in move.destroyed:
            self.remove_piece(destroyed_piece)
        return self

    def remove_piece(self, cords):
        if cords in self.white_pieces:
            self.white_pieces.remove(cords)
        elif cords in self.black_pieces:
            self.black_pieces.remove(cords)

    def __len__(self):
        return len(self.black_pieces)+len(self.white_pieces)

    def __eq__(self, other):
        if isinstance(other, ListOfPieces):
            return self.black_pieces == other.black_pieces and self.white_pieces == other.white_pieces

    def cords_list_to_str(self):
        """
        Creates nice looking string to visualize pieces on the board,
        useful for debugging and tests

        :return str: str_board
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

        for cord in self:
            x, y = cord

            y = y * 2
            y = 15 - y

            x = x * 2
            x = x + 1

            line = empty_board[y]
            line = list(line)

            if cord in self.white_pieces:
                line[x] = 'w'
            elif cord in self.black_pieces:
                line[x] = 'b'

            line = "".join(line)
            empty_board[y] = line

        return empty_board


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
        line = line.lstrip()

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

    return ListOfPieces(list_of_white_pieces, list_of_black_pieces)

class Move:
    """
    New class intended to replace old way of storing 'move' data
    Old way of storing 'move' was a tuple - (cords, dest, destroyed)
    where:
        cords - cords of moving piece
        dest - destination cords
        destroyed - list of cords of destroyed pieces
    """
    def __init__(self, cords: tuple, dest: tuple, destroy: tuple):
        assert isinstance(cords, tuple)
        assert isinstance(dest, tuple)
        assert isinstance(destroy, tuple)
        self.cords = cords
        self.dest = dest
        self.destroyed = destroy


def new_move(move):
    """
    Temporary function helping in transition from old to new Move standard
    (tuple to class)
    :return: ListofPieces:
    """
    assert isinstance(move, tuple)
    if move is None:
        move = (tuple(), tuple(), list())
    ret_move = Move(*move)  # force change old format to new
    return ret_move

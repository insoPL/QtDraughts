from tools import *


def pytest_assertrepr_compare(config, op, left, right):
    if isinstance(left, ListOfPieces) \
        and isinstance(right, ListOfPieces) \
            and op == '==':
        ai_board = left.cords_list_to_str()
        asserted_board = right.cords_list_to_str()
        two_boards = []
        for x in range(len(ai_board)):
            two_boards.append(ai_board[x]+"   "+asserted_board[x])
        return [
            '-------Testing boards----------',
            '    ai board:        asserted board:',
            *two_boards
        ]

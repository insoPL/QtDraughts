from .listOfPieces import ListOfPieces
from tools import Color
from .move import Move


def find_all_possible_moves(list_of_pieces, color, settings):
    all_possible_moves = list()

    if color == Color.black:
        list_of_my_pieces = list(list_of_pieces.black_pieces)
    elif color == Color.white:
        list_of_my_pieces = list(list_of_pieces.white_pieces)
    else:
        raise ValueError("Color: " + str(color))

    for foo in list_of_my_pieces:
        possible_attack_moves = possible_attacks(foo, list_of_pieces)
        all_possible_moves.extend(possible_attack_moves)
    if not all_possible_moves or not settings.force_attack:
        for foo in list_of_my_pieces:
            possible_moves = _possible_moves(foo, list_of_pieces)
            all_possible_moves.extend(possible_moves)
    return all_possible_moves


def _possible_moves(cords, list_of_pieces):
    return_list = list()
    if cords in list_of_pieces.white_pieces:
        if (cords[0] - 1, cords[1] + 1) not in list_of_pieces:
            if cords[0]-1 >= 0 and cords[1]+1 <= 7:
                move = Move(cords, (cords[0] - 1, cords[1] + 1), tuple())
                return_list.append(move)

        if (cords[0] + 1, cords[1] + 1) not in list_of_pieces:
            if cords[0]+1 <= 7 and cords[1]+1 <= 7:
                move = Move(cords, (cords[0] + 1, cords[1] + 1), tuple())
                return_list.append(move)
        return return_list
    elif cords in list_of_pieces.black_pieces:
        if (cords[0] - 1, cords[1] - 1) not in list_of_pieces:
            if cords[0]-1 >= 0 and cords[1]-1 >= 0:
                move = Move(cords, (cords[0] - 1, cords[1] - 1), tuple())
                return_list.append(move)

        if (cords[0] + 1, cords[1] - 1) not in list_of_pieces:
            if cords[0]+1 <= 7 and cords[1]-1 >= 0:
                move = Move(cords, (cords[0] + 1, cords[1] - 1), tuple())
                return_list.append(move)
        return return_list
    raise ValueError("cords not listed on list_of_pieces")


def possible_attacks(cords, list_of_pieces):
    cordy_pionka = cords
    if cordy_pionka in list_of_pieces.black_pieces:
        przeciwnik = list_of_pieces.white_pieces
    else:
        przeciwnik = list_of_pieces.black_pieces

    return_list = list()
    if (cordy_pionka[0] - 1, cordy_pionka[1] + 1) in przeciwnik and (cordy_pionka[0] - 2, cordy_pionka[1] + 2) not in list_of_pieces:
        if cordy_pionka[0] - 2 >= 0 and cordy_pionka[1] + 2 <= 7:
            return_list.append(Move(cords, (cordy_pionka[0] - 2, cordy_pionka[1] + 2), (cordy_pionka[0] - 1, cordy_pionka[1] + 1)))

    if (cordy_pionka[0] + 1, cordy_pionka[1] + 1) in przeciwnik and (cordy_pionka[0] + 2, cordy_pionka[1] + 2) not in list_of_pieces:
        if cordy_pionka[0] + 2 <= 7 and cordy_pionka[1] + 2 <= 7:
            return_list.append(Move(cords, (cordy_pionka[0] + 2, cordy_pionka[1] + 2), (cordy_pionka[0] + 1, cordy_pionka[1] + 1)))

    if (cordy_pionka[0] + 1, cordy_pionka[1] - 1) in przeciwnik and (cordy_pionka[0] + 2, cordy_pionka[1] - 2) not in list_of_pieces:
        if cordy_pionka[0] + 2 <= 7 and cordy_pionka[1]-2 >= 0:
            return_list.append(Move(cords, (cordy_pionka[0] + 2, cordy_pionka[1] - 2), (cordy_pionka[0] + 1, cordy_pionka[1] - 1)))

    if (cordy_pionka[0] - 1, cordy_pionka[1] - 1) in przeciwnik and (cordy_pionka[0] - 2, cordy_pionka[1] - 2) not in list_of_pieces:
        if cordy_pionka[0] - 2 >= 0 and cordy_pionka[1] - 2 >= 0:
            return_list.append(Move(cords, (cordy_pionka[0] - 2, cordy_pionka[1] - 2), (cordy_pionka[0] - 1, cordy_pionka[1] - 1)))
    return return_list

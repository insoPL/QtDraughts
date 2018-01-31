# -*- coding: utf-8 -*-


def mozliwe_ruchy_i_bicia(cords, color, cord_list_of_bottom_pieces, cord_list_of_top_pieces):  # zwraca słownik dict[docelowy_cord] = zbity_pion
    return_dict = possible_moves(cords, cord_list_of_bottom_pieces, cord_list_of_top_pieces)
    return_dict.update(possible_attacks(cords, color, cord_list_of_bottom_pieces, cord_list_of_top_pieces))
    return return_dict


def possible_moves(cordy_pionka, cord_list_of_bottom_pieces, cord_list_of_top_pieces):
    return_dict = dict()
    if cordy_pionka in cord_list_of_bottom_pieces:
        if (cordy_pionka[0]-1, cordy_pionka[1]+1) not in cord_list_of_top_pieces + cord_list_of_bottom_pieces:
            if cordy_pionka[0]-1 >= 0 and cordy_pionka[1]+1 <= 7:
                return_dict[(cordy_pionka[0] - 1, cordy_pionka[1] + 1)] = 0

        if (cordy_pionka[0]+1, cordy_pionka[1]+1) not in cord_list_of_top_pieces + cord_list_of_bottom_pieces:
            if cordy_pionka[0]+1 <= 7 and cordy_pionka[1]+1 <= 7:
                return_dict[(cordy_pionka[0] + 1, cordy_pionka[1] + 1)] = 0

    else:
        if (cordy_pionka[0]-1, cordy_pionka[1]-1) not in cord_list_of_top_pieces + cord_list_of_bottom_pieces:
            if cordy_pionka[0]-1 >= 0 and cordy_pionka[1]-1 >= 0:
                return_dict[(cordy_pionka[0] - 1, cordy_pionka[1] - 1)] = 0

        if (cordy_pionka[0]+1, cordy_pionka[1]-1) not in cord_list_of_top_pieces + cord_list_of_bottom_pieces:
            if cordy_pionka[0]+1 <= 7 and cordy_pionka[1]-1 >= 0:
                return_dict[(cordy_pionka[0] + 1, cordy_pionka[1] - 1)] = 0
    return return_dict


def possible_attacks(cordy_pionka, cord_list_of_bottom_pieces, cord_list_of_top_pieces):
    if cordy_pionka in cord_list_of_bottom_pieces:
        przeciwnik = cord_list_of_top_pieces
    else:
        przeciwnik = cord_list_of_bottom_pieces

    wszystkie = cord_list_of_bottom_pieces + cord_list_of_top_pieces
    return_dict = dict()
    if (cordy_pionka[0] - 1, cordy_pionka[1] + 1) in przeciwnik and (cordy_pionka[0] - 2, cordy_pionka[1] + 2) not in wszystkie:
        if cordy_pionka[0] - 2 >= 0 and cordy_pionka[1] + 2 <= 7:
            return_dict[(cordy_pionka[0] - 2, cordy_pionka[1] + 2)] = (cordy_pionka[0] - 1, cordy_pionka[1] + 1)

    if (cordy_pionka[0] + 1, cordy_pionka[1] + 1) in przeciwnik and (cordy_pionka[0] + 2, cordy_pionka[1] + 2) not in wszystkie:
        if cordy_pionka[0] + 2 <= 7 and cordy_pionka[1] + 2 <= 7:
            return_dict[(cordy_pionka[0] + 2, cordy_pionka[1] + 2)] = (cordy_pionka[0] + 1, cordy_pionka[1] + 1)

    if (cordy_pionka[0] + 1, cordy_pionka[1] - 1) in przeciwnik and (cordy_pionka[0] + 2, cordy_pionka[1] - 2) not in wszystkie:
        if cordy_pionka[0] + 2 <= 7 and cordy_pionka[1]-2 >= 0:
            return_dict[(cordy_pionka[0] + 2, cordy_pionka[1] - 2)] = (cordy_pionka[0] + 1, cordy_pionka[1] - 1)

    if (cordy_pionka[0] - 1, cordy_pionka[1] - 1) in przeciwnik and (cordy_pionka[0] - 2, cordy_pionka[1] - 2) not in wszystkie:
        if cordy_pionka[0] - 2 >= 0 and cordy_pionka[1] - 2 >= 0:
            return_dict[(cordy_pionka[0] - 2, cordy_pionka[1] - 2)] = (cordy_pionka[0] - 1, cordy_pionka[1] - 1)
    return return_dict

# -*- coding: utf-8 -*-
from tools import Color, ListOfPieces
from game.game_logic import possible_moves, possible_attacks
import random
import math


def find_all_possible_moves(list_of_white_pieces, list_of_black_pieces, color, settings):
    all_possible_moves = list()

    list_of_pieces = ListOfPieces(list_of_white_pieces, list_of_black_pieces)

    if color == Color.black:
        list_of_my_pieces = list(list_of_pieces.black_pieces)
    elif color == Color.white:
        list_of_my_pieces = list(list_of_pieces.white_pieces)
    else:
        raise ValueError("Color: " + str(color))
    list_of_white_pieces = list(list_of_pieces.white_pieces)
    list_of_black_pieces = list(list_of_pieces.black_pieces)

    for foo in list_of_my_pieces:
        possible_moves_foo = possible_attacks(foo, list_of_white_pieces, list_of_black_pieces)
        for move in possible_moves_foo.items():
            all_possible_moves.append((foo, move[0], move[1]))
    if not all_possible_moves or not settings.force_attack:
        for foo in list_of_my_pieces:
            possible_moves_foo = possible_moves(foo, list_of_white_pieces, list_of_black_pieces)
            for move in possible_moves_foo.items():
                all_possible_moves.append((foo, move[0], move[1]))
    return all_possible_moves


def the_best_move(all_possible_moves):
    maxim = -math.inf
    for piece_cords, target_cords, number_of_beaten_pieces, cords_of_beaten_pieces in all_possible_moves:
        if maxim < number_of_beaten_pieces:
            maxim = number_of_beaten_pieces
    ret_list = list()
    for piece_cords, target_cords, number_of_beaten_pieces, cords_of_beaten_pieces in all_possible_moves:
        if number_of_beaten_pieces == maxim:
            ret_list.append((piece_cords, target_cords, cords_of_beaten_pieces))
    if len(ret_list) != 0:
        return random.choice(ret_list)
    else:
        return None


def max_score(best_value, this_value):
    if best_value is None:
        return this_value
    else:
        return max(best_value, this_value)


def min_score(best_value, this_value):
    if best_value is None:
        return this_value
    else:
        return min(best_value, this_value)


def move_piece_on_list(list_of_pieces, piece_cords, target_cords):
    ret_list = list()
    for piece in list_of_pieces:
        if piece == piece_cords:
            ret_list.append(target_cords)
        else:
            ret_list.append(piece)
    return ret_list


def remove_piece_from_list(lista, cordy_zbitego):
    ret_list = list()
    for pionek in lista:
        if pionek != cordy_zbitego:
            ret_list.append(pionek)
    return ret_list

# -*- coding: utf-8 -*-

import random
from tools import Color
from ai_tools import custom_min, custom_max
from gameLogic.listOfPieces import ListOfPieces
from gameLogic.move import Move
from gameLogic.gameLogic import find_all_possible_moves, possible_attacks
import math


def ai(list_of_pieces, settings):
    if settings.ai_difficulty<4 and settings.ai_difficulty<random.randint(1,4):
        all_possible_moves = find_all_possible_moves(list_of_pieces, Color.white, settings)
        return random.choice(all_possible_moves)
    best_moves = _ai_compute_best_moves(list_of_pieces,settings)
    return random.choice(best_moves)


def ai_test(list_of_pieces, settings):
    foo = _ai_compute_best_moves(list_of_pieces,settings)
    assert isinstance(foo, list)
    if len(foo) == 1:  # assert test are written in a way that there is only one possible good answer
        return foo[0]
    else:
        raise ValueError


def _ai_compute_best_moves(list_of_pieces, settings):
    best_score = -math.inf
    best_moves = list()
    all_possible_moves = find_all_possible_moves(list_of_pieces, Color.white, settings)

    for move in all_possible_moves:
        copy_list_of_pieces = list_of_pieces.copy()
        copy_list_of_pieces.apply_move(move)

        if settings.multiple_attack and move.destroyed and possible_attacks(move.dest, copy_list_of_pieces):
            score = _ai_rek(copy_list_of_pieces, Color.white, settings, settings.ai_difficulty)
        else:
            score = _ai_rek(copy_list_of_pieces, Color.black, settings, settings.ai_difficulty)

        if score > best_score:
            best_moves = list()
            best_score = score
        if score == best_score:
            best_moves.append(move)
    if len(best_moves) == 0:
        empty_move = Move(tuple(), tuple(), tuple())
        best_moves.append(empty_move)
    return best_moves


def _ai_rek(list_of_pieces: ListOfPieces, color_of_active_side, settings, depth_limiter):
    min_max_value = None
    if depth_limiter == 0:
        return len(list_of_pieces.white_pieces) - len(list_of_pieces.black_pieces)
    depth_limiter -= 1

    all_possible_moves = find_all_possible_moves(list_of_pieces, color_of_active_side, settings)

    if not all_possible_moves:
        return len(list_of_pieces.white_pieces) - len(list_of_pieces.black_pieces)

    for move in all_possible_moves:
        copy_list_of_pieces = list_of_pieces.copy()
        copy_list_of_pieces.apply_move(move)
        if settings.multiple_attack and move.destroyed and possible_attacks(move.dest, copy_list_of_pieces):
            score = _ai_rek(copy_list_of_pieces, color_of_active_side, settings, depth_limiter)
        else:
            score = _ai_rek(copy_list_of_pieces, not color_of_active_side, settings, depth_limiter)

        if color_of_active_side == Color.black:
            min_max_value = custom_min(min_max_value, score)
        else:
            min_max_value = custom_max(min_max_value, score)
    return min_max_value

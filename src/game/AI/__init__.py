# -*- coding: utf-8 -*-

from .ai_tools import *
import random
from tools import *


def ai(list_of_white_pieces, list_of_black_pieces, settings):
    if settings.ai_difficulty<4 and settings.ai_difficulty<random.randint(1,4):
        all_possible_moves = find_all_possible_moves(list_of_white_pieces, list_of_black_pieces, Color.black, settings)
        piece_cords, target_pos_cords, beaten_piece_cords = random.choice(all_possible_moves)
        if beaten_piece_cords == 0:
            return [piece_cords, target_pos_cords, list()]
        return [piece_cords, target_pos_cords, [beaten_piece_cords]]
    return random.choice(_ai_compute_best_moves(list_of_white_pieces,list_of_black_pieces,settings))


def ai_test(list_of_white_pieces, list_of_black_pieces, settings):
    foo = _ai_compute_best_moves(list(list_of_white_pieces),list(list_of_black_pieces),settings)
    assert isinstance(foo, list)
    if len(foo) == 0:
        return Move(tuple(), tuple(), list())
    assert len(foo) == 1  # assert test are written in a way that there is only one possible good answer
    return new_move(foo[0])


def _ai_compute_best_moves(list_of_white_pieces, list_of_black_pieces, settings):
    best_score = -math.inf
    best_moves = list()
    all_possible_moves = find_all_possible_moves(list_of_white_pieces, list_of_black_pieces, Color.black, settings)

    if len(all_possible_moves) == 0:
        return all_possible_moves

    for piece_cords, target_pos_cords, beaten_piece_cords in all_possible_moves:
        list_of_beaten_pieces = list()
        new_list_of_black_pieces = move_piece_on_list(list_of_black_pieces, piece_cords, target_pos_cords)
        if beaten_piece_cords:
            new_list_of_white_pieces = remove_piece_from_list(list_of_white_pieces, beaten_piece_cords)
            if settings.multiple_attack:
                target_pos_cords, list_of_beaten_pieces = _ai_rek_another_attack_in_a_row(new_list_of_white_pieces,
                                                                                          new_list_of_black_pieces,
                                                                                          Color.black, target_pos_cords)
                for beaten_piece in list_of_beaten_pieces:
                    new_list_of_white_pieces = remove_piece_from_list(new_list_of_white_pieces, beaten_piece)
            list_of_beaten_pieces.append(beaten_piece_cords)
        else:
            new_list_of_white_pieces = list_of_white_pieces
        score = _ai_rek(new_list_of_white_pieces, new_list_of_black_pieces, Color.white, settings, settings.ai_difficulty)
        if score > best_score:
            best_moves = list()
            best_score = score
        if score == best_score:
            best_moves.append((piece_cords, target_pos_cords, list_of_beaten_pieces))

    return best_moves


def _ai_rek(list_of_white_pieces, list_of_black_pieces, color_of_active_side, settings, depth_limiter):
    min_max_value = None
    if depth_limiter == 0:
        return len(list_of_black_pieces) - len(list_of_white_pieces)
    depth_limiter -= 1

    all_possible_moves = find_all_possible_moves(list_of_white_pieces, list_of_black_pieces, color_of_active_side, settings)

    if not all_possible_moves:
        return len(list_of_black_pieces) - len(list_of_white_pieces)

    if color_of_active_side == Color.black:
        for piece_cords, target_pos_cords, beaten_piece_cords in all_possible_moves:
            new_list_of_black_pieces = move_piece_on_list(list_of_black_pieces, piece_cords, target_pos_cords)
            if beaten_piece_cords != 0:
                new_list_of_white_pieces = remove_piece_from_list(list_of_white_pieces, beaten_piece_cords)

                if settings.multiple_attack:
                    target_pos_cords, list_of_beaten_pieces = _ai_rek_another_attack_in_a_row(new_list_of_white_pieces,
                                                                                              new_list_of_black_pieces,
                                                                                              color_of_active_side,
                                                                                              target_pos_cords)
                    for foo in list_of_beaten_pieces:
                        new_list_of_white_pieces = remove_piece_from_list(new_list_of_white_pieces, foo)
            else:
                new_list_of_white_pieces = list_of_white_pieces
            score = _ai_rek(new_list_of_white_pieces, new_list_of_black_pieces, not color_of_active_side, settings, depth_limiter)
            min_max_value = max_score(min_max_value, score)
    elif color_of_active_side == Color.white:
        for piece_cords, target_pos_cords, beaten_piece_cords in all_possible_moves:
            new_list_of_white_pieces = move_piece_on_list(list_of_white_pieces, piece_cords, target_pos_cords)
            if beaten_piece_cords:
                new_list_of_black_pieces = remove_piece_from_list(list_of_black_pieces, beaten_piece_cords)
                target_pos_cords, list_of_beaten_pieces = _ai_rek_another_attack_in_a_row(new_list_of_white_pieces,
                                                                                          new_list_of_black_pieces,
                                                                                          color_of_active_side,
                                                                                          target_pos_cords)
                for foo in list_of_beaten_pieces:
                    new_list_of_black_pieces = remove_piece_from_list(new_list_of_black_pieces, foo)
            else:
                new_list_of_black_pieces = list_of_black_pieces
            score = _ai_rek(new_list_of_white_pieces, new_list_of_black_pieces, Color.black, settings, depth_limiter)
            min_max_value = min_score(min_max_value, score)
    return min_max_value


def _ai_rek_another_attack_in_a_row(list_of_white_pieces, list_of_black_pieces, color_of_active_side, cords):
    possible_attacks_moves = possible_attacks(cords, list_of_white_pieces, list_of_black_pieces)
    possible_scores = list()
    for target_cords, beaten_cords in possible_attacks_moves.items():
        if color_of_active_side == Color.black:
            new_list_of_black_pieces = move_piece_on_list(list_of_black_pieces, cords, target_cords)
            new_list_of_white_pieces = remove_piece_from_list(list_of_white_pieces, beaten_cords)
        else:
            new_list_of_white_pieces = move_piece_on_list(list_of_white_pieces, cords, target_cords)
            new_list_of_black_pieces = remove_piece_from_list(list_of_black_pieces, beaten_cords)

        target_cords, beaten_piece_cords = _ai_rek_another_attack_in_a_row(new_list_of_white_pieces,
                                                                           new_list_of_black_pieces,
                                                                           color_of_active_side, target_cords)
        ret_list = [beaten_cords]
        ret_list.extend(beaten_piece_cords)
        possible_scores.append((target_cords, ret_list))

    best_score = 0
    best_score_ret_data = (cords, list())
    for cords_of_target_score, ret_list_of_score in possible_scores:
        if len(ret_list_of_score) > best_score:
            best_score_ret_data = (cords_of_target_score, ret_list_of_score)
            best_score = len(ret_list_of_score)

    return best_score_ret_data

# -*- coding: utf-8 -*-

from tools import *
from .ai_tools import *
from Game.game_logic import possible_attacks


def ai(list_of_white_pieces, list_of_black_pieces):
    list_of_beaten_pieces = list()
    all_possible_moves_with_score = list()
    all_possible_moves = find_all_possible_moves(list_of_white_pieces, list_of_black_pieces, Color.black)
    for piece_cords, target_pos_cords, beaten_piece_cords in all_possible_moves:
        new_list_of_black_pieces = move_piece_on_list(list_of_black_pieces, piece_cords, target_pos_cords)
        if beaten_piece_cords != 0:
            new_list_of_white_pieces = remove_piece_from_list(list_of_white_pieces, beaten_piece_cords)
            target_pos_cords, list_of_beaten_pieces = _ai_rek_another_attack_in_a_row(new_list_of_white_pieces, new_list_of_black_pieces, Color.black, target_pos_cords)
            for beaten_piece in list_of_beaten_pieces:
                new_list_of_white_pieces = remove_piece_from_list(new_list_of_white_pieces, beaten_piece)
            list_of_beaten_pieces.append(beaten_piece_cords)
        else:
            new_list_of_white_pieces = list_of_white_pieces
        deep = 5
        score = _ai_rek(new_list_of_white_pieces, new_list_of_black_pieces, 1, deep)
        all_possible_moves_with_score.append((piece_cords, target_pos_cords, score, list_of_beaten_pieces))
        #logging.debug("[AI] It's possible to move %s -> %s with score %s", str(piece_cords), str(target_pos_cords), str(list_of_beaten_pieces))
    return the_best_move(all_possible_moves_with_score)


def _ai_rek(list_of_white_pieces, list_of_black_pieces, color_of_active_side, depth_limiter):
    min_max_value = None
    if depth_limiter == 0:
        return len(list_of_black_pieces) - len(list_of_white_pieces)
    depth_limiter -= 1

    all_possible_moves = find_all_possible_moves(list_of_white_pieces, list_of_black_pieces, color_of_active_side)

    if len(all_possible_moves) == 0:
        return len(list_of_black_pieces) - len(list_of_white_pieces)

    if color_of_active_side == Color.black:
        for piece_cords, target_pos_cords, beaten_piece_cords in all_possible_moves:
            new_list_of_black_pieces = move_piece_on_list(list_of_black_pieces, piece_cords, target_pos_cords)
            if beaten_piece_cords != 0:
                new_list_of_white_pieces = remove_piece_from_list(list_of_white_pieces, beaten_piece_cords)
                target_pos_cords, list_of_beaten_pieces = _ai_rek_another_attack_in_a_row(new_list_of_white_pieces, new_list_of_black_pieces, color_of_active_side, target_pos_cords)
                for foo in list_of_beaten_pieces:
                    new_list_of_white_pieces = remove_piece_from_list(new_list_of_white_pieces, foo)
            else:
                new_list_of_white_pieces = list_of_white_pieces
            score = _ai_rek(new_list_of_white_pieces, new_list_of_black_pieces, not color_of_active_side, depth_limiter)
            min_max_value = max_score(min_max_value, score)
    elif color_of_active_side == Color.white:
        for piece_cords, target_pos_cords, beaten_piece_cords in all_possible_moves:
            new_list_of_white_pieces = move_piece_on_list(list_of_white_pieces, piece_cords, target_pos_cords)
            if beaten_piece_cords != 0:
                new_list_of_black_pieces = remove_piece_from_list(list_of_black_pieces, beaten_piece_cords)
                target_pos_cords, list_of_beaten_pieces = _ai_rek_another_attack_in_a_row(new_list_of_white_pieces, new_list_of_black_pieces, color_of_active_side, target_pos_cords)
                for foo in list_of_beaten_pieces:
                    new_list_of_black_pieces = remove_piece_from_list(new_list_of_black_pieces, foo)
            else:
                new_list_of_black_pieces = list_of_black_pieces
            score = _ai_rek(new_list_of_white_pieces, new_list_of_black_pieces, Color.black, depth_limiter)
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

        target_cords, beaten_piece_cords = _ai_rek_another_attack_in_a_row(new_list_of_white_pieces, new_list_of_black_pieces, color_of_active_side, target_cords)
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

# -*- coding: utf-8 -*-
from game.AI import ai_test
from game.AI import _ai_rek_another_attack_in_a_row
from tools import *
from settings import Settings


class TestAi:
    def test_no_possible_movement_empty_board(self):
        default_settings = Settings(default=True)

        tested_board = ListOfPieces([], [])
        asserted_board = ListOfPieces([], [])
        ai_move = ai_test(tested_board.white_pieces, tested_board.black_pieces, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_no_possible_movement_end_of_board(self):
        default_settings = Settings(default=True)

        tested_board = ListOfPieces([], [(2, 0)])
        asserted_board = ListOfPieces([], [(2, 0)])
        ai_move = ai_test(tested_board.white_pieces, tested_board.black_pieces, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

        tested_board = ListOfPieces([(0, 0), (2, 0)], [(1, 1)])
        asserted_board = ListOfPieces([(0, 0), (2, 0)], [(1, 1)])
        ai_move = ai_test(tested_board.white_pieces, tested_board.black_pieces, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_simple_move(self):
        default_settings = Settings(default=True)

        tested_board = ListOfPieces([], [(7,7)])
        asserted_board = ListOfPieces([], [(6,6)])
        ai_move = ai_test(tested_board.white_pieces, tested_board.black_pieces, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

        tested_board = ListOfPieces([(0,6)], [(1,7)])
        asserted_board = ListOfPieces([(0,6)], [(2,6)])
        ai_move = ai_test(tested_board.white_pieces, tested_board.black_pieces, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_simple_attack_move(self):
        default_settings = Settings(default=True)

        tested_board = ListOfPieces([(1,1)],[(2,2)])
        asserted_board = ListOfPieces([],[(0,0)])
        ai_move = ai_test(tested_board.white_pieces, tested_board.black_pieces, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

        tested_board = ListOfPieces([(7,3),(5,3)],[(6,4)])
        asserted_board = ListOfPieces([(7,3)],[(4,2)])
        ai_move = ai_test(tested_board.white_pieces, tested_board.black_pieces, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_not_making_losing_moves(self):
        default_settings = Settings(default=True)

        tested_board = ListOfPieces([(1,1)],[(3,3)])
        asserted_board = ListOfPieces([(1,1)],[(4,2)])
        ai_move = ai_test(tested_board.white_pieces, tested_board.black_pieces, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

        tested_board = ListOfPieces([(2,2),(1,1)],[(3,3),(7,7)])
        asserted_board = ListOfPieces([(2,2),(1,1)],[(4,2),(7,7)])
        ai_move = ai_test(tested_board.white_pieces, tested_board.black_pieces, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_guessing_enemy_moves(self):
        default_settings = Settings(default=True)

        tested_board = ListOfPieces([(0,0),(2,2),(4,2)],[(3,3)])
        asserted_board = ListOfPieces([(0,0),(2,2)],[(5,1)])
        ai_move = ai_test(tested_board.white_pieces, tested_board.black_pieces, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_multiple_attack(self):
        default_settings = Settings(default=True)

        tested_board = ListOfPieces([(1,1),(3,3),(5,3)],[(4,4)])
        asserted_board = ListOfPieces([(5,3)],[(0,0)])
        ai_move = ai_test(tested_board.white_pieces, tested_board.black_pieces, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_multiple_attack_recursive_function(self):
        wynik = _ai_rek_another_attack_in_a_row([(1, 1), (3, 3)], [(4, 4)], Color.black, (4, 4))
        assert wynik == ((0,0),[(3,3),(1,1)])

        wynik = _ai_rek_another_attack_in_a_row([(1, 1), (3, 3), (5, 3)], [(4, 4)], Color.black, (4, 4))
        assert wynik == ((0,0),[(3,3),(1,1)])

    def test_setting_force_attack(self):
        default_settings = Settings(default=True)

        tested_board = """"  +---------------+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | |w| |b| | | | |
                             |-+-+-+-+-+-+-+-+
                             | | |w| | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | |b| |b| | |
                             |-+-+-+-+-+-+-+-+
                             |w| |w| | | | | |
                             +---------------+"""

        asserted_board = """"+---------------+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | |w| | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | |b| |b| |b| | |
                             |-+-+-+-+-+-+-+-+
                             |w| |w| | | | | |
                             +---------------+"""

        tested_board = str_to_cords(tested_board)
        asserted_board = str_to_cords(asserted_board)
        ai_move = ai_test(tested_board.white_pieces, tested_board.black_pieces, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

        default_settings.force_attack=False

        tested_board = """"  +---------------+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | |w| |b| | | | |
                             |-+-+-+-+-+-+-+-+
                             | | |w| | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | |b| |b| | |
                             |-+-+-+-+-+-+-+-+
                             |w| |w| | | | | |
                             +---------------+"""

        asserted_board = """"+---------------+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | |w| |b| | | | |
                             |-+-+-+-+-+-+-+-+
                             | | |w| | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | |b| | |
                             |-+-+-+-+-+-+-+-+
                             |w| |w| |b| | | |
                             +---------------+"""

        tested_board = str_to_cords(tested_board)
        asserted_board = str_to_cords(asserted_board)
        ai_move = ai_test(tested_board.white_pieces, tested_board.black_pieces, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_setting_multiple_attack(self):
        default_settings = Settings(default=True)

        tested_board = """"  +---------------+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | |b| | | |
                             |-+-+-+-+-+-+-+-+
                             | | | |w| |w| | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | |w| |
                             |-+-+-+-+-+-+-+-+
                             | |w| | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             +---------------+"""

        asserted_board = """"+---------------+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | |w| | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | |w| |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             |b| | | | | | | |
                             +---------------+"""
        tested_board = str_to_cords(tested_board)
        asserted_board = str_to_cords(asserted_board)
        ai_move = ai_test(tested_board.white_pieces, tested_board.black_pieces, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

        default_settings.multiple_attack=False

        tested_board = """"  +---------------+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | |b| | | |
                             |-+-+-+-+-+-+-+-+
                             | | | |w| |w| | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | |w| |
                             |-+-+-+-+-+-+-+-+
                             | |w| | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             +---------------+"""

        asserted_board = """"+---------------+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | |w| | |
                             |-+-+-+-+-+-+-+-+
                             | | |b| | | |w| |
                             |-+-+-+-+-+-+-+-+
                             | |w| | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             +---------------+"""
        tested_board = str_to_cords(tested_board)
        asserted_board = str_to_cords(asserted_board)
        ai_move = ai_test(tested_board.white_pieces, tested_board.black_pieces, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

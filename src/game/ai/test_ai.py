# -*- coding: utf-8 -*-
from game.ai import ai_test
from settings import Settings
from gameLogic.listOfPieces import ListOfPieces, str_to_cords


class TestAi:
    def test_no_possible_movement_empty_board(self):
        default_settings = Settings(default=True)

        tested_board = ListOfPieces([], [])
        asserted_board = ListOfPieces([], [])
        ai_move = ai_test(tested_board, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_no_possible_movement_end_of_board(self):
        default_settings = Settings(default=True)

        tested_board = ListOfPieces([(2, 0)], [])
        asserted_board = ListOfPieces([(2, 0)], [])
        ai_move = ai_test(tested_board, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_no_possible_movement_path_blocked(self):
        default_settings = Settings(default=True)

        tested_board = ListOfPieces([(1, 1)],[(0, 0), (2, 0)])
        asserted_board = ListOfPieces([(1, 1)],[(0, 0), (2, 0)])
        ai_move = ai_test(tested_board, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_simple_move(self):
        default_settings = Settings(default=True)

        tested_board = ListOfPieces([(7,7)], [])
        asserted_board = ListOfPieces([(6,6)], [])
        ai_move = ai_test(tested_board, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

        tested_board = ListOfPieces([(1,7)], [(0,6)])
        asserted_board = ListOfPieces([(2,6)], [(0,6)])
        ai_move = ai_test(tested_board, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_simple_attack_move1(self):
        default_settings = Settings(default=True)

        tested_board = ListOfPieces([(2,2)],[(1,1)])
        asserted_board = ListOfPieces([(0,0)],[])
        ai_move = ai_test(tested_board, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_simple_attack_move2(self):
        default_settings = Settings(default=True)

        tested_board = ListOfPieces([(6,4)],[(7,3),(5,3)])
        asserted_board = ListOfPieces([(4,2)],[(7,3)])
        ai_move = ai_test(tested_board, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_not_making_losing_moves_1(self):
        default_settings = Settings(default=True)

        tested_board = ListOfPieces([(3,3)],[(1,1)])
        asserted_board = ListOfPieces([(4,2)],[(1,1)])
        ai_move = ai_test(tested_board, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_not_making_losing_moves_2(self):
        default_settings = Settings(default=True)
        tested_board = ListOfPieces([(3,3),(7,7)],[(2,2),(1,1)])
        asserted_board = ListOfPieces([(4,2),(7,7)],[(2,2),(1,1)])
        ai_move = ai_test(tested_board, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_guessing_enemy_moves(self):
        default_settings = Settings(default=True)

        tested_board = ListOfPieces([(3,3)],[(0,0),(2,2),(4,2)])
        asserted_board = ListOfPieces([(5,1)],[(0,0),(2,2)])
        ai_move = ai_test(tested_board, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

    def test_multiple_attack(self):
        default_settings = Settings(default=True)

        tested_board = """"  +---------------+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | |w| | | |
                             |-+-+-+-+-+-+-+-+
                             | | | |b| |b| | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | |b| | | | | | |
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
                             | | | | | |b| | |
                             |-+-+-+-+-+-+-+-+
                             | | |w| | | | | |
                             |-+-+-+-+-+-+-+-+
                             | |b| | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             +---------------+"""

        tested_board = str_to_cords(tested_board)
        asserted_board = str_to_cords(asserted_board)
        ai_move = ai_test(tested_board, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

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
                             | |b| |w| | | | |
                             |-+-+-+-+-+-+-+-+
                             | | |b| | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | |w| |w| | |
                             |-+-+-+-+-+-+-+-+
                             |b| |b| | | | | |
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
                             | |b| | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | |w| |w| |w| | |
                             |-+-+-+-+-+-+-+-+
                             |b| |b| | | | | |
                             +---------------+"""

        tested_board = str_to_cords(tested_board)
        asserted_board = str_to_cords(asserted_board)
        ai_move = ai_test(tested_board, default_settings)
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
                             | |b| |w| | | | |
                             |-+-+-+-+-+-+-+-+
                             | | |b| | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | |w| |w| | |
                             |-+-+-+-+-+-+-+-+
                             |b| |b| | | | | |
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
                             | |b| |w| | | | |
                             |-+-+-+-+-+-+-+-+
                             | | |b| | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | |w| | |
                             |-+-+-+-+-+-+-+-+
                             |b| |b| |w| | | |
                             +---------------+"""

        tested_board = str_to_cords(tested_board)
        asserted_board = str_to_cords(asserted_board)
        ai_move = ai_test(tested_board, default_settings)
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
                             | | | | |w| | | |
                             |-+-+-+-+-+-+-+-+
                             | | | |b| |b| | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | |b| | | | | | |
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
                             | | | | | |b| | |
                             |-+-+-+-+-+-+-+-+
                             | | |w| | | | | |
                             |-+-+-+-+-+-+-+-+
                             | |b| | | | | | |
                             |-+-+-+-+-+-+-+-+
                             || | | | | | | |
                             +---------------+"""
        tested_board = str_to_cords(tested_board)
        asserted_board = str_to_cords(asserted_board)
        ai_move = ai_test(tested_board, default_settings)
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
                             | | | | |w| | | |
                             |-+-+-+-+-+-+-+-+
                             | | | |b| |b| | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | |b| |
                             |-+-+-+-+-+-+-+-+
                             | |b| | | | | | |
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
                             | | | | | |b| | |
                             |-+-+-+-+-+-+-+-+
                             | | |w| | | |b| |
                             |-+-+-+-+-+-+-+-+
                             | |b| | | | | | |
                             |-+-+-+-+-+-+-+-+
                             | | | | | | | | |
                             +---------------+"""
        tested_board = str_to_cords(tested_board)
        asserted_board = str_to_cords(asserted_board)
        ai_move = ai_test(tested_board, default_settings)
        tested_board.apply_move(ai_move)
        assert tested_board == asserted_board

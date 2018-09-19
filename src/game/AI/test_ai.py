# -*- coding: utf-8 -*-
from unittest import TestCase
from game.AI import ai
from game.AI import _ai_rek_another_attack_in_a_row
from tools import *
from settings import Settings


class TestAi:
    def test_no_possible_movement(self):
        default_settings = Settings(default=True)
        wynik = ai([], [], default_settings)
        assert wynik is None
        wynik = ai([], [(2, 0)], default_settings)
        assert wynik is None
        wynik = ai([(0, 0), (2, 0)], [(1, 1)], default_settings)
        assert wynik is None

    def test_simple_move(self):
        default_settings = Settings(default=True)
        wynik = ai([], [(7,7)], default_settings)
        assert wynik == ((7,7), (6,6), [])

        wynik = ai([(0,6)], [(1,7)], default_settings)
        assert wynik == ((1,7), (2,6), [])

    def test_simple_attack_move(self):
        default_settings = Settings(default=True)
        wynik = ai([(1,1)],[(2,2)], default_settings)
        assert wynik == ((2,2),(0,0),[(1,1)])

        wynik = ai([(7,3),(5,3)],[(6,4)], default_settings)
        assert wynik == ((6,4),(4,2),[(5,3)])

    def test_not_making_losing_moves(self):
        default_settings = Settings(default=True)
        wynik = ai([(1,1)],[(3,3)], default_settings)
        assert wynik == ((3,3),(4,2),[])

        wynik = ai([(2,2),(1,1)],[(3,3),(7,7)], default_settings)
        assert wynik == ((3,3),(4,2),[])

    def test_guessing_enemy_moves(self):
        default_settings = Settings(default=True)
        wynik = ai([(0,0),(2,2),(4,2)],[(3,3)], default_settings)
        assert wynik == ((3,3),(5,1),[(4,2)])

    def test_multiple_attack(self):
        default_settings = Settings(default=True)
        wynik = ai([(1,1),(3,3),(5,3)],[(4,4)], default_settings)
        assert wynik == ((4,4),(0,0),[(1,1),(3,3)])

    def test_multiple_attack_recursive_function(self):
        wynik = _ai_rek_another_attack_in_a_row([(1, 1), (3, 3)], [(4, 4)], Color.black, (4, 4))
        assert wynik == ((0,0),[(3,3),(1,1)])

        wynik = _ai_rek_another_attack_in_a_row([(1, 1), (3, 3), (5, 3)], [(4, 4)], Color.black, (4, 4))
        assert wynik == ((0,0),[(3,3),(1,1)])

    def test_setting_force_attack(self):
        default_settings = Settings(default=True)
        wynik = ai([(0,0),(2,2),(1,3),(2,0)],[(3,3),(3,1),(5,1)], default_settings)
        assert wynik == ((3, 3), (1, 1), [(2, 2)])

        default_settings.force_attack=False
        wynik = ai([(0,0),(2,2),(1,3),(2,0)],[(3,3),(3,1),(5,1)], default_settings)
        assert wynik == ((3, 1), (4, 0), [])

    def test_setting_multiple_attack(self):
        default_settings = Settings(default=True)
        wynik = ai([(1,1),(3,3),(5,3),(6,2)],[(4,4)], default_settings)
        assert wynik == ((4, 4), (0, 0), [(1,1), (3, 3)])

        default_settings.multiple_attack=False
        wynik = ai([(1,1),(3,3),(5,3),(6,2)],[(4,4)], default_settings)
        assert wynik == ((4, 4), (2, 2),[(3,3)])


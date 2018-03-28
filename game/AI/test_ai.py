# -*- coding: utf-8 -*-
from unittest import TestCase
from game.AI import ai
from game.AI import _ai_rek_another_attack_in_a_row
from tools import *
from settings import Settings


class TestAi(TestCase):
    def testNoPossibleMovement(self):
        default_settings = Settings(default=True)
        wynik = ai([], [], default_settings)
        self.assertEqual(wynik, None)
        wynik = ai([], [(2, 0)], default_settings)
        self.assertEqual(wynik, None)
        wynik = ai([(0, 0), (2, 0)], [(1, 1)], default_settings)
        self.assertEqual(wynik, None)

    def testSimpleMove(self):
        default_settings = Settings(default=True)
        wynik = ai([], [(7,7)], default_settings)
        self.assertEqual(wynik, ((7,7), (6,6), []))

        wynik = ai([(0,6)], [(1,7)], default_settings)
        self.assertEqual(wynik, ((1,7), (2,6), []))

    def testSimpleAttackMove(self):
        default_settings = Settings(default=True)
        wynik = ai([(1,1)],[(2,2)], default_settings)
        self.assertEqual(wynik,((2,2),(0,0),[(1,1)]))

        wynik = ai([(7,3),(5,3)],[(6,4)], default_settings)
        self.assertEqual(wynik,((6,4),(4,2),[(5,3)]))

    def testNotMakingLosingMoves(self):
        default_settings = Settings(default=True)
        wynik = ai([(1,1)],[(3,3)], default_settings)
        self.assertEqual(wynik,((3,3),(4,2),[]))

        wynik = ai([(2,2),(1,1)],[(3,3),(7,7)], default_settings)
        self.assertEqual(wynik,((3,3),(4,2),[]))

    def testGuessingEnemyMoves(self):
        default_settings = Settings(default=True)
        wynik = ai([(0,0),(2,2),(4,2)],[(3,3)], default_settings)
        self.assertEqual(wynik,((3,3),(5,1),[(4,2)]))

    def testMultipleAttack(self):
        default_settings = Settings(default=True)
        wynik = ai([(1,1),(3,3),(5,3)],[(4,4)], default_settings)
        self.assertEqual(wynik,((4,4),(0,0),[(1,1),(3,3)]))

    def testMultipleAttackRecursiveFunction(self):
        wynik = _ai_rek_another_attack_in_a_row([(1, 1), (3, 3)], [(4, 4)], Color.black, (4, 4))
        self.assertEqual(wynik, ((0,0),[(3,3),(1,1)]))

        wynik = _ai_rek_another_attack_in_a_row([(1, 1), (3, 3), (5, 3)], [(4, 4)], Color.black, (4, 4))
        self.assertEqual(wynik, ((0,0),[(3,3),(1,1)]))

    def testSettingForceAttack(self):
        default_settings = Settings(default=True)
        wynik = ai([(0,0),(2,2),(1,3),(2,0)],[(3,3),(3,1),(5,1)], default_settings)
        self.assertEqual(wynik,((3, 3), (1, 1), [(2, 2)]))

        default_settings.force_attack=False
        wynik = ai([(0,0),(2,2),(1,3),(2,0)],[(3,3),(3,1),(5,1)], default_settings)
        self.assertEqual(wynik,((3, 1), (4, 0), []))

    def testSettingMultipleAttack(self):
        default_settings = Settings(default=True)
        wynik = ai([(1,1),(3,3),(5,3),(6,2)],[(4,4)], default_settings)
        self.assertEqual(wynik,((4, 4), (0, 0), [(1,1), (3, 3)]))

        default_settings.multiple_attack=False
        wynik = ai([(1,1),(3,3),(5,3),(6,2)],[(4,4)], default_settings)
        self.assertEqual(wynik,((4, 4), (2, 2),[(3,3)]))


# -*- coding: utf-8 -*-
from tools import *


def mozliwe_ruchy_i_bicia(cords, color, biale, czarne):  # zwraca słownik dict[docelowy_cord] = zbity_pion
    return_dict = mozliwe_ruchy(cords, color, biale, czarne)
    return_dict.update(mozliwe_bicia(cords, color, biale, czarne))
    return return_dict


def mozliwe_ruchy(cordy_pionka, kolor_pionka, biale, czarne):
    return_dict = dict()
    if kolor_pionka == Color.white:
        if (cordy_pionka[0]-1, cordy_pionka[1]+1) not in czarne + biale:
            if cordy_pionka[0]-1 >= 0 and cordy_pionka[1]+1 <= 7:
                return_dict[(cordy_pionka[0] - 1, cordy_pionka[1] + 1)] = 0

        if (cordy_pionka[0]+1, cordy_pionka[1]+1) not in czarne + biale:
            if cordy_pionka[0]+1 <= 7 and cordy_pionka[1]+1 <= 7:
                return_dict[(cordy_pionka[0] + 1, cordy_pionka[1] + 1)] = 0

    elif kolor_pionka == Color.black:
        if (cordy_pionka[0]-1, cordy_pionka[1]-1) not in czarne + biale:
            if cordy_pionka[0]-1 >= 0 and cordy_pionka[1]-1 >= 0:
                return_dict[(cordy_pionka[0] - 1, cordy_pionka[1] - 1)] = 0

        if (cordy_pionka[0]+1, cordy_pionka[1]-1) not in czarne + biale:
            if cordy_pionka[0]+1 <= 7 and cordy_pionka[1]-1 >= 0:
                return_dict[(cordy_pionka[0] + 1, cordy_pionka[1] - 1)] = 0
    return return_dict


def mozliwe_bicia(cordy_pionka, kolor_pionka, biale, czarne):
    if kolor_pionka == Color.white:
        przeciwnik = czarne
        gracz = biale
    elif kolor_pionka == Color.black:
        przeciwnik = biale
        gracz = czarne
    else:
        raise ValueError

    wszystkie = przeciwnik + gracz
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

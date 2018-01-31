# -*- coding: utf-8 -*-
import logging
from tools import Color


class Settings:
    def __init__(self):
        self.who_starts = Color.white
        self.force_attack = True
        self.ai = True
        self.who_on_top = Color.black

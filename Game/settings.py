# -*- coding: utf-8 -*-
import logging
from tools import Color


class Settings:
    def __init__(self):
        self.who_starts = Color.black
        self.force_attack = True
        self.ai = True
        self.who_on_top = Color.white

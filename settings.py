# -*- coding: utf-8 -*-
from tools import Color
import json
import logging


class Settings:

    def __init__(self):
        try:
            data = open('settings.json')
            self.__dict__ = json.loads(data.read())
        except IOError:
            print("Could not load setting file. Loading default settings...")
            self.import_default()
            self.save_settings()
        print(self.json_dump())

    def import_default(self):
        self.who_starts = Color.white
        self.force_attack = True
        self.ai = False
        self.who_on_top = Color.white
        self.multiple_attack = True

    def json_dump(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def save_settings(self):
        with open('settings.json', 'w') as outfile:
            json.dump(self.__dict__, outfile, sort_keys=True, indent=4,
                      ensure_ascii=False)

Settings()
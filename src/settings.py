# -*- coding: utf-8 -*-
from tools import Color
import json
import logging

# attrs from list will be send when mp session will be established
list_of_mp_relevant_options = {"multiple_attack", "force_attack", "who_starts"}


class Settings:
    def __init__(self, default=False):
        self.who_starts = Color.white
        self.force_attack = True
        self.ai = False
        self.multiple_attack = True
        self.always_on_top = False
        self.ai_difficulty = 3
        if not default:
            try:
                data = open('settings.json')
                self.__dict__.update(json.loads(data.read()))
            except IOError:
                logging.debug("Could not load setting file.")
                return
            self.save_settings()

    def json_import_dump(self, json_dump):
        self.__dict__.update(json.loads(json_dump))

    def json_dump_for_mp_connection(self):
        mp_settings = dict()

        for item in list_of_mp_relevant_options:
            mp_settings[item] = getattr(self, item)

        return json.dumps(mp_settings, default=lambda o: o.__dict__)

    def save_settings(self):
        with open('settings.json', 'w') as outfile:
            json.dump(self.__dict__, outfile, sort_keys=True, indent=4, ensure_ascii=False)
        outfile.close()

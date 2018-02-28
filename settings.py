# -*- coding: utf-8 -*-
from tools import Color
import json
import logging


class Settings:

    def __init__(self, default=False):
        if default:
            self.who_starts = Color.white
            self.force_attack = True
            self.ai = False
            self.multiple_attack = True
        else:
            try:
                data = open('settings.json')
                self.__dict__ = json.loads(data.read())
            except IOError:
                logging.debug("Could not load setting file. Loading default settings...")
                self.__init__(default=True)
                return
            default_settings = Settings(default=True)
            for option in default_settings.__dict__.keys():
                if not hasattr(self, option):
                    logging.debug("Settings file is lacking option "+str(option))
                    default_attr = getattr(default_settings,option)
                    setattr(self, option, default_attr)
            self_options = list(self.__dict__.keys())
            for option in self_options:
                if not hasattr(default_settings, option):
                    logging.debug("Settings file contains unsupported option "+str(option))
                    delattr(self, option)
        self.save_settings()

    def json_dump(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def save_settings(self):
        with open('settings.json', 'w') as outfile:
            json.dump(self.__dict__, outfile, sort_keys=True, indent=4,
                      ensure_ascii=False)

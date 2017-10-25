# -*- coding: utf-8 -*-
import logging

def configure_logging(lvl):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=lvl)
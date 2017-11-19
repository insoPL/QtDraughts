# -*- coding: utf-8 -*-
from tools import *
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import *
import logging
from PyQt5.QtGui import QPainter


class Piece(QLabel):
    def __init__(self, screen):
        QLabel.__init__(self,"text",screen)
        self.move(150,150)

    @property
    def rect(self):
        pass

    def paintEvent(self, e):
        logging.debug("PaintEvent inside piece")
        pen = QPen()
        pen.setWidth(3)
        qp = QPainter()
        qp.setRenderHint(QPainter.HighQualityAntialiasing)
        qp.begin(self)
        qp.setPen(pen)
        qp.drawEllipse(0, 0, 30,30)
        qp.end()

# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon


class MainButton(QAction):
    """
    Main Button. It's located in the middle of toolbox.

    Inherits: :class:`PyQt5.QtWidgets.QAction`
    """
    def __init__(self, main_window):
        self.main_window = main_window
        QAction.__init__(self, 'New game', main_window)
        self.setShortcut('Ctrl+N')
        self.update()

    def update(self):
        """
        Change icon of Main Button according to state of :class:`game.Game` object inside :class:`Main.Main:`

        todo: Refactor code to remove checks of self.main_window.game Current solution works but is not a clean one.
        """
        if self.main_window.game.whoseTurn is None:
            self.setIcon(QIcon(':/graphics/start.png'))
        elif self.main_window.game.multiplayer and self.main_window.game.whoseTurn != self.main_window.game.isHost:
            self.setIcon(QIcon(':/graphics/internet.png'))
        elif self.main_window.game.settings.ai and self.main_window.game.whoseTurn and not self.main_window.game.multiplayer:
            self.setIcon(QIcon(':/graphics/computer.png'))
        elif self.main_window.game.whoseTurn:
            self.setIcon(QIcon(':/graphics/light_gray.png'))
        else:
            self.setIcon(QIcon(':/graphics/black.png'))


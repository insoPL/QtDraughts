# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QCheckBox, QGroupBox, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from settings import Settings, list_of_mp_relevant_options


class SettingsWindow(QWidget):
    def __init__(self, settings, mp=False):
        super().__init__()
        self.setWindowIcon(QIcon('graphics\settings.png'))
        self.settings = settings
        if self.settings.always_on_top:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)

        grid = QVBoxLayout()
        grid.addWidget(self.create_game_rules_group())
        grid.addStretch(1)
        grid.addLayout(self.cancel_accept_buttons())
        self.setLayout(grid)

        if mp:
            for name, checkBox in self.check_boxes:
                if name in list_of_mp_relevant_options:
                    checkBox.setDisabled(True)

        self.setWindowTitle("Settings")
        self.resize(400, 300)
        self.show()

    def create_game_rules_group(self):
        group_box = QGroupBox("Game Rules")
        vbox = QVBoxLayout()

        self.check_boxes = list()
        self.check_boxes.append(("force_attack", QCheckBox("If attack is possible force player to attack.")))
        self.check_boxes.append(("multiple_attack", QCheckBox("Multiple attacks of one piece in the turn.")))
        self.check_boxes.append(("ai", QCheckBox("Computer enemy.")))
        self.check_boxes.append(("who_starts", QCheckBox("White pieces start the game.")))
        self.check_boxes.append(("always_on_top", QCheckBox("Windows will be always on top. (Requires manual restart)")))

        for name, checkBox in self.check_boxes:
            checkBox.setChecked(getattr(self.settings, name))
            vbox.addWidget(checkBox)
        group_box.setLayout(vbox)
        return group_box

    def cancel_accept_buttons(self):
        accept_button = QPushButton("Accept")
        cancel_button = QPushButton("Cancel")
        default_button = QPushButton("Defaults")

        cancel_button.clicked.connect(self.close)
        accept_button.clicked.connect(self.save_and_quit)
        default_button.clicked.connect(self.back_to_defaults)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(default_button)
        hbox.addWidget(cancel_button)
        hbox.addWidget(accept_button)
        return hbox

    def save_and_quit(self):
        for name, checkBox in self.check_boxes:
            setattr(self.settings, name, checkBox.isChecked())
        self.settings.save_settings()
        self.close()

    def back_to_defaults(self):
        default_settings = Settings(True)
        for name, checkBox in self.check_boxes:
            checkBox.setChecked(getattr(default_settings, name))

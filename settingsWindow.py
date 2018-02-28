# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QCheckBox, QGroupBox, QHBoxLayout, QPushButton

from settings import Settings


class SettingsWindow(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings

        grid = QVBoxLayout()
        grid.addWidget(self.create_game_rules_group())
        grid.addStretch(1)
        grid.addLayout(self.cancel_accept_buttons())
        self.setLayout(grid)

        self.setWindowTitle("Settings")
        self.resize(400, 300)
        self.show()

    def create_game_rules_group(self):
        group_box = QGroupBox("game Rules")
        vbox = QVBoxLayout()

        self.check_boxes = list()
        self.check_boxes.append(("force_attack", QCheckBox("If attack is possible force player to attack.")))
        self.check_boxes.append(("multiple_attack", QCheckBox("Multiple attacks of one piece in the turn.")))
        self.check_boxes.append(("ai", QCheckBox("Computer enemy.")))
        self.check_boxes.append(("who_starts", QCheckBox("White pieces start the game.")))

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

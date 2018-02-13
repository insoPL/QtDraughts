# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGridLayout, QCheckBox, QGroupBox, QHBoxLayout, QPushButton
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

        self.setWindowTitle("PyQt5 Group Box")
        self.resize(400, 300)
        self.show()

    def create_game_rules_group(self):
        groupBox = QGroupBox("Game Rules")
        vbox = QVBoxLayout()

        self.checkBoxes = list()
        self.checkBoxes.append(("force_attack", QCheckBox("If attack is possible force player to attack.")))
        self.checkBoxes.append(("multiple_attack", QCheckBox("Multiple attacks of one piece in the turn.")))
        self.checkBoxes.append(("ai", QCheckBox("Computer enemy.")))
        self.checkBoxes.append(("who_starts", QCheckBox("White pieces start the game.")))
        self.checkBoxes.append(("who_on_top", QCheckBox("White pieces on top of arena")))

        for name, checkBox in self.checkBoxes:
            checkBox.setChecked(getattr(self.settings, name))
            vbox.addWidget(checkBox)
        groupBox.setLayout(vbox)
        return groupBox

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
        for name, checkBox in self.checkBoxes:
            setattr(self.settings, name, checkBox.isChecked())
        self.settings.save_settings()
        self.close()

    def back_to_defaults(self):
        default_settings = Settings(True)
        for name, checkBox in self.checkBoxes:
            checkBox.setChecked(getattr(default_settings, name))

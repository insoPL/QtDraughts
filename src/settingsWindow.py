# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QCheckBox, QGroupBox, QHBoxLayout, QPushButton, QSlider
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from settings import Settings, list_of_mp_relevant_options


class SettingsWindow(QWidget):
    def __init__(self, settings, mp=False):
        super().__init__()
        self.setWindowIcon(QIcon(':/graphics\settings.png'))
        self.settings = settings
        if self.settings.always_on_top:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)

        grid = QVBoxLayout()
        grid.addWidget(self.create_game_rules_group())
        grid.addStretch(1)
        grid.addLayout(self.cancel_accept_buttons())
        self.setLayout(grid)

        if mp:
            for name, item in self.vbox_elements.items():
                if name in list_of_mp_relevant_options:
                    item.setDisabled(True)

        self.setWindowTitle("Settings")
        self.resize(400, 300)

    def create_game_rules_group(self):
        group_box = QGroupBox("Game Rules")
        vbox = QVBoxLayout()

        self.vbox_elements = dict()
        self.vbox_elements["force_attack"] = QCheckBox("If attack is possible force player to attack.")
        self.vbox_elements["multiple_attack"] = QCheckBox("Multiple attacks of one piece in the turn.")
        self.vbox_elements["who_starts"] = QCheckBox("White pieces start the game.")
        self.vbox_elements["always_on_top"] = QCheckBox("Windows will be always on top. (Requires manual restart)")
        self.vbox_elements["ai"] = QCheckBox("Computer enemy, choose difficulty:")
        self.vbox_elements["ai_difficulty"] = QSlider(Qt.Horizontal)

        for name, item in self.vbox_elements.items():
            if isinstance(item, QCheckBox):
                item.setChecked(getattr(self.settings, name))
            elif isinstance(item, QSlider):
                item.setValue(getattr(self.settings, name))
            vbox.addWidget(item)

        self.vbox_elements["ai_difficulty"].setTickInterval(1)
        self.vbox_elements["ai_difficulty"].setRange(1,5)
        self.vbox_elements["ai"].clicked.connect(self.update_slider)
        self.update_slider()

        group_box.setLayout(vbox)
        return group_box

    def update_slider(self):
        foo = not self.vbox_elements["ai"].isChecked()
        self.vbox_elements["ai_difficulty"].setDisabled(foo)

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
        for name, item in self.vbox_elements.items():
            if isinstance(item, QCheckBox):
                setattr(self.settings, name, item.isChecked())
            elif isinstance(item, QSlider):
                setattr(self.settings, name, item.value())
        self.settings.save_settings()
        self.close()

    def back_to_defaults(self):
        default_settings = Settings(True)
        for name, item in self.vbox_elements.items():
            if isinstance(item, QCheckBox):
                item.setChecked(getattr(default_settings, name))
            elif isinstance(item, QSlider):
                item.setValue(getattr(default_settings, name))
        self.update_slider()

# -*- coding: utf-8 -*-
import logging

from PyQt5.QtWidgets import QMessageBox

import game.game_logic
from tools import Color
from .board import Board
from .pieces import Pieces
from .ai_wrapper import ThreadAI


class Game:
    def __init__(self, screen, settings):
        logging.debug("game constructor")
        self.settings = settings
        self.screen = screen
        self.board = Board(screen)
        self.pieces = None
        self.whoseTurn = None
        self.possible_moves = list()
        self.multiplayer = False

    def start_multiplayer_match(self, network_thread):
        self.multiplayer = True
        self.network_thread = network_thread
        self.network_thread.new_move.connect(self.mp_enemy_make_move)
        self.end_math()
        self.start_match()
        logging.debug("Starting Multiplayer match")

    def start_match(self):
        self.pieces = Pieces(self)
        self.whoseTurn = self.settings.who_starts
        self.screen.surrender_button.setDisabled(False)
        if self.multiplayer:
            pass
        elif self.settings.ai and self.settings.who_starts:
            self.ai_start_turn()
        else:
            self.compute_possible_moves_in_this_turn()
        self.screen.main_button.update()

    def end_math(self):
        self.possible_moves = list()
        self.pieces = None
        self.whoseTurn = None
        self.screen.main_button.update()

    def try_to_make_a_move(self, piece, dest_cords):
        if piece.cords in self.possible_moves:
            if self.try_attack(piece, dest_cords):
                if self.settings.multiple_attack and game_logic.possible_attacks(piece.cords, *self.pieces.two_lists):
                    self.possible_moves = [piece.cords]
                    return
                self.end_turn()
            elif self.try_move(piece, dest_cords):
                self.end_turn()

    def try_move(self, piece, dest_cords):
        possible_moves = game_logic.possible_moves(piece.cords, *self.pieces.two_lists)
        for possible_dest_cord, possible_destroyed_piece in possible_moves.items():
            if possible_dest_cord == dest_cords:
                piece.cords = dest_cords
                return True
        return False

    def try_attack(self, piece, dest_cords):
        possible_attacks = game_logic.possible_attacks(piece.cords, *self.pieces.two_lists)
        for possible_dest_cord, possible_destroyed_piece in possible_attacks.items():
            if possible_dest_cord == dest_cords:
                self.pieces.remove_piece(possible_destroyed_piece)
                piece.cords = dest_cords
                return True
        return False

    def end_turn(self):
        self.whoseTurn = Color.opposite(self.whoseTurn)
        self.screen.main_button.update()
        if self.multiplayer and (self.whoseTurn == Color.white):
            self.possible_moves = list()
            return
        elif self.settings.ai and (self.whoseTurn == Color.white):
            self.ai_start_turn()
        else:
            self.compute_possible_moves_in_this_turn()

    def mp_enemy_make_move(self):
        self.end_turn()

    def ai_start_turn(self):
        self.threadAI = ThreadAI(self.pieces)
        self.threadAI.finished_calculation.connect(self.ai_end_turn)
        self.threadAI.start()

    def ai_end_turn(self):
        if self.threadAI.best_move is None:
            self.end_math()
            self.threadAI = None
            QMessageBox.information(self.screen, 'Game Over', "      You Won.      ")
            return
        piece_cords, target_cords, beaten_cords = self.threadAI.best_move

        logging.debug("[AI]: AI chose to make a move %s -> %s", str(piece_cords), str(target_cords))
        piece = self.pieces.get_piece(piece_cords)
        piece.cords = target_cords
        if beaten_cords != 0:
            for beaten_piece in beaten_cords:
                self.pieces.remove_piece(beaten_piece)
        self.whoseTurn = Color.opposite(self.whoseTurn)
        self.screen.main_button.update()
        self.threadAI = None
        self.compute_possible_moves_in_this_turn()

    def list_of_pieces_which_can_attack(self) -> list:
        list_of_pieces_which_can_attack = list()
        for piece in self.pieces:
            if piece.color == self.whoseTurn:
                possible_attacks = game_logic.possible_attacks(piece.cords, *self.pieces.two_lists)
                if possible_attacks:
                    list_of_pieces_which_can_attack.append(piece.cords)
        return list_of_pieces_which_can_attack

    def list_of_pieces_which_can_move(self) -> list:
        list_of_pieces_which_can_move = list()
        for piece in self.pieces:
            if self.whoseTurn == piece.color:
                if game_logic.possible_moves(piece.cords, *self.pieces.two_lists).keys():
                    list_of_pieces_which_can_move.append(piece.cords)
        return list_of_pieces_which_can_move

    def update_drawing(self):
        self.board.redraw()

    def compute_possible_moves_in_this_turn(self):
        ret_list = list()
        list_of_pieces_which_can_attack = self.list_of_pieces_which_can_attack()
        list_of_pieces_which_can_move = self.list_of_pieces_which_can_move()

        for piece in self.pieces:
            if piece.color == self.whoseTurn and piece.cords in list_of_pieces_which_can_attack:
                ret_list.append(piece.cords)
        if ret_list and self.settings.force_attack:
            self.possible_moves = ret_list
            return

        for piece in self.pieces:
            if piece.color == self.whoseTurn and piece.cords in list_of_pieces_which_can_move:
                ret_list.append(piece.cords)
        self.possible_moves = ret_list
        if not self.possible_moves:
            self.end_math()
            if self.settings.ai:
                QMessageBox.information(self.screen, 'Game Over', "You Lost.")
            else:
                QMessageBox.information(self.screen, 'Game Over', "Player with "+Color.to_str(Color.opposite(self.whoseTurn))+" pieces won.")

# -*- coding: utf-8 -*-
import logging

from PyQt5.QtWidgets import QMessageBox

import game.gameLogic
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

    def start_multiplayer_match(self, connection):
        if connection.networkThread.mode == "server":
            self.isHost = True
        else:
            self.isHost = False

        self.settings.ai = False  # TO DO: sending settings over network
        self.multiplayer = True
        self.connection = connection
        self.connection.new_move.connect(self.mp_enemy_make_move)
        self.connection.special_action.connect(self.mp_enemy_special_action)

        self.pieces = Pieces(self)
        self.whoseTurn = Color.white
        self.screen.surrender_button.setDisabled(False)
        if self.isHost:
            self.compute_possible_moves_in_this_turn()
        self.screen.main_button.update()

        self.connection.connection_error.connect(self.connection_error)

        logging.debug("Starting Multiplayer match")

    def start_match(self):
        self.pieces = Pieces(self)
        self.whoseTurn = self.settings.who_starts
        self.screen.surrender_button.setDisabled(False)
        if self.settings.ai and self.settings.who_starts:
            self.ai_start_turn()
        else:
            self.compute_possible_moves_in_this_turn()
        self.screen.main_button.update()

    def end_match(self):
        self.possible_moves = list()
        self.pieces = None
        self.whoseTurn = None
        self.screen.main_button.update()
        self.multiplayer = False
        self.screen.surrender_button.setDisabled(True)

    def try_to_make_a_move(self, piece, dest_cords):
        if piece.cords in self.possible_moves:
            if self.try_attack(piece, dest_cords):
                if self.settings.multiple_attack and gameLogic.possible_attacks(piece.cords, *self.pieces.two_lists):
                    self.possible_moves = [piece.cords]
                    return
                self.end_turn()
            elif self.try_move(piece, dest_cords):
                self.end_turn()

    def try_move(self, piece, dest_cords):
        possible_moves = gameLogic.possible_moves(piece.cords, *self.pieces.two_lists)
        for possible_dest_cord, possible_destroyed_piece in possible_moves.items():
            if possible_dest_cord == dest_cords:
                if self.multiplayer:
                    self.connection.send_move(piece.cords, dest_cords)
                piece.cords = dest_cords
                return True
        return False

    def try_attack(self, piece, dest_cords):
        possible_attacks = gameLogic.possible_attacks(piece.cords, *self.pieces.two_lists)
        for possible_dest_cord, possible_destroyed_piece in possible_attacks.items():
            if possible_dest_cord == dest_cords:
                if self.multiplayer:
                    self.connection.send_move(piece.cords, dest_cords, possible_destroyed_piece)
                self.pieces.remove_piece(possible_destroyed_piece)
                piece.cords = dest_cords
                return True
        return False

    def end_turn(self):
        self.whoseTurn = Color.opposite(self.whoseTurn)
        self.screen.main_button.update()
        if self.multiplayer and not (self.whoseTurn == self.isHost):
            self.possible_moves = list()
            self.connection.send_special_action("end_turn")
            return
        elif self.settings.ai and (self.whoseTurn == Color.white) and not self.multiplayer:
            self.ai_start_turn()
        else:
            self.compute_possible_moves_in_this_turn()

    def mp_enemy_make_move(self, list_of_moves):
        piece_cord = list_of_moves[0]
        dest = list_of_moves[1]
        piece = self.pieces.get_piece(piece_cord)
        piece.cords = dest
        if len(list_of_moves) > 2:
            for destroyed_piece in list_of_moves[2:]:
                self.pieces.remove_piece(destroyed_piece)

    def mp_enemy_special_action(self, command):
        if command == "end_turn":
            self.end_turn()
        elif command == "surrender":
            self.end_match()
            self.connection.close()
            QMessageBox.information(self.screen, 'Game Over', "      You Won, network player surrenderd      ")
        elif "[settings]" in command:
            self.settings.json_import_dump(command[10:])

    def ai_start_turn(self):
        self.threadAI = ThreadAI(self.pieces, self.settings)
        self.threadAI.finished_calculation.connect(self.ai_end_turn)
        self.threadAI.start()

    def ai_end_turn(self):
        if self.threadAI.best_move is None:
            self.end_match()
            self.threadAI = None
            QMessageBox.information(self.screen, 'Game Over', "      You Won.      ")
            return
        piece_cords, target_cords, beaten_cords = self.threadAI.best_move

        logging.debug("[ai]: ai chose to make a move %s -> %s", str(piece_cords), str(target_cords))
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
                possible_attacks = gameLogic.possible_attacks(piece.cords, *self.pieces.two_lists)
                if possible_attacks:
                    list_of_pieces_which_can_attack.append(piece.cords)
        return list_of_pieces_which_can_attack

    def list_of_pieces_which_can_move(self) -> list:
        list_of_pieces_which_can_move = list()
        for piece in self.pieces:
            if self.whoseTurn == piece.color:
                if gameLogic.possible_moves(piece.cords, *self.pieces.two_lists).keys():
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
            self.end_match()
            if self.settings.ai:
                QMessageBox.information(self.screen, 'Game Over', "You Lost.")
            else:
                QMessageBox.information(self.screen, 'Game Over', "Player with "+Color.to_str(Color.opposite(self.whoseTurn))+" pieces won.")

    def connection_error(self, err):
        logging.debug(err)
        if "10054" in err:
            QMessageBox.warning(self.screen, 'Connection Error', "      Connection was suddenly closed.      ")
        else:
            QMessageBox.warning(self.screen, 'Connection Error', "      Connection Error.      ")
        self.end_match()

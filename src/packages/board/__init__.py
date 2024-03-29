from ..utils.colors import RGB_Color, DARK_YELLOW, DARK_RED
from ..move import Move
from ..logics import (
    get_possible_moves,
    possition_under_attack,
    is_valid,
    any_valid_moves,
    get_valid_moves,
)
from ..engine import (
    get_best_move,
)

from typing import Literal
from random import choice

import sys
import json
import pygame

pygame.init()


class Board:
    def __init__(
        self,
        cell_size: int,
        rows: int,
        cols: int,
        dark_color: RGB_Color,
        light_color: RGB_Color,
        highlight_color: RGB_Color,
        font_color: RGB_Color,
        background_color: RGB_Color,
    ) -> None:
        """initialize a board and store it's arguments.

        Args:
            cell_size (int): cell_size
            rows (int): rows
            cols (int): cols
            dark_color (RGB_Color): dark_color
            light_color (RGB_Color): light_color
            highlight_color (RGB_Color): highlight_color
            font_color (RGB_Color): font_color
            background_color (RGB_Color): background_color

        Returns:
            None:
        """
        self.cell_size: int = cell_size
        self.rows: int = rows
        self.cols: int = cols
        self.dark_color: RGB_Color = dark_color
        self.light_color: RGB_Color = light_color
        self.highlight_color: RGB_Color = highlight_color
        self.board_font: pygame.font.Font = pygame.font.Font(
            r"../res/fonts/ChessMeridaUnicode.ttf", 30
        )
        self.text_font: pygame.font.Font = pygame.font.Font(
            r"../res/fonts/calibrib.ttf", 50
        )
        self.font_color: RGB_Color = font_color
        self.background_color: RGB_Color = background_color

        self.capture_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            r"../res/sounds/capture.mp3"
        )
        self.castle_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            r"../res/sounds/castle.mp3"
        )
        self.check_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            r"../res/sounds/check.mp3"
        )
        self.game_end_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            r"../res/sounds/game_end.mp3"
        )
        self.game_start_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            r"../res/sounds/game_start.mp3"
        )
        self.promotion_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            r"../res/sounds/piece_move.mp3"
        )
        self.piece_move_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            r"../res/sounds/promotion.mp3"
        )

        # a variable to determine if the end_game sound should be played
        self.play_game_over_sound: bool = True

        self.screen: pygame.surface.Surface = pygame.display.set_mode(
            (self.rows * self.cell_size, self.cols * self.cell_size)
        )

        self.game_pause: bool = False

        # string representation of each piece. first letter is the color and the second letter is the type of piece.
        self.pieces: list[str] = [
            "wP",
            "wN",
            "wB",
            "wR",
            "wQ",
            "wK",
            "bP",
            "bN",
            "bB",
            "bR",
            "bQ",
            "bK",
        ]

        # initial state of a chess board. "__" represent empty squares.
        self.board_state: list[list[str]] = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        # a uniqe integer representing the board state for each possition.
        self.board_hash: int = 0
        self.board_hash_list: list[int] = []

        self.game_type: int | None = None

        # type of players in the game. it can be "Human" or "AI"
        self.players: dict[str, str] | None = None

        # a string representing from which side the board is shown. "w" for white and "b" for black
        self.view: str = "w"

        # initial possition of kings in the board state
        self.king_possitions: dict[str, tuple[int, int]] = {"w": (7, 4), "b": (0, 4)}

        self.castle_rights: dict[str, dict[str, bool]] = {
            "w": {"short": True, "long": True},
            "b": {"short": True, "long": True},
        }

        self.checks: dict[str, bool] = {"w": False, "b": False}

        self.checkmate: bool = False
        self.stalemate: bool = False
        self.draw_status: bool = False
        self.draw_status_type: str | None = None

        # a string used to show which side's turn it is to move
        self.turn_to_move: Literal["w", "b"] = "w"

        # used for converting board_state index to actual rank on the chess board
        self.row_to_rank: dict[int, int] = {
            0: 8,
            1: 7,
            2: 6,
            3: 5,
            4: 4,
            5: 3,
            6: 2,
            7: 1,
        }

        # used for converting board_state index to actual file on the chess board
        self.col_to_file: dict[int, str] = {
            0: "a",
            1: "b",
            2: "c",
            3: "d",
            4: "e",
            5: "f",
            6: "g",
            7: "h",
        }

        self.move_log: list[Move] = []

        # a boolean used in checking for draws or checkmates
        self.new_move: bool = True

        self.fifty_move_rule: int = 0

        self.piece_images: dict[str, pygame.surface.Surface] = {}

        self.load_piece_images()

        # possition of selected_cell in board_state
        self.selected_cell: tuple[int, int] | None = None

        # possition of selected_piece in board_state
        self.selected_piece: tuple[int, int] | None = None

        with open(r"./packages/utils/openings_list.json", "r") as openings_data_file:
            # a list of known opening database
            self.openings: list[dict[str, str | list[str]]] = json.load(
                openings_data_file
            )

        with open(r"./packages/utils/zobrist_hash_keys.json", "r") as zobrist_hash_file:
            # hash keys generated to create board_hash
            self.zobrist_hash_keys: dict[str, int] = json.load(zobrist_hash_file)

        with open(r"./packages/utils/transposition_table.json", "r") as hash_file:
            # database of stored board possitions
            self.transposition_table: dict[str, float] = json.load(hash_file)

        self.initialize_board_hash()

        pygame.display.set_caption("Chess Game")

    def initialize_board_hash(self) -> None:
        """create the the hash for initial possition.

        Args:

        Returns:
            None:
        """
        self.board_hash = 0

        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece != "__":
                    self.board_hash = (
                        self.board_hash
                        ^ self.zobrist_hash_keys[f"{piece}_({row},{col})"]
                    )

        for piece in ["wK", "wQ", "bK", "bQ"]:
            self.board_hash = (
                self.board_hash ^ self.zobrist_hash_keys[f"{piece}_castle_rights"]
            )
        self.board_hash_list = [self.board_hash]

    def load_piece_images(self) -> None:
        """creating a Surface Image for each piece and scalling them to the size of the cells on the board.

        Args:

        Returns:
            None:
        """

        for piece in self.pieces:
            self.piece_images[piece] = pygame.transform.scale(
                pygame.image.load(rf"../res/images/pieces/{piece}.png").convert_alpha(),
                (self.cell_size, self.cell_size),
            )

    def row_col_switch(self, row_col: int) -> int:
        """switching given row or col number based on the view.

        Args:
            row_col (int): row_col

        Returns:
            int:
        """
        if self.view == "w":
            return row_col
        return 7 - row_col

    def set_selected_cell(self, pos: tuple[int, int]) -> None:
        """set selected_cell based on the given mouse pos.

        Args:
            pos (tuple[int, int]): pos

        Returns:
            None:
        """

        selected_cell = (
            self.row_col_switch(pos[1] // self.cell_size),
            self.row_col_switch(pos[0] // self.cell_size),
        )
        self.selected_cell = (
            None if self.selected_cell == selected_cell else selected_cell
        )

    def set_selected_piece(self) -> None:
        """set selected_piece based on the selected_cell and previous selected_piece.

        Args:

        Returns:
            None:
        """

        if self.selected_cell is not None:
            s_row, s_col = self.selected_cell
            if self.selected_piece is None and self.board_state[s_row][s_col] != "__":
                self.selected_piece = self.selected_cell
            elif (
                self.selected_piece is not None
                and self.board_state[s_row][s_col] != "__"
            ):

                p_row, p_col = self.selected_piece

                if self.selected_piece == self.king_possitions[self.turn_to_move]:
                    if (
                        self.castle_rights[self.turn_to_move]["short"]
                        and s_row == p_row
                        and s_col == p_col + 3
                    ):
                        return
                    if (
                        self.castle_rights[self.turn_to_move]["long"]
                        and s_row == p_row
                        and s_col == p_col - 4
                    ):
                        return

                if (
                    self.board_state[p_row][p_col][0]
                    == self.board_state[s_row][s_col][0]
                ):
                    self.selected_piece = self.selected_cell

        else:
            self.selected_piece = None

    def switch_turn(self) -> None:
        """switch turn_to_move after a move is made.

        Args:

        Returns:
            None:
        """
        self.turn_to_move = "w" if self.turn_to_move == "b" else "b"

    def switch_view(self) -> None:
        """switch view of the board.

        Args:

        Returns:
            None:
        """
        if self.game_pause:
            return

        self.view = "w" if self.view == "b" else "b"
        self.selected_cell = None

    def set_checkmate_stalemate(self) -> None:
        """check if game is over after a move is made.

        Args:

        Returns:
            None:
        """
        if not self.new_move:
            return
        self.new_move = False
        if any_valid_moves(
            self.board_state,
            self.turn_to_move,
            self.king_possitions[self.turn_to_move],
            self.get_last_move(),
            self.castle_rights[self.turn_to_move],
        ):
            return

        if self.checks[self.turn_to_move]:
            self.checkmate = True
            self.move_log[-1].update_notation("#")
        else:
            self.stalemate = True

    def set_draw(self) -> None:
        """check if the game is drawn based on the possition.

        Args:

        Returns:
            None:
        """
        white_materials: list[tuple[str, int]] = []
        black_materials: list[str] = []
        colored_bishops: int | None = None

        if self.stalemate:
            self.draw_status = True
            self.draw_status_type = "Stalemate"
            return

        if self.checkmate:
            return

        if self.fifty_move_rule // 2 == 50:
            self.draw_status = True
            self.draw_status_type = "50 move rule"
            return

        if self.board_hash_list.count(self.board_hash) >= 3:

            self.draw_status = True
            self.draw_status_type = "Repetition"

        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece[1] in ["Q", "R", "P"]:
                    return
                if piece[0] == "w":
                    white_materials.append((piece, row + col))
                elif piece[0] == "b":
                    black_materials.append((piece, row + col))
        if len(white_materials) <= 2 and len(black_materials) <= 2:
            self.draw_status = True
            self.draw_status_type = "Insufficient Materials"
            return
        for piece, pos in white_materials:
            if piece[1] == "N":
                return
            if piece[1] == "B" and colored_bishops is None:
                colored_bishops = pos % 2

            elif piece[1] == "B" and colored_bishops != pos % 2:
                return
        colored_bishops = None

        for piece, pos in black_materials:
            if piece[1] == "N":
                return
            if piece[1] == "B" and colored_bishops is None:
                colored_bishops = pos % 2

            elif piece[1] == "B" and colored_bishops != pos % 2:
                return
        self.draw_status = True
        self.draw_status_type = "Insufficient Materials"

    def set_row_col_move_notation(self, move: Move) -> str:
        """return move notaition modification based on the move.

        Args:
            move (Move): move

        Returns:
            str:
        """

        row_col_notation: str = ""
        move_list: list[Move] = []
        row_flag: bool = False
        col_flag: bool = False

        if move.moved_piece[1] in ["P", "K"]:
            return row_col_notation

        for row in range(8):
            for col in range(8):

                if (
                    self.board_state[row][col] == move.moved_piece
                    and (row, col) != move.start_pos
                ):
                    moves_to_check = get_possible_moves(
                        self.board_state,
                        (row, col),
                        self.turn_to_move,
                        self.get_last_move(),
                        self.castle_rights[self.turn_to_move],
                    )
                    for check_move in moves_to_check:
                        if move.end_pos == check_move.end_pos and is_valid(
                            self.board_state,
                            check_move,
                            self.turn_to_move,
                            self.king_possitions[self.turn_to_move],
                        ):
                            move_list.append(check_move)

        for check_move in move_list:
            if col_flag is False and move.start_pos[0] == check_move.start_pos[0]:
                col_flag = True
            if row_flag is False and move.start_pos[1] == check_move.start_pos[1]:
                row_flag = True

            if row_flag and col_flag:
                break

        if col_flag:
            row_col_notation = self.col_to_file[move.start_pos[1]]

        if row_flag:
            row_col_notation += str(self.row_to_rank[move.start_pos[0]])

        return row_col_notation

    def get_last_move(self) -> Move | None:
        """get last_move if available.

        Args:

        Returns:
            Move | None:
        """
        if len(self.move_log) == 0:
            return None
        return self.move_log[-1]

    def make_move(self, move: Move | None) -> None:
        """make the given move.

        Args:
            move (Move | None): move

        Returns:
            None:
        """
        if move is None:
            return

        if (move.start_pos is not None and move.end_pos is not None) and (
            move.start_pos != move.end_pos
        ):

            available_moves: list[Move] = get_possible_moves(
                self.board_state,
                move.start_pos,
                self.turn_to_move,
                self.get_last_move(),
                self.castle_rights[self.turn_to_move],
            )

            if move in available_moves:

                move.row_col_notation = self.set_row_col_move_notation(move)

                temp_board_state: list[list[str]] = [
                    list_item.copy() for list_item in self.board_state
                ]
                if move.is_castle:
                    move.update_end_pos()

                p_row, p_col = move.start_pos

                temp_board_state[p_row][p_col] = "__"
                s_row, s_col = move.end_pos

                if move.is_pawn_promotion:
                    if self.players[self.turn_to_move] == "Human":
                        temp_board_state[s_row][s_col] = self.pawn_promotion()
                    else:
                        temp_board_state[s_row][s_col] = f"{self.turn_to_move}Q"
                else:
                    temp_board_state[s_row][s_col] = move.moved_piece

                if move.is_pawn_promotion:
                    move.promoted_piece = temp_board_state[s_row][s_col]

                if move.is_en_passant:

                    temp_board_state[move.en_passant_pos[0]][
                        move.en_passant_pos[1]
                    ] = "__"

                king_pos = (
                    move.end_pos
                    if move.moved_piece[1] == "K"
                    else self.king_possitions[self.turn_to_move]
                )

                if move.is_castle:
                    if move.get_castle_type() == "short":
                        temp_board_state[s_row][s_col - 1] = temp_board_state[s_row][
                            s_col + 1
                        ]
                        temp_board_state[s_row][s_col + 1] = "__"
                    elif move.get_castle_type() == "long":
                        temp_board_state[s_row][s_col + 1] = temp_board_state[s_row][
                            s_col - 2
                        ]
                        temp_board_state[s_row][s_col - 2] = "__"

                if not possition_under_attack(
                    temp_board_state, king_pos, self.turn_to_move
                ):

                    self.board_state: list[list[str]] = [
                        list_item.copy() for list_item in temp_board_state
                    ]

                    move.castle_rights = {
                        side: self.castle_rights[side].copy()
                        for side in self.castle_rights.keys()
                    }

                    if king_pos != self.king_possitions[self.turn_to_move]:

                        self.castle_rights[self.turn_to_move]["short"] = False
                        self.castle_rights[self.turn_to_move]["long"] = False

                    elif move.moved_piece[1] == "R":
                        if move.start_pos[1] == "0":
                            self.castle_rights[self.turn_to_move]["long"] = False
                        elif move.start_pos[1] == "7":
                            self.castle_rights[self.turn_to_move]["short"] = False

                    self.king_possitions[self.turn_to_move] = king_pos
                    self.checks[self.turn_to_move] = False

                    self.switch_turn()

                    if possition_under_attack(
                        self.board_state,
                        self.king_possitions[self.turn_to_move],
                        self.turn_to_move,
                    ):
                        self.checks[self.turn_to_move] = True
                        move.update_notation("+")

                    move.set_fifty_move_rule(self.fifty_move_rule)
                    self.fifty_move_rule = move.fifty_move_rule

                    if len(self.move_log) > 0:
                        move.opening_name = self.move_log[-1].opening_name

                    self.update_move_log(move)
                    self.update_board_hash(move)
                    self.new_move = True
                    self.update_openings()
                    self.move_sound(move, self.checks[self.turn_to_move])

            self.selected_cell = None
            self.selected_piece = None

    def undo_move(self) -> None:
        """undo last move.

        Args:

        Returns:
            None:
        """
        if self.game_pause:
            return

        self.new_move = True
        if self.move_log:

            self.board_hash_list.pop()
            self.board_hash = self.board_hash_list[-1]

            move = self.move_log.pop()
            self.checkmate = False
            self.stalemate = False
            self.draw_status = False
            self.draw_status_type = None

            if len(self.move_log) == 0:
                self.fifty_move_rule = 0
            else:
                self.fifty_move_rule = self.move_log[-1].fifty_move_rule

            s_row, s_col = move.start_pos
            e_row, e_col = move.end_pos
            self.board_state[s_row][s_col] = move.moved_piece
            self.board_state[e_row][e_col] = move.captured_piece

            if move.is_en_passant:
                self.board_state[move.en_passant_pos[0]][
                    move.en_passant_pos[1]
                ] = f"{self.turn_to_move}P"

            self.switch_turn()

            if move.is_castle:
                if move.get_castle_type() == "short":
                    self.board_state[e_row][7] = f"{self.turn_to_move}R"
                    self.board_state[e_row][e_col - 1] = "__"

                elif move.get_castle_type() == "long":
                    self.board_state[e_row][0] = f"{self.turn_to_move}R"
                    self.board_state[e_row][e_col + 1] = "__"

            if move.moved_piece[1] == "K":
                self.king_possitions[move.moved_piece[0]] = (s_row, s_col)

            self.castle_rights = {
                side: move.castle_rights[side].copy()
                for side in move.castle_rights.keys()
            }
            self.piece_move_sound.play()
            self.play_game_over_sound = True

    def get_file_rank(self, pos: tuple[int, int]) -> str:
        """get file_rank notation based on the given pos.

        Args:
            pos (tuple[int, int]): pos

        Returns:
            str:
        """

        return f"{self.col_to_file[pos[1]]}{self.row_to_rank[pos[0]]}"

    def move_sound(self, move: Move, check: bool) -> None:
        """play the move sound.

        Args:
            move (Move): move
            check (bool): check

        Returns:
            None:
        """
        sound_effect: pygame.mixer.Sound | None = None

        if check:
            sound_effect = self.check_sound
        elif move.is_pawn_promotion:
            sound_effect = self.promotion_sound
        elif move.captured_piece != "__" or move.is_en_passant:
            sound_effect = self.capture_sound
        elif move.is_castle:
            sound_effect = self.castle_sound
        else:
            sound_effect = self.piece_move_sound

        sound_effect.play()

    def update_transposition_table_file(self) -> None:
        """update transposition_table file after an engine move.

        Args:

        Returns:
            None:
        """
        with open(r"./packages/utils/transposition_table.json", "w") as hash_file:
            json.dump(self.transposition_table, hash_file, indent=2)

    def update_board_hash(self, move: Move | None) -> None:
        """update board_hash after a move.

        Args:
            move (Move | None): move

        Returns:
            None:
        """
        if move is None:
            return
        s_row, s_col = move.start_pos
        self.board_hash = (
            self.board_hash
            ^ self.zobrist_hash_keys[f"{move.moved_piece}_({s_row},{s_col})"]
        )

        e_row, e_col = move.end_pos
        if move.is_en_passant:
            p_row, p_col = move.en_passant_pos
            piece = "wP" if move.moved_piece[0] == "b" else "bP"
            self.board_hash = (
                self.board_hash ^ self.zobrist_hash_keys[f"{piece}_({p_row},{p_col})"]
            )
            self.board_hash = (
                self.board_hash ^ self.zobrist_hash_keys[f"en_passant_file_{p_col}"]
            )
        elif move.captured_piece != "__":
            self.board_hash = (
                self.board_hash
                ^ self.zobrist_hash_keys[f"{move.captured_piece}_({e_row},{e_col})"]
            )
        elif move.is_castle:
            castle_type = move.get_castle_type()
            side = move.moved_piece[0]

            if castle_type == "short" and side == "w":
                s_row, s_col = (7, 7)
                e_row, e_col = (7, 5)
                self.board_hash = (
                    self.board_hash ^ self.zobrist_hash_keys["wK_castle_rights"]
                )

            elif castle_type == "long" and side == "w":
                s_row, s_col = (7, 0)
                e_row, e_col = (7, 3)
                self.board_hash = (
                    self.board_hash ^ self.zobrist_hash_keys["wQ_castle_rights"]
                )

            elif castle_type == "short" and side == "b":
                s_row, s_col = (0, 0)
                e_row, e_col = (0, 5)
                self.board_hash = (
                    self.board_hash ^ self.zobrist_hash_keys["bK_castle_rights"]
                )

            elif castle_type == "long" and side == "b":
                s_row, s_col = (0, 0)
                e_row, e_col = (0, 3)
                self.board_hash = (
                    self.board_hash ^ self.zobrist_hash_keys["bQ_castle_rights"]
                )
            else:
                raise ValueError

            self.board_hash = (
                self.board_hash ^ self.zobrist_hash_keys[f"{side}R_({s_row},{s_col})"]
            )
            self.board_hash = (
                self.board_hash ^ self.zobrist_hash_keys[f"{side}R_({e_row},{e_col})"]
            )
        e_row, e_col = move.end_pos
        self.board_hash = (
            self.board_hash
            ^ self.zobrist_hash_keys[f"{move.moved_piece}_({e_row},{e_col})"]
        )
        if move.is_two_square_pawn_move():
            opponent_side = "w" if move.moved_piece[0] == "b" else "b"
            if e_col - 1 in range(8):
                if self.board_state[e_row][e_col - 1] == f"{opponent_side}P":

                    self.board_hash = (
                        self.board_hash
                        ^ self.zobrist_hash_keys[f"en_passant_file_{e_col - 1}"]
                    )
            if e_col + 1 in range(8):
                if self.board_state[e_row][e_col + 1] == f"{opponent_side}P":

                    self.board_hash = (
                        self.board_hash
                        ^ self.zobrist_hash_keys[f"en_passant_file_{e_col + 1}"]
                    )

        self.board_hash = self.board_hash ^ self.zobrist_hash_keys["black_to_move"]
        self.board_hash_list.append(self.board_hash)

    def update_move_log(self, move: Move) -> None:
        """add given move to the move log.

        Args:
            move (Move): move

        Returns:
            None:
        """
        self.move_log.append(move)

    def update_openings(self) -> None:
        """remove openings from the openings list if they don't match the move log.

        Args:

        Returns:
            None:
        """
        index = len(self.move_log) - 1
        if index < 0:
            return
        remaining_openings = []
        for opening in self.openings:
            if opening["moves"][index] == self.move_log[-1].notation:
                if index == len(opening["moves"]) - 1:
                    self.move_log[-1].opening_name = opening["name"]
                if index + 1 < len(opening["moves"]):
                    remaining_openings.append(opening)

        self.openings = [opening.copy() for opening in remaining_openings]

    def get_move_depth(self) -> int:
        """get depth of calculation for engine move based on the possition.

        Args:

        Returns:
            int:
        """
        number_of_pieces = 0
        for row in range(8):
            for col in range(8):
                if self.board_state[row][col] != "__":
                    number_of_pieces += 1
        if number_of_pieces <= 4:
            return 4
        return 3

    def update_board_state(self) -> None:
        """update board and game status.

        Args:

        Returns:
            None:
        """
        if self.game_pause:
            return
        self.set_selected_piece()
        if self.players[self.turn_to_move] == "Human":
            self.make_move(
                Move(
                    self.selected_piece,
                    self.selected_cell,
                    self.board_state,
                    self.turn_to_move,
                )
            )
        elif (
            self.players[self.turn_to_move] == "AI"
            and self.checkmate is False
            and self.draw_status is False
        ):

            opponent = "w" if self.turn_to_move == "b" else "b"
            move_to_make = get_best_move(
                get_valid_moves(
                    self.board_state,
                    self.turn_to_move,
                    self.king_possitions[self.turn_to_move],
                    self.castle_rights[self.turn_to_move],
                    self.get_last_move(),
                ),
                self.board_state,
                self.board_hash,
                self.turn_to_move,
                self.king_possitions[self.turn_to_move],
                self.castle_rights[self.turn_to_move],
                self.king_possitions[opponent],
                self.castle_rights[opponent],
                self.openings,
                len(self.move_log),
                self.get_last_move(),
                self.zobrist_hash_keys,
                self.transposition_table,
                self.board_hash_list,
                self.fifty_move_rule,
                3,
            )
            # a short delay between engine moves
            pygame.time.delay(200)

            self.update_transposition_table_file()

            self.make_move(
                move_to_make,
            )
        self.set_checkmate_stalemate()
        self.set_draw()

    def draw_board(self) -> None:
        """drawing the background of the board with the light and dark color specified for each cell.

        Args:

        Returns:
            None:
        """
        for row in range(self.rows):
            for col in range(self.cols):
                cell_rect: pygame.Rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                if (row + col) % 2 == 0:
                    pygame.draw.rect(self.screen, self.light_color, cell_rect)
                else:
                    pygame.draw.rect(self.screen, self.dark_color, cell_rect)
                if row == self.rows - 1:
                    text_surface = self.board_font.render(
                        (self.col_to_file[self.row_col_switch(col)]),
                        True,
                        self.font_color,
                    )

                    text_rect = text_surface.get_rect(bottomright=cell_rect.bottomright)
                    self.screen.blit(text_surface, text_rect)

                if col == 0:
                    text_surface = self.board_font.render(
                        str(self.row_to_rank[self.row_col_switch(row)]),
                        True,
                        self.font_color,
                    )
                    text_rect = text_surface.get_rect(topleft=cell_rect.topleft)
                    self.screen.blit(text_surface, text_rect)

    def draw_pieces(self) -> None:
        """draw the pieces based on the board_state and their current possition.

        Args:

        Returns:
            None:
        """
        for row in range(self.rows):
            for col in range(self.cols):
                piece_rect: pygame.Rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

                if (
                    self.board_state[self.row_col_switch(row)][self.row_col_switch(col)]
                    != "__"
                ):
                    self.screen.blit(
                        self.piece_images[
                            self.board_state[self.row_col_switch(row)][
                                self.row_col_switch(col)
                            ]
                        ],
                        piece_rect,
                    )

    def highlight_cell(self) -> None:
        """highlight selected cell with the highlight_color on the board.

        Args:

        Returns:
            None:
        """

        if self.selected_cell is not None:

            row, col = self.selected_cell
            if self.board_state[row][col][0] == self.turn_to_move:

                row, col = self.row_col_switch(row), self.row_col_switch(col)

                cell_rect: pygame.Rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                cell_surface = pygame.Surface((self.cell_size, self.cell_size))
                cell_surface.fill(self.highlight_color)
                cell_surface.set_alpha(150)
                self.screen.blit(cell_surface, cell_rect)

    def highlight_last_move(self) -> None:
        """highlight last_move on the board.

        Args:

        Returns:
            None:
        """
        if self.move_log:
            for cell in [self.move_log[-1].start_pos, self.move_log[-1].end_pos]:
                cell_rect: pygame.Rect = pygame.Rect(
                    self.row_col_switch(cell[1]) * self.cell_size,
                    self.row_col_switch(cell[0]) * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                cell_surface = pygame.Surface((self.cell_size, self.cell_size))
                cell_surface.fill(self.highlight_color)
                cell_surface.set_alpha(150)
                self.screen.blit(cell_surface, cell_rect)

    def highlight_valid_moves(self) -> None:
        """highlight valid moves for selected piece.

        Args:

        Returns:
            None:
        """
        if self.selected_piece is None:
            return

        possible_moves = get_possible_moves(
            self.board_state,
            self.selected_piece,
            self.turn_to_move,
            self.get_last_move(),
            self.castle_rights[self.turn_to_move],
        )

        for move in possible_moves:
            if is_valid(
                self.board_state,
                move,
                self.turn_to_move,
                self.king_possitions[self.turn_to_move],
            ):
                if move.is_castle:
                    move.update_end_pos()

                row, col = move.end_pos

                cell_rect: pygame.Rect = pygame.Rect(
                    self.row_col_switch(col) * self.cell_size,
                    self.row_col_switch(row) * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                cell_surface = pygame.Surface((self.cell_size, self.cell_size))
                cell_surface.fill(DARK_YELLOW)
                cell_surface.set_alpha(150)
                self.screen.blit(cell_surface, cell_rect)

    def pawn_promotion(self) -> str:
        """choose the promotion piece when the player is Human.

        Args:

        Returns:
            str:
        """
        pieces = (
            ["wN", "wB", "wR", "wQ"]
            if self.turn_to_move == "w"
            else ["bN", "bB", "bR", "bQ"]
        )
        piece = pieces[3]

        for i in range(4):
            piece_surface = self.piece_images[pieces[i]]
            piece_rect = pygame.Rect(
                (2 + i) * self.cell_size,
                4 * self.cell_size,
                self.cell_size,
                self.cell_size,
            )

            pygame.draw.rect(self.screen, self.background_color, piece_rect)
            self.screen.blit(piece_surface, piece_rect)
        pygame.display.update()

        piece_selected = False

        while not piece_selected:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col = (
                    mouse_pos[1] // self.cell_size,
                    mouse_pos[0] // self.cell_size,
                )

                if row == 4 and col in range(2, 6):
                    return pieces[col - 2]
        return piece

    def print_help(self) -> None:
        """show help menu on the screen.

        Args:

        Returns:
            None:
        """

        if not self.game_pause:
            return

        self.screen.fill(self.background_color)

        title_surface = self.text_font.render("Help Window", True, self.font_color)
        title_rect = title_surface.get_rect(
            center=(self.cell_size * 4, self.cell_size // 2)
        )

        help_surface = self.text_font.render(
            "h - show this help screen", True, self.font_color
        )
        help_rect = help_surface.get_rect(
            midleft=(self.cell_size // 2, 2 * self.cell_size)
        )

        view_surface = self.text_font.render(
            "v - change view (flip board)", True, self.font_color
        )
        view_rect = view_surface.get_rect(
            midleft=(self.cell_size // 2, 3 * self.cell_size)
        )

        undo_surface = self.text_font.render(
            "z - undo last move", True, self.font_color
        )
        undo_rect = undo_surface.get_rect(
            midleft=(self.cell_size // 2, 4 * self.cell_size)
        )

        reset_surface = self.text_font.render("r - reset board", True, self.font_color)
        reset_rect = reset_surface.get_rect(
            midleft=(self.cell_size // 2, 5 * self.cell_size)
        )

        notation_surface = self.text_font.render(
            "n - show notation log", True, self.font_color
        )
        notation_rect = notation_surface.get_rect(
            midleft=(self.cell_size // 2, 6 * self.cell_size)
        )

        self.screen.blit(title_surface, title_rect)
        self.screen.blit(help_surface, help_rect)
        self.screen.blit(view_surface, view_rect)
        self.screen.blit(undo_surface, undo_rect)
        self.screen.blit(reset_surface, reset_rect)
        self.screen.blit(notation_surface, notation_rect)

    def draw_game_results(self) -> None:
        """draw game_results on the screen if the game is over.

        Args:

        Returns:
            None:
        """
        if self.checkmate:
            winner = "White" if self.checks["b"] else "Black"
            checkmate_surface_1 = self.text_font.render(
                f"{winner} wins by Checkmate",
                True,
                self.font_color,
                self.background_color,
            )
            checkmate_rect_1 = checkmate_surface_1.get_rect(
                center=(self.cell_size * 4, self.cell_size * 4)
            )

            checkmate_surface_2 = self.text_font.render(
                f"{winner} wins by Checkmate", True, DARK_RED
            )
            checkmate_rect_2 = checkmate_surface_2.get_rect(
                center=(self.cell_size * 4 + 2, self.cell_size * 4 + 2)
            )
            self.screen.blit(checkmate_surface_1, checkmate_rect_1)
            self.screen.blit(checkmate_surface_2, checkmate_rect_2)
            if self.play_game_over_sound:
                self.play_game_over_sound = False
                self.game_end_sound.play()
            return

        if self.draw_status and self.draw_status_type is not None:
            draw_surface_1 = self.text_font.render(
                f"Draw by {self.draw_status_type}",
                True,
                self.font_color,
                self.background_color,
            )
            draw_rect_1 = draw_surface_1.get_rect(
                center=(self.cell_size * 4, self.cell_size * 4)
            )

            draw_surface_2 = self.text_font.render(
                f"Draw by {self.draw_status_type}", True, DARK_RED
            )
            draw_rect_2 = draw_surface_2.get_rect(
                center=(self.cell_size * 4 + 2, self.cell_size * 4 + 2)
            )
            self.screen.blit(draw_surface_1, draw_rect_1)
            self.screen.blit(draw_surface_2, draw_rect_2)
            if self.play_game_over_sound:
                self.play_game_over_sound = False
                self.game_end_sound.play()
            return

    def draw(self) -> None:
        """call all the draw methods.

        Args:

        Returns:
            None:
        """
        if not self.game_pause:
            self.draw_board()
            self.highlight_last_move()
            self.highlight_cell()
            self.highlight_valid_moves()
            self.draw_pieces()
            self.draw_game_results()

        pygame.display.update()

    def print_move_notations(self) -> None:
        """show notation log on the screen.

        Args:

        Returns:
            None:
        """

        if not self.game_pause:
            return
        if len(self.move_log) == 0:
            self.game_pause = not self.game_pause
            return

        move_list: list[str] = []
        move_count: int = 1
        for i in range(1, len(self.move_log), 2):
            move_list.append(
                f"{move_count}. {self.move_log[i-1].notation} {self.move_log[i].notation}  "
            )
            move_count += 1
        if len(self.move_log) % 2 != 0:
            move_list.append(f"{move_count}. {self.move_log[-1].notation}  ")

        self.screen.fill(self.background_color)
        opening_font: pygame.font.Font = pygame.font.Font(
            r"../res/fonts/calibrib.ttf", 25
        )
        opening_surface = opening_font.render(
            self.move_log[-1].opening_name, True, (0, 0, 0)
        )
        opening_rect = opening_surface.get_rect(
            center=(self.cell_size * 4, self.cell_size // 2)
        )
        self.screen.blit(opening_surface, opening_rect)

        initial_start_line_y = opening_rect.height + self.cell_size
        initial_start_line_x = self.cell_size // 2

        start_line_x = initial_start_line_x
        start_line_y = initial_start_line_y

        notation_font: pygame.font.Font = pygame.font.Font(
            r"../res/fonts/Times.TTF", 40
        )

        pressed_key: int | None = None

        while pressed_key is None:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                pressed_key = event.key

                if pressed_key == pygame.K_n:
                    self.game_pause = not self.game_pause
                    return
                if pressed_key == pygame.K_UP:
                    initial_start_line_y += self.cell_size // 2
                    opening_rect = opening_rect.move(0, self.cell_size // 2)

                if pressed_key == pygame.K_DOWN:
                    initial_start_line_y -= self.cell_size // 2
                    opening_rect = opening_rect.move(0, -self.cell_size // 2)

            start_line_x = initial_start_line_x
            start_line_y = initial_start_line_y

            self.screen.fill(self.background_color)

            self.screen.blit(opening_surface, opening_rect)
            for move in move_list:
                move_surface = notation_font.render(
                    move,
                    True,
                    (0, 0, 0),
                )

                if move_surface.get_width() + start_line_x > self.screen.get_width():
                    start_line_x = self.cell_size // 2
                    start_line_y += self.cell_size // 2

                move_rect = move_surface.get_rect(midleft=(start_line_x, start_line_y))

                self.screen.blit(move_surface, move_rect)

                start_line_x += move_rect.width

            pygame.display.update()

            pressed_key = None

    def set_game_type(self) -> None:
        """set players type for each side.

        Args:

        Returns:
            None:
        """

        title_1_surface = self.text_font.render("Welcome to GCAI", True, (0, 0, 0))
        title_1_rect = title_1_surface.get_rect(
            center=(self.cell_size * 4, self.cell_size // 2)
        )
        title_2_surface = self.text_font.render("Choose a Game Type", True, (0, 0, 0))
        title_2_rect = title_2_surface.get_rect(
            midtop=(
                (
                    title_1_rect.midbottom[0],
                    title_1_rect.midbottom[1] + self.cell_size // 2,
                )
            )
        )

        type_1_surface = self.text_font.render("1. Player Vs. Player", True, (0, 0, 0))
        type_1_rect = type_1_surface.get_rect(
            center=(
                self.cell_size * 4,
                self.cell_size * 4 - self.cell_size // 2,
            )
        )
        type_2_surface = self.text_font.render("2. Engine Vs. Engine", True, (0, 0, 0))
        type_2_rect = type_2_surface.get_rect(
            midtop=(
                type_1_rect.midbottom[0],
                type_1_rect.midbottom[1] + self.cell_size // 2,
            )
        )
        type_3_surface = self.text_font.render("3. Player Vs. Engine", True, (0, 0, 0))
        type_3_rect = type_3_surface.get_rect(
            midtop=(
                type_2_rect.midbottom[0],
                type_2_rect.midbottom[1] + self.cell_size // 2,
            )
        )

        border_1_rect = type_1_rect.inflate(20, 20)
        border_2_rect = type_2_rect.inflate(20, 20)
        border_3_rect = type_3_rect.inflate(20, 20)

        border_rects = [border_1_rect, border_2_rect, border_3_rect]

        rect_background_colors: list[tuple[int, int, int]] = [
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
        ]

        while self.game_type is None:

            rect_background_colors = [
                (0, 0, 0),
                (0, 0, 0),
                (0, 0, 0),
            ]

            self.screen.fill(self.background_color)

            self.screen.blit(title_1_surface, title_1_rect)
            self.screen.blit(title_2_surface, title_2_rect)

            mouse_pos = pygame.mouse.get_pos()

            for num, border_rect in enumerate(border_rects):
                if border_rect.collidepoint(mouse_pos):
                    rect_background_colors[num] = (173, 128, 45)

            for num, border_rect in enumerate(border_rects):
                pygame.draw.rect(
                    self.screen,
                    rect_background_colors[num],
                    border_rect,
                    width=3,
                    border_radius=15,
                )

            self.screen.blit(type_1_surface, type_1_rect)
            self.screen.blit(type_2_surface, type_2_rect)
            self.screen.blit(type_3_surface, type_3_rect)

            pygame.display.update()

            key = None
            click = False
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                click = True

            if event.type == pygame.KEYDOWN:
                key = event.key
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if key == pygame.K_1 or (click and border_1_rect.collidepoint(mouse_pos)):
                self.game_type = 1
                self.players = {"w": "Human", "b": "Human"}
                self.game_start_sound.play()
                return

            if key == pygame.K_2 or (click and border_2_rect.collidepoint(mouse_pos)):
                self.game_type = 2
                self.players = {"w": "AI", "b": "AI"}
                self.game_start_sound.play()
                return

            if key == pygame.K_3 or (click and border_3_rect.collidepoint(mouse_pos)):
                self.game_type = 3
                self.set_players()
                self.game_start_sound.play()

    def set_players(self) -> None:
        """set the color for player if game type is Player vs. Engine.

        Args:

        Returns:
            None:
        """

        title_surface = self.text_font.render("Choose a Color", True, (0, 0, 0))
        title_rect = title_surface.get_rect(
            center=(self.cell_size * 4, self.cell_size // 2)
        )
        type_1_surface = self.text_font.render("1. White", True, (0, 0, 0))
        type_1_rect = type_1_surface.get_rect(
            center=(
                self.cell_size * 4,
                self.cell_size * 4 - self.cell_size // 2,
            )
        )
        type_2_surface = self.text_font.render("2. Black", True, (0, 0, 0))
        type_2_rect = type_2_surface.get_rect(
            midtop=(
                type_1_rect.midbottom[0],
                type_1_rect.midbottom[1] + self.cell_size // 2,
            )
        )
        type_3_surface = self.text_font.render("3. Random", True, (0, 0, 0))
        type_3_rect = type_3_surface.get_rect(
            midtop=(
                type_2_rect.midbottom[0],
                type_2_rect.midbottom[1] + self.cell_size // 2,
            )
        )

        border_1_rect = type_1_rect.inflate(20, 20)
        border_2_rect = type_2_rect.inflate(20, 20)
        border_3_rect = type_3_rect.inflate(20, 20)

        border_rects = [border_1_rect, border_2_rect, border_3_rect]

        rect_background_colors: list[tuple[int, int, int]] = [
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
        ]

        while self.players is None:

            rect_background_colors = [
                (0, 0, 0),
                (0, 0, 0),
                (0, 0, 0),
            ]

            self.screen.fill(self.background_color)

            self.screen.blit(title_surface, title_rect)

            mouse_pos = pygame.mouse.get_pos()

            for num, border_rect in enumerate(border_rects):
                if border_rect.collidepoint(mouse_pos):
                    rect_background_colors[num] = (173, 128, 45)

            for num, border_rect in enumerate(border_rects):
                pygame.draw.rect(
                    self.screen,
                    rect_background_colors[num],
                    border_rect,
                    width=3,
                    border_radius=15,
                )

            self.screen.blit(type_1_surface, type_1_rect)
            self.screen.blit(type_2_surface, type_2_rect)
            self.screen.blit(type_3_surface, type_3_rect)

            pygame.display.update()

            key = None
            click = False
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                click = True
            if event.type == pygame.KEYDOWN:
                key = event.key
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if key == pygame.K_1 or (click and border_1_rect.collidepoint(mouse_pos)):
                self.players = {"w": "Human", "b": "AI"}
                self.view = "w"
                return
            if key == pygame.K_2 or (click and border_2_rect.collidepoint(mouse_pos)):
                self.players = {"w": "AI", "b": "Human"}
                self.view = "b"
                return
            if key == pygame.K_3 or (click and border_3_rect.collidepoint(mouse_pos)):
                white_side = choice(["Human", "AI"])
                black_side = "Human" if white_side == "AI" else "AI"
                self.players = {"w": white_side, "b": black_side}
                self.view = "w" if white_side == "Human" else "b"
                return

    def reset_board(self) -> None:
        """reset the game.

        Args:

        Returns:
            None:
        """
        if self.game_pause:
            return

        self.board_state: list[list[str]] = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.selected_cell = None
        self.selected_piece = None
        self.turn_to_move = "w"
        self.view = "w"
        self.king_possitions = {"w": (7, 4), "b": (0, 4)}

        self.castle_rights = {
            "w": {"short": True, "long": True},
            "b": {"short": True, "long": True},
        }

        self.checks = {"w": False, "b": False}

        self.checkmate = False
        self.stalemate = False
        self.draw_status = False
        self.draw_status_type = None
        self.fifty_move_rule = 0
        self.move_log.clear()
        self.new_move = True

        self.game_type = None
        self.players = None

        self.play_game_over_sound = True

        with open(r"./packages/utils/openings_list.json", "r") as openings_data_file:
            self.openings = json.load(openings_data_file)
        self.initialize_board_hash()

        self.set_game_type()

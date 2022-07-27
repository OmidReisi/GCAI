from ..utils.colors import RGB_Color, DARK_YELLOW
from ..move import Move
from ..logics import (
    get_possible_moves,
    possition_under_attack,
    is_valid,
    any_valid_moves,
)

from typing import Literal

import sys
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
        """Initializing a board with the given number of rows and cols and the defined cell_size and setting the initial_state of the board.

        Args:
            cell_size (int): cell_size
            rows (int): rows
            cols (int): cols
            dark_color (RGB_Color): dark_color
            light_color (RGB_Color): light_color

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

        self.screen: pygame.surface.Surface = pygame.display.set_mode(
            (self.rows * self.cell_size, self.cols * self.cell_size)
        )

        self.help_window_active: bool = False

        # initial_state of the board and how the pieces are set up. ("__" shows the empty cells)
        self.initial_state: list[list[str]] = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

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

        self.board_state: list[list[str]] = self.initial_state

        self.view: str = "w"

        self.king_possitions: dict[str, tuple[int, int]] = {"w": (7, 4), "b": (0, 4)}

        self.castle_rights: dict[str, dict[str, bool]] = {
            "w": {"short": True, "long": True},
            "b": {"short": True, "long": True},
        }

        self.checks: dict[str, bool] = {"w": False, "b": False}

        self.checkmate: bool = False
        self.stalemate: bool = False

        self.turn_to_move: Literal["w", "b"] = "w"

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
        self.new_move: bool = False

        self.piece_images: dict[str, pygame.surface.Surface] = {}

        self.load_piece_images()

        self.selected_cell: tuple[int, int] | None = None
        self.selected_piece: tuple[int, int] | None = None

        pygame.display.set_caption("Chess Game")

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
        if self.view == "w":
            return row_col
        return 7 - row_col

    def set_selected_cell(self, pos: tuple[int, int]) -> None:

        selected_cell = (
            self.row_col_switch(pos[1] // self.cell_size),
            self.row_col_switch(pos[0] // self.cell_size),
        )
        self.selected_cell = (
            None if self.selected_cell == selected_cell else selected_cell
        )

    def set_selected_piece(self) -> None:

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
        self.turn_to_move = "w" if self.turn_to_move == "b" else "b"

    def switch_view(self) -> None:
        if self.help_window_active:
            return

        self.view = "w" if self.view == "b" else "b"
        self.selected_cell = None

    def set_checkmate_stalemate(self) -> None:
        if not self.new_move:
            return
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
            print("checkmate")
        else:
            self.stalemate = True
            print("stalemate")

    def get_last_move(self) -> Move | None:
        if len(self.move_log) == 0:
            return None
        return self.move_log[-1]

    def make_move(self, move: Move) -> None:
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

                if move.moved_piece[1] not in ["P", "K"]:
                    for row in range(8):
                        if (
                            self.board_state[row][move.start_pos[1]] == move.moved_piece
                            and row != move.start_pos[0]
                        ):
                            moves_to_check = get_possible_moves(
                                self.board_state,
                                (row, move.start_pos[1]),
                                self.turn_to_move,
                                self.get_last_move(),
                                self.castle_rights[self.turn_to_move],
                            )
                            for check_move in moves_to_check:
                                if move.end_pos == check_move.end_pos:
                                    move.row_col_notation = str(
                                        self.row_to_rank[move.start_pos[0]]
                                    )
                                    break
                            if move.row_col_notation != "":
                                break
                    for col in range(8):
                        if (
                            self.board_state[move.start_pos[0]][col] == move.moved_piece
                            and col != move.start_pos[1]
                        ):
                            moves_to_check = get_possible_moves(
                                self.board_state,
                                (move.start_pos[0], col),
                                self.turn_to_move,
                                self.get_last_move(),
                                self.castle_rights[self.turn_to_move],
                            )
                            for check_move in moves_to_check:
                                if move.end_pos == check_move.end_pos:
                                    move.row_col_notation = self.col_to_file[
                                        move.start_pos[1]
                                    ]
                                    break
                            if move.row_col_notation != "":
                                break

                #
                # last_available_move: Move = available_moves[-1]
                #
                # if move == last_available_move:
                #
                #     if (
                #         move == last_available_move
                #         and last_available_move.is_en_passant
                #     ):
                #         move.set_en_passant()
                #         move.set_en_passant_pos(last_available_move.en_passant_pos)
                #
                temp_board_state: list[list[str]] = [
                    list_item.copy() for list_item in self.board_state
                ]
                if move.is_castle:
                    move.update_end_pos()

                p_row, p_col = move.start_pos

                temp_board_state[p_row][p_col] = "__"
                s_row, s_col = move.end_pos
                temp_board_state[s_row][s_col] = (
                    self.pawn_promotion()
                    if move.is_pawn_promotion
                    else move.moved_piece
                )
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

                    self.update_move_log(move)
                    self.new_move = True

            self.selected_cell = None
            self.selected_piece = None

    def undo_move(self) -> None:
        if self.help_window_active:
            return

        self.new_move = True
        if self.move_log:
            move = self.move_log.pop()
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

    def get_file_rank(self, pos: tuple[int, int]) -> str:

        return f"{self.col_to_file[pos[1]]}{self.row_to_rank[pos[0]]}"

    def update_move_log(self, move: Move) -> None:
        self.move_log.append(move)

    def update_board_state(self, pos: tuple[int, int]):
        if self.help_window_active:
            return
        self.set_selected_cell(pos)
        self.set_selected_piece()
        self.make_move(
            Move(
                self.selected_piece,
                self.selected_cell,
                self.board_state,
                self.turn_to_move,
            )
        )
        self.set_checkmate_stalemate()

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

        self.screen.blit(title_surface, title_rect)
        self.screen.blit(help_surface, help_rect)
        self.screen.blit(view_surface, view_rect)
        self.screen.blit(undo_surface, undo_rect)
        self.screen.blit(reset_surface, reset_rect)

    def draw(self) -> None:
        """calling the draw_board(), highlight_cell(), highlight_last_move(), draw_pieces() respectively.

        Args:

        Returns:
            None:
        """
        if not self.help_window_active:
            self.draw_board()
            self.highlight_last_move()
            self.highlight_cell()
            self.highlight_valid_moves()
            self.draw_pieces()

        else:
            self.print_help()

        pygame.display.update()

    def print_move_notations(self):
        for move in self.move_log:
            print(move.notation)

    def reset_board(self) -> None:
        if self.help_window_active:
            return

        self.board_state = self.initial_state
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
        self.move_log = []

from ..utils.colors import RGB_Color
from ..move import Move
from ..logics import get_possible_moves

from typing import Literal

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
        self.font: pygame.font.Font = pygame.font.Font(
            r"../res/fonts/ChessMeridaUnicode.ttf", 30
        )
        self.font_color: RGB_Color = font_color
        self.screen: pygame.surface.Surface = pygame.display.set_mode(
            (self.rows * self.cell_size, self.cols * self.cell_size)
        )

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

        self.board_state = self.initial_state

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

    def set_selected_cell(self, pos: tuple[int, int]) -> None:
        selected_cell = (pos[1] // self.cell_size, pos[0] // self.cell_size)
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
                if (
                    self.board_state[p_row][p_col][0]
                    == self.board_state[s_row][s_col][0]
                ):
                    self.selected_piece = self.selected_cell

        else:
            self.selected_piece = None

    def switch_turn(self) -> None:
        self.turn_to_move = "w" if self.turn_to_move == "b" else "b"

    def make_move(self, move: Move) -> None:
        if (move.start_pos is not None and move.end_pos is not None) and (
            move.start_pos != move.end_pos
        ):

            if move in get_possible_moves(
                self.board_state, move.start_pos, self.turn_to_move
            ):

                p_row, p_col = move.start_pos
                self.board_state[p_row][p_col] = "__"
                s_row, s_col = move.end_pos
                self.board_state[s_row][s_col] = move.moved_piece

                self.update_move_log(move)

                self.switch_turn()

            self.selected_cell = None
            self.selected_piece = None

    def undo_move(self) -> None:
        if self.move_log:
            move = self.move_log.pop()
            s_row, s_col = move.start_pos
            e_row, e_col = move.end_pos
            self.board_state[s_row][s_col] = move.moved_piece
            self.board_state[e_row][e_col] = move.captured_piece

            self.switch_turn()

    def get_file_rank(self, pos: tuple[int, int]) -> str:

        return f"{self.col_to_file[pos[1]]}{self.row_to_rank[pos[0]]}"

    def update_move_log(self, move: Move) -> None:
        self.move_log.append(move)

    def update_board_state(self, pos: tuple[int, int]):
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
                    text_surface = self.font.render(
                        (self.col_to_file[col]), True, self.font_color
                    )

                    text_rect = text_surface.get_rect(bottomright=cell_rect.bottomright)
                    self.screen.blit(text_surface, text_rect)

                if col == 0:
                    text_surface = self.font.render(
                        str(self.row_to_rank[row]), True, self.font_color
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

                if self.board_state[row][col] != "__":
                    self.screen.blit(
                        self.piece_images[self.board_state[row][col]], piece_rect
                    )

    def highlight_cell(self) -> None:

        if self.selected_cell is not None:

            cell_rect: pygame.Rect = pygame.Rect(
                self.selected_cell[1] * self.cell_size,
                self.selected_cell[0] * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            pygame.draw.rect(self.screen, self.highlight_color, cell_rect)

    def highlight_last_move(self) -> None:
        if self.move_log:
            for cell in [self.move_log[-1].start_pos, self.move_log[-1].end_pos]:
                cell_rect: pygame.Rect = pygame.Rect(
                    cell[1] * self.cell_size,
                    cell[0] * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, self.highlight_color, cell_rect)

    def draw(self) -> None:
        """calling the draw_board(), highlight_cell(), highlight_last_move(), draw_pieces() respectively.

        Args:

        Returns:
            None:
        """
        self.draw_board()
        self.highlight_last_move()
        self.highlight_cell()
        self.draw_pieces()
        pygame.display.update()
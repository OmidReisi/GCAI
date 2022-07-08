from ..utils.colors import RGB_Color

import pygame
import numpy as np

pygame.init()


class Board:
    def __init__(
        self,
        cell_size: int,
        rows: int,
        cols: int,
        dark_color: RGB_Color,
        light_color: RGB_Color,
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
        self.screen: pygame.surface.Surface = pygame.display.set_mode(
            (self.rows * self.cell_size, self.cols * self.cell_size)
        )

        # initial_state of the board and how the pieces are set up. ("__" shows the empty cells)
        self.initial_state: np.ndarray = np.array(
            [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                ["__", "__", "__", "__", "__", "__", "__", "__"],
                ["__", "__", "__", "__", "__", "__", "__", "__"],
                ["__", "__", "__", "__", "__", "__", "__", "__"],
                ["__", "__", "__", "__", "__", "__", "__", "__"],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ]
        )

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

        self.piece_images: dict[str, pygame.surface.Surface] = {}

        self.load_piece_images()

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

                if self.board_state[row, col] != "__":
                    self.screen.blit(
                        self.piece_images[self.board_state[row, col]], piece_rect
                    )

    def draw(self) -> None:
        """calling the draw_board() and draw_pieces() methods

        Args:

        Returns:
            None:
        """
        self.draw_board()
        self.draw_pieces()

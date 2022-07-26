from packages.utils.colors import (
    RGB_Color,
    BEIGE,
    BROWN,
    LIGHT_GREEN,
    BLACK,
    LIGHT_GREY,
)
from packages.board import Board

import sys
import pygame

pygame.init()


def main() -> None:
    game_run: bool = True
    board: Board = Board(120, 8, 8, BROWN, BEIGE, LIGHT_GREEN, BLACK, LIGHT_GREY)
    clock: pygame.time.Clock = pygame.time.Clock()

    while game_run:

        board.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.update_board_state(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    board.undo_move()
                if event.key == pygame.K_v:
                    board.switch_view()
                if event.key == pygame.K_r:
                    board.reset_board()

        clock.tick(60)


if __name__ == "__main__":
    main()

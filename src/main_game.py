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

# initalize pygame library
pygame.init()


def main() -> None:
    """main game funcion

    Args:

    Returns:
        None:
    """
    game_run: bool = True

    # create a board for the game
    board: Board = Board(120, 8, 8, BROWN, BEIGE, LIGHT_GREEN, BLACK, LIGHT_GREY)
    # define a clock for game fps
    clock: pygame.time.Clock = pygame.time.Clock()

    board.set_game_type()

    # game's main loop
    while game_run:

        board.draw()
        board.update_board_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.set_selected_cell(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    board.undo_move()
                if event.key == pygame.K_v:
                    board.switch_view()
                if event.key == pygame.K_r:
                    board.reset_board()
                if event.key == pygame.K_n:
                    board.game_pause = not board.game_pause
                    board.print_move_notations()
                if event.key == pygame.K_h:
                    board.game_pause = not board.game_pause
                    board.print_help()

        # maximum fps
        clock.tick(60)


# run the main funcion if the script ir ran directly
if __name__ == "__main__":
    main()

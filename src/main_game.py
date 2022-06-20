from packages.utils.colors import RGB_Color, BEIGE, BROWN
from packages.board.board_setup import BoardSetup

import sys
import pygame


def main() -> None:
    pygame.init()
    board: BoardSetup = BoardSetup(60, 8, 8, BROWN, BEIGE)
    board.draw()

    game_run: bool = True
    clock: pygame.time.Clock = pygame.time.Clock()

    while game_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()

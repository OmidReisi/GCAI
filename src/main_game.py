from packages.utils.colors import RGB_Color, BEIGE, BROWN
from packages.board import Board

import sys
import pygame

pygame.init()


def main() -> None:
    game_run: bool = True
    board: Board = Board(60, 8, 8, BROWN, BEIGE)
    clock: pygame.time.Clock = pygame.time.Clock()

    while game_run:

        board.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()

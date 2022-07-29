from ..move import Move

from random import choice


def get_random_move(move_list: list[Move]) -> Move | None:
    if len(move_list) == 0:
        return None
    return choice(move_list)

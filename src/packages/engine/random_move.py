from ..move import Move

from random import choice


def get_random_move(move_list: list[Move], is_opening_move: bool) -> Move | None:
    if len(move_list) == 0:
        return None
    return (choice(move_list), is_opening_move)

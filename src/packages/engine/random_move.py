from ..move import Move

from random import choice


def get_random_move(move_list: list[Move]) -> Move | None:
    """return a random move from the move list.

    Args:
        move_list (list[Move]): move_list

    Returns:
        Move | None:
    """
    if len(move_list) == 0:
        return None
    return choice(move_list)

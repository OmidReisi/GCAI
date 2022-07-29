from ..move import Move
from ..logics import get_possible_moves, is_valid

from random import choice


def get_random_move(
    board_state: list[list[str]],
    turn_to_move: str,
    king_pos: tuple[int, int],
    castle_rights: dict[str, bool],
    last_move: Move | None,
) -> Move | None:

    possible_moves: list[Move] = []
    valid_moves: list[Move] = []
    for row in range(8):
        for col in range(8):
            possible_moves += get_possible_moves(
                board_state, (row, col), turn_to_move, last_move, castle_rights
            )
    for move in possible_moves:
        if is_valid(board_state, move, turn_to_move, king_pos):
            valid_moves.append(move)
    if len(valid_moves) == 0:
        return None
    return choice(valid_moves)

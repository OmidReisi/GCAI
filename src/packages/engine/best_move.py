from .engine_move import make_move, get_switched_turn
from .move_evaluation import get_move_evaluation
from .random_move import get_random_move
from ..move import Move
from ..logics import get_valid_moves


def get_best_move(
    valid_moves: list[Move],
    board_state: list[list[str]],
    turn_to_move: str,
    king_pos: tuple[int, int],
    castle_rights: dict[str, bool],
    opponent_king_pos: tuple[int, int],
    opponent_castle_rights: dict[str, bool],
    depth: int,
) -> Move | None:

    best_moves: list[Move] = []

    min_max_eval = 1000 if turn_to_move == "b" else -1000

    if len(valid_moves) == 0:
        return None

    for move in valid_moves:

        move_eval = get_move_evaluation(
            board_state,
            turn_to_move,
            move,
            king_pos,
            castle_rights,
            opponent_king_pos,
            opponent_castle_rights,
            depth,
        )

        if turn_to_move == "b" and move_eval < min_max_eval:
            best_moves = [move]
            min_max_eval = move_eval
        elif turn_to_move == "w" and move_eval > min_max_eval:
            best_moves = [move]
            min_max_eval = move_eval

        elif move_eval == min_max_eval:
            best_moves.append(move)

    return get_random_move(best_moves)

from .move_evaluation import get_move_evaluation
from .random_move import get_random_move
from ..move import Move


def get_best_move(
    valid_moves: list[Move],
    board_state: list[list[str]],
    turn_to_move: str,
    opponent_king_pos: tuple[int, int],
    opponent_castle_rights: dict[str, bool],
) -> Move | None:
    if len(valid_moves) == 0:
        return None
    max_eval = -1000
    turn_evaluation = 1 if turn_to_move == "w" else -1
    best_moves: list[Move] = []

    for move in valid_moves:
        move_eval = turn_evaluation * get_move_evaluation(
            board_state, turn_to_move, move, opponent_king_pos, opponent_castle_rights
        )
        if move_eval > max_eval:
            best_moves = [move]
            max_eval = move_eval
        elif move_eval == max_eval:
            best_moves.append(move)
    return get_random_move(best_moves)

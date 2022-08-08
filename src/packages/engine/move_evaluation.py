from .board_evaluation import get_minimax_evaluation
from .engine_move import get_switched_turn, get_castle_rights, get_king_pos, make_move
from ..move import Move


def get_move_evaluation(
    move_to_make: Move,
    board_state: list[list[str]],
    turn_to_move: str,
    king_pos: tuple[int, int],
    castle_rights: dict[str, bool],
    opponent_king_pos: tuple[int, int],
    opponent_castle_rights: dict[str, bool],
    alpha: float,
    beta: float,
    depth: int,
) -> tuple[float, float, float]:
    generated_board_state = make_move(board_state, turn_to_move, move_to_make)

    if move_to_make.is_castle:
        move_to_make.update_end_pos()

    king_pos = get_king_pos(move_to_make, king_pos)
    temp_castle_rights = get_castle_rights(move_to_make, castle_rights)

    return get_minimax_evaluation(
        generated_board_state,
        get_switched_turn(turn_to_move),
        opponent_king_pos,
        opponent_castle_rights,
        king_pos,
        temp_castle_rights,
        move_to_make,
        alpha,
        beta,
        depth,
    )

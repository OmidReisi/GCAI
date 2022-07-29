from .board_evaluation import get_board_evaluation
from .engine_move import get_switched_turn, make_move
from ..move import Move
from ..logics import any_valid_moves, possition_under_attack


def get_move_evaluation(
    board_state: list[list[str]],
    turn_to_move: str,
    move: Move,
    opponent_king_pos: tuple[int, int],
    opponent_castle_rights: dict[str, bool],
) -> int:
    turn_evaluation: int = 1 if turn_to_move == "w" else -1
    is_check: bool = False

    board_eval = get_board_evaluation(board_state)

    temp_board_state = make_move(board_state, turn_to_move, move)

    current_board_eval = get_board_evaluation(temp_board_state)

    move_evaluation = current_board_eval - board_eval

    turn_to_move = get_switched_turn(turn_to_move)

    if possition_under_attack(temp_board_state, opponent_king_pos, turn_to_move):
        is_check = True

    if not any_valid_moves(
        board_state, turn_to_move, opponent_king_pos, move, opponent_castle_rights
    ):
        if is_check:
            return turn_evaluation * 1000
        return 0

    if is_check:
        return move_evaluation + 1 * turn_evaluation
    return move_evaluation

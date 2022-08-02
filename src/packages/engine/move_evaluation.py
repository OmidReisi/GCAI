from .board_evaluation import get_board_evaluation
from .engine_move import get_switched_turn, get_castle_rights, get_king_pos, make_move
from .random_move import get_random_move
from ..move import Move
from ..logics import any_valid_moves, get_valid_moves, possition_under_attack


def get_move_evaluation(
    board_state: list[list[str]],
    turn_to_move: str,
    move: Move | None,
    king_pos: tuple[int, int],
    castle_rights: dict[str, bool],
    opponent_king_pos: tuple[int, int],
    opponent_castle_rights: dict[str, bool],
    depth: int,
) -> int:

    if move is None:
        return 0

    turn_evaluation: int = 1 if turn_to_move == "w" else -1
    is_check: bool = False

    if depth <= 0:
        return 0

    board_eval = get_board_evaluation(board_state)

    if move.is_castle:
        move.update_end_pos()

    opponent_board_state = make_move(board_state, turn_to_move, move)

    king_pos = get_king_pos(move, king_pos)
    temp_castle_rights = get_castle_rights(move, castle_rights)

    current_board_eval = get_board_evaluation(opponent_board_state)

    move_evaluation = current_board_eval - board_eval

    opponent_turn = get_switched_turn(turn_to_move)

    if possition_under_attack(opponent_board_state, opponent_king_pos, opponent_turn):
        is_check = True

    if not any_valid_moves(
        opponent_board_state,
        opponent_turn,
        opponent_king_pos,
        move,
        opponent_castle_rights,
    ):
        if is_check:
            return turn_evaluation * 1000

        return 0

    if is_check:
        current_move_eval = move_evaluation + 1 * turn_evaluation

    else:
        current_move_eval = move_evaluation

    opponent_valid_moves = get_valid_moves(
        opponent_board_state,
        opponent_turn,
        opponent_king_pos,
        opponent_castle_rights,
        move,
    )

    opponent_max_eval = -1000
    opponent_turn_eval = -1 * turn_evaluation

    for opponent_move in opponent_valid_moves:
        opponent_move_eval = get_move_evaluation(
            opponent_board_state,
            opponent_turn,
            opponent_move,
            opponent_king_pos,
            opponent_castle_rights,
            king_pos,
            temp_castle_rights,
            depth - 1,
        )
        if opponent_turn_eval * opponent_move_eval > opponent_max_eval:
            opponent_max_eval = opponent_move_eval * opponent_turn_eval

    return current_move_eval + opponent_max_eval * opponent_turn_eval


# def get_move_evaluation(
#     board_state: list[list[str]],
#     turn_to_move: str,
#     move: Move | None,
#     king_pos: tuple[int, int],
#     castle_rights: dict[str, bool],
#     opponent_king_pos: tuple[int, int],
#     opponent_castle_rights: dict[str, bool],
#     depth: int,
# ) -> int:
#
#     if move is None:
#         return 0
#
#     turn_evaluation: int = 1 if turn_to_move == "w" else -1
#     is_check: bool = False
#
#     if depth == 0:
#         return 0
#
#     board_eval = get_board_evaluation(board_state)
#
#     if move.is_castle:
#         move.update_end_pos()
#
#     temp_board_state = make_move(board_state, turn_to_move, move)
#
#     king_pos = get_king_pos(move, king_pos)
#     temp_castle_rights = get_castle_rights(move, castle_rights)
#
#     current_board_eval = get_board_evaluation(temp_board_state)
#
#     move_evaluation = current_board_eval - board_eval
#
#     opponent_turn = get_switched_turn(turn_to_move)
#
#     if possition_under_attack(temp_board_state, opponent_king_pos, opponent_turn):
#         is_check = True
#
#     if not any_valid_moves(
#         board_state, opponent_turn, opponent_king_pos, move, opponent_castle_rights
#     ):
#         if is_check:
#             return turn_evaluation * 1000
#
#         return 0
#
#     if is_check:
#         current_move_eval = move_evaluation + 1 * turn_evaluation
#
#     else:
#         current_move_eval = move_evaluation
#
#     opponent_valid_moves = get_valid_moves(
#         temp_board_state, opponent_turn, opponent_king_pos, opponent_castle_rights, move
#     )
#
#     opponent_best_move = get_best_move(
#         opponent_valid_moves,
#         temp_board_state,
#         opponent_turn,
#         opponent_king_pos,
#         opponent_castle_rights,
#         king_pos,
#         temp_castle_rights,
#         depth - 1,
#     )
#
#     return current_move_eval + get_move_evaluation(
#         temp_board_state,
#         opponent_turn,
#         opponent_best_move,
#         opponent_king_pos,
#         opponent_castle_rights,
#         king_pos,
#         temp_castle_rights,
#         depth - 1,
#     )
#
#

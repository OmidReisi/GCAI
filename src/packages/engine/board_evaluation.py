from ..move import Move
from ..logics import any_valid_moves, get_valid_moves, possition_under_attack
from .engine_move import get_switched_turn, get_castle_rights, get_king_pos, make_move


def get_board_evaluation(
    board_state: list[list[str]],
    turn_to_move: str,
    king_pos: tuple[int, int],
    castle_rights: dict[str, bool],
    last_move: Move | None,
) -> tuple[float, bool]:

    checkmate_index = -1 if turn_to_move == "w" else 1

    check: bool = False

    if possition_under_attack(board_state, king_pos, turn_to_move):
        check = True

    if not any_valid_moves(
        board_state, turn_to_move, king_pos, last_move, castle_rights
    ):
        if check:
            return (1000 * checkmate_index, True)

        return (0, True)

    piece_evaluation: dict[str, int] = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
    evaluation: int = 0

    for row in range(8):
        for col in range(8):
            piece = board_state[row][col]
            if piece[0] == "w":
                evaluation += piece_evaluation[piece[1]]
            elif piece[0] == "b":
                evaluation -= piece_evaluation[piece[1]]

    return (evaluation, False)


def get_minimax_evaluation(
    board_state: list[list[str]],
    turn_to_move: str,
    king_pos: tuple[int, int],
    castle_rights: dict[str, bool],
    opponent_king_pos: tuple[int, int],
    opponent_castle_rights: dict[str, bool],
    last_move: Move | None,
    alpha: float,
    beta: float,
    depth: float,
) -> tuple[float, float, float]:

    current_board_eval = get_board_evaluation(
        board_state, turn_to_move, king_pos, castle_rights, last_move
    )

    if depth == 0 or current_board_eval[1]:
        return (current_board_eval[0] * depth, alpha, beta)

    opponent_turn = get_switched_turn(turn_to_move)

    valid_moves = get_valid_moves(
        board_state, turn_to_move, king_pos, castle_rights, last_move
    )

    if turn_to_move == "w":
        max_eval = -float("inf")
        for move in valid_moves:
            opponent_board_state = make_move(board_state, turn_to_move, move)

            king_pos = get_king_pos(move, king_pos)
            temp_castle_rights = get_castle_rights(move, castle_rights)
            board_eval = get_minimax_evaluation(
                opponent_board_state,
                opponent_turn,
                opponent_king_pos,
                opponent_castle_rights,
                king_pos,
                temp_castle_rights,
                move,
                alpha,
                beta,
                depth - 1,
            )
            max_eval = max(max_eval, board_eval[0])
            alpha = max(alpha, board_eval[0])
            if beta <= alpha:
                break
        return (max_eval, alpha, beta)

    if turn_to_move == "b":
        min_eval = float("inf")
        for move in valid_moves:
            opponent_board_state = make_move(board_state, turn_to_move, move)

            king_pos = get_king_pos(move, king_pos)
            temp_castle_rights = get_castle_rights(move, castle_rights)
            board_eval = get_minimax_evaluation(
                opponent_board_state,
                opponent_turn,
                opponent_king_pos,
                opponent_castle_rights,
                king_pos,
                temp_castle_rights,
                move,
                alpha,
                beta,
                depth - 1,
            )
            min_eval = min(min_eval, board_eval[0])
            beta = min(beta, board_eval[0])
            if beta <= alpha:
                break
        return (min_eval, alpha, beta)

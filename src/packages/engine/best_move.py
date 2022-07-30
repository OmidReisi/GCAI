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
) -> Move | None:
    if len(valid_moves) == 0:
        return None
    initial_king_pos = king_pos
    opponent_turn = get_switched_turn(turn_to_move)
    max_eval = -1000
    opponent_max_eval = -1000
    turn_evaluation = 1 if turn_to_move == "w" else -1
    opponent_turn_evaluation = -turn_evaluation
    best_moves: list[Move] = []

    # for move in valid_moves:
    #     move_eval = turn_evaluation * get_move_evaluation(
    #         board_state, turn_to_move, move, opponent_king_pos, opponent_castle_rights
    #     )
    #     if move_eval > max_eval:
    #         best_moves = [move]
    #         max_eval = move_eval
    #     elif move_eval == max_eval:
    #         best_moves.append(move)
    # return get_random_move(best_moves)

    for move in valid_moves:
        king_pos = initial_king_pos
        opponent_max_eval = -1000

        move_eval = turn_evaluation * get_move_evaluation(
            board_state, turn_to_move, move, opponent_king_pos, opponent_castle_rights
        )
        opponent_board_state = make_move(board_state, turn_to_move, move)
        opponent_valid_moves = get_valid_moves(
            opponent_board_state,
            opponent_turn,
            opponent_king_pos,
            opponent_castle_rights,
            move,
        )
        if move.is_castle:
            move.update_end_pos()
        king_pos = move.end_pos if move.moved_piece[1] == "K" else king_pos

        for opponent_move in opponent_valid_moves:
            opponent_move_eval = opponent_turn_evaluation * get_move_evaluation(
                opponent_board_state,
                opponent_turn,
                opponent_move,
                king_pos,
                castle_rights,
            )
            if opponent_move_eval > opponent_max_eval:
                opponent_max_eval = opponent_move_eval

        if move_eval - opponent_max_eval > max_eval:
            best_moves = [move]
            max_eval = move_eval - opponent_max_eval
        elif move_eval - opponent_max_eval == max_eval:
            best_moves.append(move)

    return get_random_move(best_moves)

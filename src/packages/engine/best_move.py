from .move_evaluation import get_move_evaluation
from .random_move import get_random_move
from ..move import Move


def get_best_move(
    valid_moves: list[Move],
    board_state: list[list[str]],
    turn_to_move: str,
    king_pos: tuple[int, int],
    castle_rights: dict[str, bool],
    opponent_king_pos: tuple[int, int],
    opponent_castle_rights: dict[str, bool],
    openings: list[dict[str, str | list[str]]],
    opening_index: int,
    last_move: Move | None,
    depth: int,
) -> tuple[Move | None, bool]:

    best_moves: list[Move] = []

    min_max_eval = float("inf") if turn_to_move == "b" else -float("inf")

    if len(valid_moves) == 0:
        print("no valid move")
        return None

    if len(openings) != 0:
        move_list: list[Move] = []
        for opening in openings:
            if len(opening["moves"]) > opening_index:
                move_to_add = Move.from_notation(
                    opening["moves"][opening_index],
                    board_state,
                    turn_to_move,
                    last_move,
                    castle_rights,
                    king_pos,
                )
                if move_to_add is not None:
                    move_list.append(move_to_add)

        if len(move_list) > 0:
            return get_random_move(move_list, True)
        print("error no opening move")

    for move in valid_moves:

        move_eval = get_move_evaluation(
            move,
            board_state,
            turn_to_move,
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

    return get_random_move(best_moves, False)

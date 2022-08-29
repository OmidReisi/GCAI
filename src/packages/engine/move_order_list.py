from ..move import Move
from ..utils.piece_square_tables import piece_evaluation

# from .square_evaluation import get_piece_square_evaluation


def get_move_order_list(
    move_list: list[Move], turn_to_move: str, game_stage: str, board_eval: float
) -> list[Move]:
    evaluation_index = 1 if turn_to_move == "w" else -1
    move_value_list: list[tuple[int, float]] = []

    for index, move in enumerate(move_list):
        if move is None:
            continue

        capture_score = 0

        start_pos_score = evaluation_index * piece_evaluation[move.moved_piece[1]]

        if move.is_pawn_promotion:

            end_pos_score = evaluation_index * piece_evaluation[move.promoted_piece[1]]
        else:

            end_pos_score = evaluation_index * piece_evaluation[move.moved_piece[1]]

        if move.captured_piece != "__":
            capture_score = evaluation_index * piece_evaluation[move.captured_piece[1]]
            if (
                piece_evaluation[move.moved_piece[1]]
                - piece_evaluation[move.captured_piece[1]]
                < 0.5
            ):
                capture_score += evaluation_index

        move_eval = board_eval - start_pos_score + end_pos_score + capture_score

        move_value_list.append((index, move_eval))

        # if turn_to_move == "w" and move_eval - board_eval > -2:
        #
        #     move_value_list.append((index, move_eval))
        # elif turn_to_move == "b" and move_eval - board_eval < 2:
        #     move_value_list.append((index, move_eval))

    reverse_list = True if turn_to_move == "w" else False

    sorted_move_value_list = sorted(
        move_value_list, key=lambda li: li[1], reverse=reverse_list
    )

    sorted_move_list: list[Move] = []

    for index, _ in sorted_move_value_list:
        sorted_move_list.append(move_list[index])

    return sorted_move_list

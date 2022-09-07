from ..utils.piece_square_tables import piece_evaluation


def get_king_safty_eval(
    board_state: list[list[str]],
    king_side: str,
    king_pos: tuple[int, int] | None,
    game_stage: str,
) -> tuple[float, float]:
    """get relative king_safty based on it's possition.

    Args:
        board_state (list[list[str]]): board_state
        king_side (str): king_side
        king_pos (tuple[int, int] | None): king_pos
        game_stage (str): game_stage

    Returns:
        tuple[float, float]:
    """

    king_mobility: float = 0

    if king_pos is None:
        return 0
    division_index = 100
    k_row, k_col = king_pos
    side_eval = 1 if king_side == "w" else -1
    king_eval: float = 0.0

    for row in [k_row + 1, k_row - 1, k_row]:
        for col in [k_col + 1, k_col - 1, k_col]:
            if row in range(8) and col in range(8) and (row, col) != king_pos:
                piece = board_state[row][col]
                if piece == "__":
                    king_eval += 0.005
                elif piece[0] == king_side:
                    king_eval += piece_evaluation[piece[1]] / division_index
                else:
                    king_eval -= piece_evaluation[piece[1]] / division_index
                    king_mobility -= piece_evaluation[piece[1]] * 0.05

    for row, col in [
        (k_row + 2, k_col - 2),
        (k_row + 2, k_col - 1),
        (k_row + 2, k_col),
        (k_row + 2, k_col + 1),
        (k_row + 2, k_col + 2),
        (k_row + 1, k_col - 2),
        (k_row + 1, k_col + 2),
        (k_row, k_col - 2),
        (k_row, k_col + 2),
        (k_row - 1, k_col - 2),
        (k_row - 1, k_col + 2),
        (k_row - 2, k_col - 2),
        (k_row - 2, k_col - 1),
        (k_row - 2, k_col),
        (k_row - 2, k_col + 1),
        (k_row - 2, k_col + 2),
    ]:
        if row in range(8) and col in range(8):
            piece = board_state[row][col]
            if piece == "__":
                king_eval += 0.001
            elif piece[0] == king_side:
                king_eval += piece_evaluation[piece[1]] / (division_index * 2)
            else:
                king_eval -= piece_evaluation[piece[1]] / (division_index * 2)
                king_mobility -= piece_evaluation[piece[1]] * 0.1

    return (king_eval * side_eval, king_mobility * side_eval)

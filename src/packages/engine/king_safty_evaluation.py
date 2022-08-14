from ..utils.piece_square_tables import piece_evaluation


def get_king_safty_eval(
    board_state: list[list[str]], king_side: str, king_pos: tuple[int, int] | None
) -> float:

    if king_pos is None:
        return 0

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
                    king_eval += piece_evaluation[piece[1]] / 100
                else:
                    king_eval -= piece_evaluation[piece[1]] / 100

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
                king_eval += piece_evaluation[piece[1]] / 200
            else:
                king_eval -= piece_evaluation[piece[1]] / 200

    return king_eval * side_eval

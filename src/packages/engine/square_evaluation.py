from ..utils.piece_square_tables import *


def get_piece_square_evaluation(
    piece: str,
    pos: tuple[int, int],
    game_stage: str,
) -> float:
    """get the value of the piece based on it's possition on the board.

    Args:
        piece (str): piece
        pos (tuple[int, int]): pos
        game_stage (str): game_stage

    Returns:
        float:
    """
    row, col = pos
    if piece == "wP":
        return wP_table[row][col]
    if piece == "wN":
        return wN_table[row][col]
    if piece == "wB":
        return wB_table[row][col]
    if piece == "wR":
        return wR_table[row][col]
    if piece == "wQ":
        return wQ_table[row][col]
    if piece == "wK" and game_stage == "middle game":
        return wK_middle_game_table[row][col]
    if piece == "wK" and game_stage == "end game":
        return wK_end_game_table[row][col]
    if piece == "bP":
        return bP_table[row][col]
    if piece == "bN":
        return bN_table[row][col]
    if piece == "bB":
        return bB_table[row][col]
    if piece == "bR":
        return bR_table[row][col]
    if piece == "bQ":
        return bQ_table[row][col]
    if piece == "bK" and game_stage == "middle game":
        return bK_middle_game_table[row][col]
    if piece == "bK" and game_stage == "end game":
        return bK_end_game_table[row][col]
    return 0

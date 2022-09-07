def possition_under_attack(
    board_state: list[list[str]], possition: tuple[int, int], turn_to_move: str
) -> bool:
    """check to see if the given possition is under attack from opponent's pieces.

    Args:
        board_state (list[list[str]]): board_state
        possition (tuple[int, int]): possition
        turn_to_move (str): turn_to_move

    Returns:
        bool:
    """
    row, col = possition

    opponent_color = "w" if turn_to_move == "b" else "b"

    king_checks = [
        (row - 1, col - 1),
        (row - 1, col),
        (row - 1, col + 1),
        (row, col - 1),
        (row, col + 1),
        (row + 1, col - 1),
        (row + 1, col),
        (row + 1, col + 1),
    ]

    knight_checks = [
        (row - 1, col + 2),
        (row - 1, col - 2),
        (row - 2, col + 1),
        (row - 2, col - 1),
        (row + 1, col + 2),
        (row + 1, col - 2),
        (row + 2, col - 1),
        (row + 2, col + 1),
    ]

    bishop_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    rook_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    if turn_to_move == "w" and row - 1 in range(8):
        if col - 1 in range(8):
            if board_state[row - 1][col - 1] == "bP":
                return True
        if col + 1 in range(8):
            if board_state[row - 1][col + 1] == "bP":
                return True

    if turn_to_move == "b" and row + 1 in range(8):
        if col - 1 in range(8):
            if board_state[row + 1][col - 1] == "wP":
                return True
        if col + 1 in range(8):
            if board_state[row + 1][col + 1] == "wP":
                return True

    for s_row, s_col in king_checks:
        if s_row in range(8) and s_col in range(8):
            if board_state[s_row][s_col] == f"{opponent_color}K":
                return True

    for s_row, s_col in knight_checks:
        if s_row in range(8) and s_col in range(8):
            if board_state[s_row][s_col] == f"{opponent_color}N":
                return True

    for direction in bishop_directions:
        for i in range(1, 8):
            s_row = row + direction[0] * i
            s_col = col + direction[1] * i

            if s_row not in range(8) or s_col not in range(8):
                break

            if board_state[s_row][s_col] in [
                f"{opponent_color}B",
                f"{opponent_color}Q",
            ]:
                return True

            if board_state[s_row][s_col] != "__":
                break

    for direction in rook_directions:
        for i in range(1, 8):
            s_row = row + direction[0] * i
            s_col = col + direction[1] * i

            if s_row not in range(8) or s_col not in range(8):
                break

            if board_state[s_row][s_col] in [
                f"{opponent_color}R",
                f"{opponent_color}Q",
            ]:
                return True

            if board_state[s_row][s_col] != "__":
                break

    return False

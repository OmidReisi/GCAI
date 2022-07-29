def get_board_evaluation(board_state: list[list[str]]) -> int:
    piece_evaluation: dict[str, int] = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
    evaluation: int = 0

    for row in range(8):
        for col in range(8):
            piece = board_state[row][col]
            if piece[0] == "w":
                evaluation += piece_evaluation[piece[1]]
            elif piece[0] == "b":
                evaluation -= piece_evaluation[piece[1]]

    return evaluation

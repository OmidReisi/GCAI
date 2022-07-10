from ..move import Move


def get_possible_moves(
    board_state: list[list[str]], selected_pos: tuple[int, int], turn_to_move: str
) -> list[Move] | None:

    row, col = selected_pos

    selected_side, piece = board_state[row][col]

    if selected_side == turn_to_move:

        if piece == "P":
            return get_pawn_moves(board_state, selected_pos, turn_to_move)
        elif piece == "N":
            pass
        elif piece == "B":
            pass
        elif piece == "R":
            pass
        elif piece == "Q":
            pass
        elif piece == "K":
            pass
    else:
        return []


def get_pawn_moves(
    board_state: list[list[str]], selected_pos: tuple[int, int], turn_to_move: str
):
    moves: list[Move] = []
    p_row, p_col = selected_pos
    if turn_to_move == "w":
        try:
            if board_state[p_row - 1][p_col] == "__":
                moves.append(
                    Move(selected_pos, (p_row - 1, p_col), board_state, turn_to_move)
                )
                if p_row == 6 and board_state[p_row - 2][p_col] == "__":

                    moves.append(
                        Move(
                            selected_pos, (p_row - 2, p_col), board_state, turn_to_move
                        )
                    )

        except IndexError:
            return moves

        if p_row - 1 in range(len(board_state)):
            if p_col - 1 in range(len(board_state[p_row - 1])):

                if board_state[p_row - 1][p_col - 1].startswith("b"):
                    moves.append(
                        Move(
                            selected_pos,
                            (p_row - 1, p_col - 1),
                            board_state,
                            turn_to_move,
                        )
                    )

        if p_row - 1 in range(len(board_state)):
            if p_col + 1 in range(len(board_state[p_row - 1])):
                if board_state[p_row - 1][p_col + 1].startswith("b"):
                    moves.append(
                        Move(
                            selected_pos,
                            (p_row - 1, p_col + 1),
                            board_state,
                            turn_to_move,
                        )
                    )

        return moves

    if turn_to_move == "b":
        try:
            if board_state[p_row + 1][p_col] == "__":
                moves.append(
                    Move(selected_pos, (p_row + 1, p_col), board_state, turn_to_move)
                )
                if p_row == 1 and board_state[p_row + 2][p_col] == "__":

                    moves.append(
                        Move(
                            selected_pos, (p_row + 2, p_col), board_state, turn_to_move
                        )
                    )

        except IndexError:
            return moves

        if p_row + 1 in range(len(board_state)):
            if p_col - 1 in range(len(board_state[p_row + 1])):

                if board_state[p_row + 1][p_col - 1].startswith("w"):
                    moves.append(
                        Move(
                            selected_pos,
                            (p_row + 1, p_col - 1),
                            board_state,
                            turn_to_move,
                        )
                    )

        if p_row + 1 in range(len(board_state)):
            if p_col + 1 in range(len(board_state[p_row + 1])):
                if board_state[p_row + 1][p_col + 1].startswith("b"):
                    moves.append(
                        Move(
                            selected_pos,
                            (p_row + 1, p_col + 1),
                            board_state,
                            turn_to_move,
                        )
                    )

        return moves

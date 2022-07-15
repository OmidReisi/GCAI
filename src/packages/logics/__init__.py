from ..move import Move


def get_possible_moves(
    board_state: list[list[str]], selected_pos: tuple[int, int], turn_to_move: str
) -> list[Move] | None:

    row, col = selected_pos

    selected_side, piece = board_state[row][col]

    if selected_side == turn_to_move:

        if piece == "P":
            return get_pawn_moves(board_state, selected_pos, turn_to_move)
        if piece == "N":
            return get_knight_moves(board_state, selected_pos, turn_to_move)
        if piece == "B":
            return get_bishop_moves(board_state, selected_pos, turn_to_move)
        if piece == "R":
            return get_rook_moves(board_state, selected_pos, turn_to_move)
        if piece == "Q":
            return get_queen_moves(board_state, selected_pos, turn_to_move)
        if piece == "K":
            return get_king_moves(board_state, selected_pos, turn_to_move)
    else:
        return []


def get_pawn_moves(
    board_state: list[list[str]], selected_pos: tuple[int, int], turn_to_move: str
) -> list[Move]:
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

        if p_row - 1 in range(8):
            if p_col - 1 in range(8):

                if board_state[p_row - 1][p_col - 1][0] == "b":
                    moves.append(
                        Move(
                            selected_pos,
                            (p_row - 1, p_col - 1),
                            board_state,
                            turn_to_move,
                        )
                    )

        if p_row - 1 in range(8):
            if p_col + 1 in range(8):
                if board_state[p_row - 1][p_col + 1][0] == "b":
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

        if p_row + 1 in range(8):
            if p_col - 1 in range(8):

                if board_state[p_row + 1][p_col - 1][0] == "w":
                    moves.append(
                        Move(
                            selected_pos,
                            (p_row + 1, p_col - 1),
                            board_state,
                            turn_to_move,
                        )
                    )

        if p_row + 1 in range(8):
            if p_col + 1 in range(8):
                if board_state[p_row + 1][p_col + 1][0] == "w":
                    moves.append(
                        Move(
                            selected_pos,
                            (p_row + 1, p_col + 1),
                            board_state,
                            turn_to_move,
                        )
                    )

        return moves


def get_knight_moves(
    board_state: list[list[str]], selected_pos: tuple[int, int], turn_to_move: str
) -> list[Move]:
    moves: list[Move] = []
    p_row, p_col = selected_pos
    possitions_to_check = [
        (p_row - 1, p_col + 2),
        (p_row - 1, p_col - 2),
        (p_row - 2, p_col + 1),
        (p_row - 2, p_col - 1),
        (p_row + 1, p_col + 2),
        (p_row + 1, p_col - 2),
        (p_row + 2, p_col - 1),
        (p_row + 2, p_col + 1),
    ]

    for row, col in possitions_to_check:
        if row in range(8) and col in range(8):
            if board_state[row][col][0] != turn_to_move:
                moves.append(Move(selected_pos, (row, col), board_state, turn_to_move))

    return moves


def get_bishop_moves(
    board_state: list[list[str]], selected_pos: tuple[int, int], turn_to_move: str
) -> list[Move]:
    moves: list[Move] = []
    directions = {
        "upleft": True,
        "upright": True,
        "downleft": True,
        "downright": True,
    }
    p_row, p_col = selected_pos

    for i in range(1, 8):
        if p_row + i in range(8):
            if p_col + i in range(8):
                possition_to_check = board_state[p_row + i][p_col + i]
                if possition_to_check[0] == turn_to_move:
                    directions["downright"] = False
                elif directions["downright"]:

                    if possition_to_check != "__":
                        directions["downright"] = False
                    moves.append(
                        Move(
                            selected_pos,
                            (p_row + i, p_col + i),
                            board_state,
                            turn_to_move,
                        )
                    )
            if p_col - i in range(8):
                possition_to_check = board_state[p_row + i][p_col - i]
                if possition_to_check[0] == turn_to_move:
                    directions["downleft"] = False
                elif directions["downleft"]:

                    if possition_to_check != "__":
                        directions["downleft"] = False
                    moves.append(
                        Move(
                            selected_pos,
                            (p_row + i, p_col - i),
                            board_state,
                            turn_to_move,
                        )
                    )

        if p_row - i in range(8):
            if p_col + i in range(8):
                possition_to_check = board_state[p_row - i][p_col + i]
                if possition_to_check[0] == turn_to_move:
                    directions["upright"] = False
                elif directions["upright"]:

                    if possition_to_check != "__":
                        directions["upright"] = False
                    moves.append(
                        Move(
                            selected_pos,
                            (p_row - i, p_col + i),
                            board_state,
                            turn_to_move,
                        )
                    )
            if p_col - i in range(8):
                possition_to_check = board_state[p_row - i][p_col - i]
                if possition_to_check[0] == turn_to_move:
                    directions["upleft"] = False
                elif directions["upleft"]:

                    if possition_to_check != "__":
                        directions["upleft"] = False
                    moves.append(
                        Move(
                            selected_pos,
                            (p_row - i, p_col - i),
                            board_state,
                            turn_to_move,
                        )
                    )
    return moves


def get_rook_moves(
    board_state: list[list[str]], selected_pos: tuple[int, int], turn_to_move: str
) -> list[Move]:
    moves: list[Move] = []

    directions = {
        "up": True,
        "down": True,
        "left": True,
        "right": True,
    }

    p_row, p_col = selected_pos

    for i in range(1, 8):
        if p_row + i in range(8):
            possition_to_check = board_state[p_row + i][p_col]
            if possition_to_check[0] == turn_to_move:
                directions["down"] = False
            elif directions["down"]:

                if possition_to_check != "__":
                    directions["down"] = False
                moves.append(
                    Move(
                        selected_pos,
                        (p_row + i, p_col),
                        board_state,
                        turn_to_move,
                    )
                )
        if p_row - i in range(8):
            possition_to_check = board_state[p_row - i][p_col]
            if possition_to_check[0] == turn_to_move:
                directions["up"] = False
            elif directions["up"]:

                if possition_to_check != "__":
                    directions["up"] = False
                moves.append(
                    Move(
                        selected_pos,
                        (p_row - i, p_col),
                        board_state,
                        turn_to_move,
                    )
                )
        if p_col + i in range(8):
            possition_to_check = board_state[p_row][p_col + i]
            if possition_to_check[0] == turn_to_move:
                directions["right"] = False
            elif directions["right"]:

                if possition_to_check != "__":
                    directions["right"] = False
                moves.append(
                    Move(
                        selected_pos,
                        (p_row, p_col + i),
                        board_state,
                        turn_to_move,
                    )
                )
        if p_col - i in range(8):
            possition_to_check = board_state[p_row][p_col - i]
            if possition_to_check[0] == turn_to_move:
                directions["left"] = False
            elif directions["left"]:

                if possition_to_check != "__":
                    directions["left"] = False
                moves.append(
                    Move(
                        selected_pos,
                        (p_row, p_col - i),
                        board_state,
                        turn_to_move,
                    )
                )
    return moves


def get_queen_moves(
    board_state: list[list[str]], selected_pos: tuple[int, int], turn_to_move: str
) -> list[Move]:
    moves: list[Move] = []
    directions = {
        "up": True,
        "down": True,
        "left": True,
        "right": True,
        "upleft": True,
        "upright": True,
        "downleft": True,
        "downright": True,
    }
    p_row, p_col = selected_pos

    for i in range(1, 8):
        if p_row + i in range(8):

            possition_to_check = board_state[p_row + i][p_col]
            if possition_to_check[0] == turn_to_move:
                directions["down"] = False
            elif directions["down"]:

                if possition_to_check != "__":
                    directions["down"] = False
                moves.append(
                    Move(
                        selected_pos,
                        (p_row + i, p_col),
                        board_state,
                        turn_to_move,
                    )
                )

            if p_col + i in range(8):
                possition_to_check = board_state[p_row + i][p_col + i]
                if possition_to_check[0] == turn_to_move:
                    directions["downright"] = False
                elif directions["downright"]:

                    if possition_to_check != "__":
                        directions["downright"] = False
                    moves.append(
                        Move(
                            selected_pos,
                            (p_row + i, p_col + i),
                            board_state,
                            turn_to_move,
                        )
                    )
            if p_col - i in range(8):
                possition_to_check = board_state[p_row + i][p_col - i]
                if possition_to_check[0] == turn_to_move:
                    directions["downleft"] = False
                elif directions["downleft"]:

                    if possition_to_check != "__":
                        directions["downleft"] = False
                    moves.append(
                        Move(
                            selected_pos,
                            (p_row + i, p_col - i),
                            board_state,
                            turn_to_move,
                        )
                    )

        if p_row - i in range(8):

            possition_to_check = board_state[p_row - i][p_col]
            if possition_to_check[0] == turn_to_move:
                directions["up"] = False
            elif directions["up"]:

                if possition_to_check != "__":
                    directions["up"] = False
                moves.append(
                    Move(
                        selected_pos,
                        (p_row - i, p_col),
                        board_state,
                        turn_to_move,
                    )
                )

            if p_col + i in range(8):
                possition_to_check = board_state[p_row - i][p_col + i]
                if possition_to_check[0] == turn_to_move:
                    directions["upright"] = False
                elif directions["upright"]:

                    if possition_to_check != "__":
                        directions["upright"] = False
                    moves.append(
                        Move(
                            selected_pos,
                            (p_row - i, p_col + i),
                            board_state,
                            turn_to_move,
                        )
                    )
            if p_col - i in range(8):
                possition_to_check = board_state[p_row - i][p_col - i]
                if possition_to_check[0] == turn_to_move:
                    directions["upleft"] = False
                elif directions["upleft"]:

                    if possition_to_check != "__":
                        directions["upleft"] = False
                    moves.append(
                        Move(
                            selected_pos,
                            (p_row - i, p_col - i),
                            board_state,
                            turn_to_move,
                        )
                    )

        if p_col + i in range(8):
            possition_to_check = board_state[p_row][p_col + i]
            if possition_to_check[0] == turn_to_move:
                directions["right"] = False
            elif directions["right"]:

                if possition_to_check != "__":
                    directions["right"] = False
                moves.append(
                    Move(
                        selected_pos,
                        (p_row, p_col + i),
                        board_state,
                        turn_to_move,
                    )
                )
        if p_col - i in range(8):
            possition_to_check = board_state[p_row][p_col - i]
            if possition_to_check[0] == turn_to_move:
                directions["left"] = False
            elif directions["left"]:

                if possition_to_check != "__":
                    directions["left"] = False
                moves.append(
                    Move(
                        selected_pos,
                        (p_row, p_col - i),
                        board_state,
                        turn_to_move,
                    )
                )
    return moves


def get_king_moves(
    board_state: list[list[str]], selected_pos: tuple[int, int], turn_to_move: str
) -> list[Move]:
    moves: list[Move] = []
    p_row, p_col = selected_pos
    possitions_to_check = [
        (p_row - 1, p_col),
        (p_row - 1, p_col - 1),
        (p_row - 1, p_col + 1),
        (p_row, p_col - 1),
        (p_row, p_col + 1),
        (p_row + 1, p_col),
        (p_row + 1, p_col - 1),
        (p_row + 1, p_col + 1),
    ]

    for row, col in possitions_to_check:
        if row in range(8) and col in range(8):
            if board_state[row][col][0] != turn_to_move:
                moves.append(Move(selected_pos, (row, col), board_state, turn_to_move))

    return moves

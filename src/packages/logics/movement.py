from ..move import Move
from .check import possition_under_attack


def get_possible_moves(
    board_state: list[list[str]],
    selected_pos: tuple[int, int],
    turn_to_move: str,
    last_move: Move,
    castle_rights: dict[str, bool],
) -> list[Move]:

    row, col = selected_pos

    selected_side, piece = board_state[row][col]

    if selected_side == turn_to_move:

        if piece == "P":
            move_list = get_pawn_moves(board_state, selected_pos, turn_to_move)

            move = get_en_passant(board_state, selected_pos, turn_to_move, last_move)

            if move is not None:
                move_list.append(move)

            return move_list
        if piece == "N":
            return get_knight_moves(board_state, selected_pos, turn_to_move)
        if piece == "B":
            return get_bishop_moves(board_state, selected_pos, turn_to_move)
        if piece == "R":
            return get_rook_moves(board_state, selected_pos, turn_to_move)
        if piece == "Q":
            return get_queen_moves(board_state, selected_pos, turn_to_move)
        if piece == "K":
            return get_king_moves(board_state, selected_pos, turn_to_move) + get_castle(
                board_state, selected_pos, turn_to_move, castle_rights
            )

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


def get_en_passant(
    board_state: list[list[str]],
    selected_pos: tuple[int, int],
    turn_to_move: str,
    last_move: Move | None,
) -> Move | None:
    if last_move is None:
        return None

    p_row, p_col = selected_pos

    if turn_to_move == "w" and p_row == 3:
        if p_col - 1 in range(8) and board_state[p_row][p_col - 1] == "bP":
            if last_move.is_two_square_pawn_move():
                return Move(
                    selected_pos, (p_row - 1, p_col - 1), board_state, turn_to_move
                )
        if p_col + 1 in range(8) and board_state[p_row][p_col + 1] == "bP":
            if last_move.is_two_square_pawn_move():
                return Move(
                    selected_pos, (p_row - 1, p_col + 1), board_state, turn_to_move
                )

    if turn_to_move == "b" and p_row == 4:
        if p_col - 1 in range(8) and board_state[p_row][p_col - 1] == "wP":
            if last_move.is_two_square_pawn_move():
                return Move(
                    selected_pos, (p_row + 1, p_col - 1), board_state, turn_to_move
                )
        if p_col + 1 in range(8) and board_state[p_row][p_col + 1] == "wP":
            if last_move.is_two_square_pawn_move():
                return Move(
                    selected_pos, (p_row + 1, p_col + 1), board_state, turn_to_move
                )

    return None


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


def get_castle(
    board_state: list[list[str]],
    selected_pos: tuple[int, int],
    turn_to_move: str,
    castle_rights: dict[str, bool],
) -> list[Move]:

    moves: list[Move] = []

    p_row, p_col = selected_pos

    if castle_rights["short"]:

        if all(
            [
                board_state[p_row][p_col + 1] == "__",
                board_state[p_row][p_col + 2] == "__",
            ]
        ):
            if not any(
                [
                    possition_under_attack(board_state, (p_row, p_col), turn_to_move),
                    possition_under_attack(
                        board_state, (p_row, p_col + 1), turn_to_move
                    ),
                    possition_under_attack(
                        board_state, (p_row, p_col + 2), turn_to_move
                    ),
                ]
            ):

                moves.append(
                    Move(selected_pos, (p_row, p_col + 2), board_state, turn_to_move)
                )
                moves.append(
                    Move(selected_pos, (p_row, p_col + 3), board_state, turn_to_move)
                )

    if castle_rights["long"]:

        if all(
            [
                board_state[p_row][p_col - 1] == "__",
                board_state[p_row][p_col - 2] == "__",
                board_state[p_row][p_col - 3] == "__",
            ]
        ):
            if not any(
                [
                    possition_under_attack(board_state, (p_row, p_col), turn_to_move),
                    possition_under_attack(
                        board_state, (p_row, p_col - 1), turn_to_move
                    ),
                    possition_under_attack(
                        board_state, (p_row, p_col - 2), turn_to_move
                    ),
                ]
            ):

                moves.append(
                    Move(selected_pos, (p_row, p_col - 2), board_state, turn_to_move)
                )
                moves.append(
                    Move(selected_pos, (p_row, p_col - 4), board_state, turn_to_move)
                )

    return moves


def any_valid_moves(
    board_state: list[list[str]],
    turn_to_move: str,
    initial_king_pos: tuple[int, int],
    last_move: Move | None,
    castle_rights: dict[str, bool],
) -> bool:
    for row in range(8):
        for col in range(8):
            if board_state[row][col][0] == turn_to_move:
                move_list = get_possible_moves(
                    board_state, (row, col), turn_to_move, last_move, castle_rights
                )
                for move in move_list:
                    temp_board_state = [listitem.copy() for listitem in board_state]
                    s_row, s_col = move.start_pos
                    e_row, e_col = move.end_pos
                    temp_board_state[e_row][e_col] = move.moved_piece
                    temp_board_state[s_row][s_col] = "__"
                    king_pos = (
                        move.end_pos if move.moved_piece[1] == "K" else initial_king_pos
                    )
                    if not possition_under_attack(
                        temp_board_state, king_pos, turn_to_move
                    ):
                        return True
    return False

from ..move import Move


def get_switched_turn(turn: str) -> str:
    if turn == "b":
        return "w"
    return "b"


def get_castle_rights(move: Move, castle_rights: dict[str, bool]) -> dict[str, bool]:
    temp_castle_rights: dict[str, bool] = castle_rights.copy()
    if move.moved_piece[1] == "K":
        temp_castle_rights["short"] = False
        temp_castle_rights["long"] = False

    if move.moved_piece[1] == "R" and move.start_pos[1] == 0:
        temp_castle_rights["long"] = False
    if move.moved_piece[1] == "R" and move.start_pos[1] == 7:
        temp_castle_rights["short"] = False

    return temp_castle_rights


def get_king_pos(move: Move, king_pos: tuple[int, int]) -> tuple[int, int]:
    if move.moved_piece[1] == "K":
        return move.end_pos
    return king_pos


def make_move(
    board_state: list[list[str]], turn_to_move: str, move: Move
) -> list[list[str]]:

    temp_board_state: list[list[str]] = [list_item.copy() for list_item in board_state]

    p_row, p_col = move.start_pos

    temp_board_state[p_row][p_col] = "__"
    s_row, s_col = move.end_pos
    temp_board_state[s_row][s_col] = (
        f"{turn_to_move}Q" if move.is_pawn_promotion else move.moved_piece
    )
    if move.is_pawn_promotion:
        move.promoted_piece = temp_board_state[s_row][s_col]

    if move.is_en_passant:

        temp_board_state[move.en_passant_pos[0]][move.en_passant_pos[1]] = "__"

    if move.is_castle:
        if move.get_castle_type() == "short":
            temp_board_state[s_row][s_col - 1] = temp_board_state[s_row][s_col + 1]
            temp_board_state[s_row][s_col + 1] = "__"
        elif move.get_castle_type() == "long":
            temp_board_state[s_row][s_col + 1] = temp_board_state[s_row][s_col - 2]
            temp_board_state[s_row][s_col - 2] = "__"

    return temp_board_state


def undo_move(
    board_state: list[list[str]], turn_to_move: str, move: Move
) -> list[list[str]]:

    temp_board_state: list[list[str]] = [list_item.copy() for list_item in board_state]

    s_row, s_col = move.start_pos
    e_row, e_col = move.end_pos
    temp_board_state[s_row][s_col] = move.moved_piece
    temp_board_state[e_row][e_col] = move.captured_piece

    if move.is_en_passant:
        temp_board_state[move.en_passant_pos[0]][
            move.en_passant_pos[1]
        ] = f"{turn_to_move}P"

    turn_to_move = get_switched_turn(turn_to_move)

    if move.is_castle:
        if move.get_castle_type() == "short":
            temp_board_state[e_row][7] = f"{turn_to_move}R"
            temp_board_state[e_row][e_col - 1] = "__"

        elif move.get_castle_type() == "long":
            temp_board_state[e_row][0] = f"{turn_to_move}R"
            temp_board_state[e_row][e_col + 1] = "__"

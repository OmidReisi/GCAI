from .movement import get_possible_moves
from .check import possition_under_attack
from ..move import Move


def is_valid(
    board_state: list[list[str]],
    move: Move,
    turn_to_move: str,
    king_pos: tuple[int, int],
) -> bool:
    """check if the move is valid.

    Args:
        board_state (list[list[str]]): board_state
        move (Move): move
        turn_to_move (str): turn_to_move
        king_pos (tuple[int, int]): king_pos

    Returns:
        bool:
    """

    temp_board_state: list[list[str]] = [list_item.copy() for list_item in board_state]
    if move.is_castle:
        move.update_end_pos()

    p_row, p_col = move.start_pos

    temp_board_state[p_row][p_col] = "__"
    s_row, s_col = move.end_pos
    temp_board_state[s_row][s_col] = move.moved_piece

    if move.is_en_passant:

        temp_board_state[move.en_passant_pos[0]][move.en_passant_pos[1]] = "__"

    king_pos = move.end_pos if move.moved_piece[1] == "K" else king_pos

    if move.is_castle:
        if move.get_castle_type() == "short":
            temp_board_state[s_row][s_col - 1] = temp_board_state[s_row][s_col + 1]
            temp_board_state[s_row][s_col + 1] = "__"
        elif move.get_castle_type() == "long":
            temp_board_state[s_row][s_col + 1] = temp_board_state[s_row][s_col - 2]
            temp_board_state[s_row][s_col - 2] = "__"

    if possition_under_attack(temp_board_state, king_pos, turn_to_move):
        return False
    return True


def any_valid_moves(
    board_state: list[list[str]],
    turn_to_move: str,
    king_pos: tuple[int, int],
    last_move: Move | None,
    castle_rights: dict[str, bool],
) -> bool:
    """check if there are any valid moves.

    Args:
        board_state (list[list[str]]): board_state
        turn_to_move (str): turn_to_move
        king_pos (tuple[int, int]): king_pos
        last_move (Move | None): last_move
        castle_rights (dict[str, bool]): castle_rights

    Returns:
        bool:
    """
    for row in range(8):
        for col in range(8):
            if board_state[row][col][0] == turn_to_move:
                move_list = get_possible_moves(
                    board_state, (row, col), turn_to_move, last_move, castle_rights
                )
                for move in move_list:
                    if is_valid(board_state, move, turn_to_move, king_pos):
                        return True
    return False


def get_valid_moves(
    board_state: list[list[str]],
    turn_to_move: str,
    king_pos: tuple[int, int],
    castle_rights: dict[str, bool],
    last_move: Move | None,
) -> list[Move]:
    """get valid moves from possible moves.

    Args:
        board_state (list[list[str]]): board_state
        turn_to_move (str): turn_to_move
        king_pos (tuple[int, int]): king_pos
        castle_rights (dict[str, bool]): castle_rights
        last_move (Move | None): last_move

    Returns:
        list[Move]:
    """

    possible_moves: list[Move] = []
    valid_moves: list[Move] = []
    for row in range(8):
        for col in range(8):
            possible_moves += get_possible_moves(
                board_state, (row, col), turn_to_move, last_move, castle_rights
            )
    for move in possible_moves:
        if is_valid(board_state, move, turn_to_move, king_pos):
            valid_moves.append(move)
    return valid_moves


# def get_piece_valid_moves(
#     board_state: list[list[str]],
#     turn_to_move: str,
#     selected_pos: tuple[int, int],
#     king_pos: tuple[int, int],
#     castle_rights: dict[str, bool],
#     last_move: Move | None,
# ) -> list[Move]:
#     """get the valid moves for the piece in the given possition.
#
#     Args:
#         board_state (list[list[str]]): board_state
#         turn_to_move (str): turn_to_move
#         selected_pos (tuple[int, int]): selected_pos
#         king_pos (tuple[int, int]): king_pos
#         castle_rights (dict[str, bool]): castle_rights
#         last_move (Move | None): last_move
#
#     Returns:
#         list[Move]:
#     """
#     row, col = selected_pos
#     piece = board_state[row][col]
#
#     if piece[0] != turn_to_move:
#         return []
#
#     valid_moves: list[Move] = []
#
#     possible_moves = get_possible_moves(
#         board_state, selected_pos, turn_to_move, last_move, castle_rights
#     )
#
#     for move in possible_moves:
#         if is_valid(board_state, move, turn_to_move, king_pos):
#             valid_moves.append(move)
#
#     return valid_moves
#
#
# def num_of_piece_valid_moves(
#     board_state: list[list[str]],
#     selected_pos: tuple[int, int],
#     turn_to_move: str,
#     king_pos: tuple[int, int],
#     castle_rights: dict[str, bool],
#     last_move: Move | None,
# ) -> int:
#     row, col = selected_pos
#     piece = board_state[row][col]
#
#     if piece[0] != turn_to_move:
#         return 0
#
#     possible_moves = get_possible_moves(
#         board_state, selected_pos, turn_to_move, last_move, castle_rights
#     )
#
#     num_of_moves = 0
#
#     for move in possible_moves:
#         if is_valid(board_state, move, turn_to_move, king_pos):
#             num_of_moves += 1
#
#     return num_of_moves

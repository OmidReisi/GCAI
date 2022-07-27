from .movement import get_possible_moves
from .check import possition_under_attack
from ..move import Move


def is_valid(
    board_state: list[list[str]],
    move: Move,
    turn_to_move: str,
    king_pos: tuple[int, int],
) -> bool:

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

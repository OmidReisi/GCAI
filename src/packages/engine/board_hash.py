from ..move import Move


def get_board_hash(
    board_state: list[list[str]],
    board_hash: float,
    move: Move | None,
    zobrist_hash_keys: dict[str, int],
) -> int:
    if move is None:
        return
    s_row, s_col = move.start_pos
    board_hash = board_hash ^ zobrist_hash_keys[f"{move.moved_piece}_({s_row},{s_col})"]

    e_row, e_col = move.end_pos
    if move.captured_piece != "__":
        board_hash = (
            board_hash ^ zobrist_hash_keys[f"{move.captured_piece}_({e_row},{e_col})"]
        )
    elif move.is_en_passant:
        p_row, p_col = move.en_passant_pos
        piece = "wP" if move.moved_piece[0] == "b" else "bP"
        board_hash = board_hash ^ zobrist_hash_keys[f"{piece}_({p_row},{p_col})"]
        board_hash = board_hash ^ zobrist_hash_keys[f"en_passant_file_{p_col}"]
    elif move.is_castle:
        castle_type = move.get_castle_type()
        side = move.moved_piece[0]

        if castle_type == "short" and side == "w":
            s_row, s_col = (7, 7)
            e_row, e_col = (7, 5)
            board_hash = board_hash ^ zobrist_hash_keys["wK_castle_rights"]

        elif castle_type == "long" and side == "w":
            s_row, s_col = (7, 0)
            e_row, e_col = (7, 3)
            board_hash = board_hash ^ zobrist_hash_keys["wQ_castle_rights"]

        elif castle_type == "short" and side == "b":
            s_row, s_col = (0, 0)
            e_row, e_col = (0, 5)
            board_hash = board_hash ^ zobrist_hash_keys["bK_castle_rights"]

        elif castle_type == "long" and side == "b":
            s_row, s_col = (0, 0)
            e_row, e_col = (0, 3)
            board_hash = board_hash ^ zobrist_hash_keys["bQ_castle_rights"]
        else:
            raise ValueError

        board_hash = board_hash ^ zobrist_hash_keys[f"{side}R_({s_row},{s_col})"]
        board_hash = board_hash ^ zobrist_hash_keys[f"{side}R_({e_row},{e_col})"]
    e_row, e_col = move.end_pos
    board_hash = board_hash ^ zobrist_hash_keys[f"{move.moved_piece}_({e_row},{e_col})"]
    if move.is_two_square_pawn_move():
        opponent_side = "w" if move.moved_piece[0] == "b" else "b"
        if e_col - 1 in range(8):
            if board_state[e_row][e_col - 1] == f"{opponent_side}P":

                board_hash = (
                    board_hash ^ zobrist_hash_keys[f"en_passant_file_{e_col - 1}"]
                )
        if e_col + 1 in range(8):
            if board_state[e_row][e_col + 1] == f"{opponent_side}P":

                board_hash = (
                    board_hash ^ zobrist_hash_keys[f"en_passant_file_{e_col + 1}"]
                )

    board_hash = board_hash ^ zobrist_hash_keys["black_to_move"]
    return board_hash

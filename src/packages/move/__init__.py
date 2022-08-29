from __future__ import annotations


row_to_rank: dict[int, int] = {
    0: 8,
    1: 7,
    2: 6,
    3: 5,
    4: 4,
    5: 3,
    6: 2,
    7: 1,
}
col_to_file: dict[int, str] = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h",
}


rank_to_row: dict[int, int] = {
    8: 0,
    7: 1,
    6: 2,
    5: 3,
    4: 4,
    3: 5,
    2: 6,
    1: 7,
}
file_to_col: dict[str, int] = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
}


symbols_notation: dict[str, str] = {
    "wK": "♔",
    "wQ": "♕",
    "wR": "♖",
    "wB": "♗",
    "wN": "♘",
    "wP": "♙",
    "bK": "♚",
    "bQ": "♛",
    "bR": "♜",
    "bB": "♝",
    "bN": "♞",
    "bP": "♟",
}


class Move:
    def __init__(
        self,
        start_pos: tuple[int, int] | None,
        end_pos: tuple[int, int] | None,
        board_state: list[list[str]],
        turn_to_move: str,
    ) -> None:
        self.start_pos: tuple[int, int] | None = start_pos
        self.end_pos: tuple[int, int] | None = end_pos
        self.turn_to_move: str = turn_to_move

        self.is_pawn_promotion: bool = False

        self.promoted_piece: str | None = None

        self.castle_rights: dict[str, dict[str, bool]] = {
            "w": {"short": True, "long": True},
            "b": {"short": True, "long": True},
        }

        if self.start_pos is not None:
            self.moved_piece: str = board_state[self.start_pos[0]][self.start_pos[1]]
        else:
            self.moved_piece = None

        if self.end_pos is not None:
            self.captured_piece: str = board_state[self.end_pos[0]][self.end_pos[1]]
        else:
            self.captured_piece = None

        if self.moved_piece == "wP" and self.end_pos[0] == 0:
            self.is_pawn_promotion = True
            self.promoted_piece = "wQ"

        if self.moved_piece == "bP" and self.end_pos[0] == 7:
            self.is_pawn_promotion = True
            self.promoted_piece = "bQ"

        self.opening_name: str | None = None

        self.row_col_notation: str = ""
        self.notation: str = self.get_notation()

        self.fifty_move_rule: int | None = None

    def set_promoted_piece(self, piece: str) -> None:
        if self.is_pawn_promotion:
            self.promoted_piece = piece

    def is_two_square_pawn_move(self) -> bool:
        if self.start_pos is not None and self.end_pos is not None:
            if (
                abs(self.start_pos[0] - self.end_pos[0]) == 2
                and self.start_pos[1] == self.end_pos[1]
            ):
                return True
        return False

    @property
    def is_en_passant(self) -> bool:
        if self.start_pos is None or self.end_pos is None:
            return False
        if (
            self.moved_piece[1] == "P"
            and abs(self.start_pos[0] - self.end_pos[0]) == 1
            and abs(self.start_pos[1] - self.end_pos[1]) == 1
            and self.captured_piece == "__"
        ):
            return True

        return False

    @property
    def en_passant_pos(self) -> tuple[int, int] | None:
        if self.is_en_passant:
            return (self.start_pos[0], self.end_pos[1])
        return None

    @property
    def is_castle(self) -> bool:
        if self.start_pos is None or self.end_pos is None:
            return False
        if self.moved_piece[1] == "K" and self.start_pos[0] == self.end_pos[0]:
            if self.end_pos[1] - self.start_pos[1] in [2, -2, 3, -4]:
                return True
        return False

    def get_castle_type(self) -> str | None:

        if self.is_castle:
            if self.start_pos[1] < self.end_pos[1]:
                return "short"
            return "long"
        return None

    def update_end_pos(self) -> None:
        if self.is_castle:
            p_row, p_col = self.start_pos
            if self.get_castle_type() == "short":
                self.end_pos = (p_row, p_col + 2)
            else:
                self.end_pos = (p_row, p_col - 2)
            self.captured_piece = "__"

    def get_notation(self) -> str | None:
        if self.start_pos is None or self.end_pos is None:
            return None
        if self.is_castle:
            if self.get_castle_type() == "short":
                return "0-0"
            if self.get_castle_type() == "long":
                return "0-0-0"
        piece = "" if self.moved_piece[1] == "P" else self.moved_piece[1]
        capture = "" if self.captured_piece == "__" else "x"
        if self.is_en_passant:
            capture = "x"

        if capture == "x" and piece == "":
            piece = col_to_file[self.start_pos[1]]
        promotion = (
            f"={self.promoted_piece[1]}"
            if self.is_pawn_promotion and self.promoted_piece is not None
            else ""
        )

        return (
            piece
            + self.row_col_notation
            + capture
            + col_to_file[self.end_pos[1]]
            + str(row_to_rank[self.end_pos[0]])
            + promotion
        )

    def update_notation(self, notation_part: str) -> None:
        self.notation = self.get_notation() + notation_part

    def get_symbols_notation(self):
        if self.notation[0] in ["K", "Q", "R", "B", "N"]:
            return (
                symbols_notation[self.turn_to_move + self.notation[0]]
                + self.notation[1:]
            )
        return self.notation

    def set_fifty_move_rule(self, previous_fifty_move_rule: int) -> None:
        if self.start_pos is None or self.end_pos is None:
            return
        if self.moved_piece[1] == "P" or self.captured_piece != "__":
            self.fifty_move_rule = 0

        else:
            self.fifty_move_rule = previous_fifty_move_rule + 1

    def __eq__(self, other: Move) -> bool:
        if (
            (self.start_pos == other.start_pos)
            and (self.end_pos == other.end_pos)
            and (self.captured_piece == other.captured_piece)
            and (self.moved_piece == other.moved_piece)
            and (self.turn_to_move == other.turn_to_move)
        ):
            return True

        return False

    def __ne__(self, other: Move) -> bool:
        return not self == other

    @staticmethod
    def set_row_col_move_notation(
        move: Move,
        board_state: list[list[str]],
        turn_to_move: str,
        castle_rights: dict[str, bool],
        king_pos: tuple[int, int],
        last_move: Move | None,
    ) -> str:

        from ..logics import get_possible_moves, is_valid

        row_col_notation: str = ""
        move_list: list[Move] = []
        row_flag: bool = False
        col_flag: bool = False

        if move.moved_piece[1] in ["P", "K"]:
            return row_col_notation

        for row in range(8):
            for col in range(8):

                if (
                    board_state[row][col] == move.moved_piece
                    and (row, col) != move.start_pos
                ):

                    moves_to_check = get_possible_moves(
                        board_state,
                        (row, col),
                        turn_to_move,
                        last_move,
                        castle_rights,
                    )
                    for check_move in moves_to_check:
                        if move.end_pos == check_move.end_pos and is_valid(
                            board_state,
                            check_move,
                            turn_to_move,
                            king_pos,
                        ):
                            move_list.append(check_move)

        for check_move in move_list:
            if col_flag is False and move.start_pos[0] == check_move.start_pos[0]:
                col_flag = True
            if row_flag is False and move.start_pos[1] == check_move.start_pos[1]:
                row_flag = True

            if row_flag and col_flag:
                break

        if col_flag:
            row_col_notation = col_to_file[move.start_pos[1]]

        if row_flag:
            row_col_notation += str(row_to_rank[move.start_pos[0]])

        return row_col_notation

    @staticmethod
    def from_notation(
        notation: str,
        board_state: list[list[str]],
        turn_to_move: str,
        last_move: Move | None,
        castle_rights: dict[str, bool],
        king_pos: tuple[int, int],
    ) -> Move | None:

        from ..logics import get_possible_moves

        piece = (
            f"{turn_to_move}{notation[0]}"
            if notation[0] in ["K", "Q", "R", "B", "N"]
            else f"{turn_to_move}P"
        )

        move_notation = notation if notation[-1] != "+" else notation[:-1]

        for row in range(8):
            for col in range(8):
                move_list = get_possible_moves(
                    board_state,
                    (row, col),
                    turn_to_move,
                    last_move,
                    castle_rights,
                    piece,
                )

                for move in move_list:
                    move.row_col_notation = Move.set_row_col_move_notation(
                        move,
                        board_state,
                        turn_to_move,
                        castle_rights,
                        king_pos,
                        last_move,
                    )

                    if move.notation == move_notation:
                        return move
        return None

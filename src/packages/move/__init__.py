from __future__ import annotations


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

        if self.moved_piece == "bP" and self.end_pos[0] == 7:
            self.is_pawn_promotion = True

        self.row_to_rank: dict[int, int] = {
            0: 8,
            1: 7,
            2: 6,
            3: 5,
            4: 4,
            5: 3,
            6: 2,
            7: 1,
        }
        self.col_to_file: dict[int, str] = {
            0: "a",
            1: "b",
            2: "c",
            3: "d",
            4: "e",
            5: "f",
            6: "g",
            7: "h",
        }

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
            piece = self.col_to_file[self.start_pos[1]]
        promotion = (
            f"={self.promoted_piece[1]}"
            if self.is_pawn_promotion and self.promoted_piece is not None
            else ""
        )

        return (
            piece
            + self.row_col_notation
            + capture
            + self.col_to_file[self.end_pos[1]]
            + str(self.row_to_rank[self.end_pos[0]])
            + promotion
        )

    def update_notation(self, notation_part: str) -> None:
        self.notation = self.get_notation() + notation_part

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

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
        self.is_en_passant: bool = False
        self.is_castling: bool = False

        self.promoted_piece: str | None = None
        self.en_passant_pos: tuple[int, int] | None = None

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

    def set_en_passant(self):
        self.is_en_passant = True

    def set_en_passant_pos(self, pos: tuple[int, int]):
        if self.is_en_passant:
            self.en_passant_pos = pos

    def __eq__(self, other: Move) -> bool:
        if (
            (self.start_pos == other.start_pos)
            and (self.end_pos == other.end_pos)
            and (self.captured_piece == other.captured_piece)
            and (self.moved_piece == other.moved_piece)
            and (self.turn_to_move == other.turn_to_move)
            and (self.is_pawn_promotion == other.is_pawn_promotion)
            and (self.is_castling == other.is_castling)
        ):
            return True

        return False

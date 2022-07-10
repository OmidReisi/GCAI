from __future__ import annotations


class Move:
    def __init__(
        self,
        start_pos: tuple[int, int] | None,
        end_pos: tuple[int, int] | None,
        board_state: list[list[str]],
        turn_to_move: str,
    ) -> None:
        self.start_pos: tuple[int, int] = start_pos
        self.end_pos: tuple[int, int] = end_pos
        self.turn_to_move = turn_to_move

        if self.start_pos is not None:
            self.moved_piece: str = board_state[self.start_pos[0]][self.start_pos[1]]
        else:
            self.moved_piece = None

        if self.end_pos is not None:
            self.captured_piece: str = board_state[self.end_pos[0]][self.end_pos[1]]
        else:
            self.captured_piece = None

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

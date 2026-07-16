from typing import List, Optional, Tuple

ROWS = 6
COLS = 7
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2


class Board:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.last_move: Optional[Tuple[int, int]] = None

    def copy(self) -> "Board":
        b = Board()
        b.grid = [row[:] for row in self.grid]
        b.last_move = self.last_move
        return b

    def legal_moves(self) -> List[int]:
        return [c for c in range(COLS) if self.grid[0][c] == EMPTY]

    def apply_move(self, col: int, player: int) -> int:
        if col not in range(COLS) or self.grid[0][col] != EMPTY:
            raise ValueError("Illegal move")
        for r in range(ROWS - 1, -1, -1):
            if self.grid[r][col] == EMPTY:
                self.grid[r][col] = player
                self.last_move = (r, col)
                return r
        raise ValueError("Column full")

    def is_full(self) -> bool:
        return all(self.grid[0][c] != EMPTY for c in range(COLS))

    def winner(self) -> Optional[int]:
        for r in range(ROWS):
            for c in range(COLS):
                p = self.grid[r][c]
                if p == EMPTY:
                    continue
                if c <= COLS - 4 and all(self.grid[r][c + i] == p for i in range(4)):
                    return p
                if r <= ROWS - 4 and all(self.grid[r + i][c] == p for i in range(4)):
                    return p
                if r <= ROWS - 4 and c <= COLS - 4 and all(self.grid[r + i][c + i] == p for i in range(4)):
                    return p
                if r >= 3 and c <= COLS - 4 and all(self.grid[r - i][c + i] == p for i in range(4)):
                    return p
        return None

    def is_terminal(self) -> bool:
        return self.winner() is not None or self.is_full()

    def __str__(self) -> str:
        rows = []
        for r in range(ROWS):
            rows.append(" ".join(str(x) for x in self.grid[r]))
        return "\n".join(rows)


def legal_moves(board: Board) -> List[int]:
    return board.legal_moves()


def apply_move(board: Board, col: int, player: int) -> int:
    return board.apply_move(col, player)


def winner(board: Board) -> Optional[int]:
    return board.winner()


def is_draw(board: Board) -> bool:
    return board.is_full() and board.winner() is None


def is_terminal(board: Board) -> bool:
    return board.is_terminal()

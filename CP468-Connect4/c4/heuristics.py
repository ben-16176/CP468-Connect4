from typing import List

from c4.board import COLS, PLAYER1, PLAYER2, ROWS, Board


def window_score(window: List[int], player: int) -> int:
    opp = PLAYER1 if player == PLAYER2 else PLAYER2
    count_p = window.count(player)
    count_o = window.count(opp)
    if count_p > 0 and count_o > 0:
        return 0
    if count_p == 4:
        return 10000
    if count_p == 3:
        return 50
    if count_p == 2:
        return 10
    if count_o == 3:
        return -80
    if count_o == 2:
        return -5
    return 0


def evaluate(board: Board, player: int) -> int:
    score = 0
    center_col = COLS // 2
    center_count = sum(1 for r in range(ROWS) if board.grid[r][center_col] == player)
    score += center_count * 3

    for r in range(ROWS):
        for c in range(COLS - 3):
            window = [board.grid[r][c + i] for i in range(4)]
            score += window_score(window, player)

    for c in range(COLS):
        for r in range(ROWS - 3):
            window = [board.grid[r + i][c] for i in range(4)]
            score += window_score(window, player)

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board.grid[r + i][c + i] for i in range(4)]
            score += window_score(window, player)

    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board.grid[r - i][c + i] for i in range(4)]
            score += window_score(window, player)

    return score

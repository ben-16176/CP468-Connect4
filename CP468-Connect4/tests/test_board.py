import pytest
from c4.board import Board, PLAYER1, PLAYER2

def test_legal_moves_and_gravity():
    b = Board()
    assert len(b.legal_moves()) == 7
    r = b.apply_move(3, PLAYER1)
    assert r == 5
    r2 = b.apply_move(3, PLAYER2)
    assert r2 == 4

def test_win_horizontal():
    b = Board()
    # Place four pieces across the bottom row.
    for c in range(4):
        b.apply_move(c, PLAYER1)
    assert b.winner() == PLAYER1

def test_win_vertical():
    b = Board()
    for _ in range(4):
        b.apply_move(0, PLAYER2)
    assert b.winner() == PLAYER2

def test_draw_detection():
    b = Board()
    b.grid = [
        [1, 2, 1, 1, 1, 2, 2],
        [2, 2, 1, 1, 2, 1, 1],
        [1, 1, 2, 1, 2, 1, 1],
        [2, 2, 1, 2, 1, 2, 2],
        [2, 2, 1, 2, 1, 2, 1],
        [2, 2, 2, 1, 1, 2, 2],
    ]
    assert b.is_full()
    assert b.winner() is None
    assert b.is_terminal()

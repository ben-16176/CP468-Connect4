from c4.board import Board, PLAYER1, PLAYER2
from c4.agents import MinimaxAgent
import random

def test_minimax_finds_immediate_win():
    b = Board()
    # Set up a position where Player 1 can win by playing column 3.
    b.apply_move(0, PLAYER1)
    b.apply_move(0, PLAYER2)
    b.apply_move(1, PLAYER1)
    b.apply_move(1, PLAYER2)
    b.apply_move(2, PLAYER1)
    rng = random.Random(0)
    agent = MinimaxAgent(PLAYER1, depth=2, rng=rng)
    move = agent.select_move(b)
    assert move == 3


def test_minimax_draw_board_scores_zero():
    b = Board()
    b.grid = [
        [1, 2, 1, 1, 2, 2, 2],
        [2, 1, 2, 2, 1, 1, 1],
        [1, 2, 1, 1, 2, 2, 2],
        [2, 1, 2, 2, 1, 1, 1],
        [1, 2, 1, 1, 2, 2, 2],
        [2, 1, 2, 2, 1, 1, 1],
    ]
    rng = random.Random(0)
    agent = MinimaxAgent(PLAYER1, depth=4, rng=rng)

    assert b.is_full()
    assert b.winner() is None
    assert agent._minimax(b, 0, True, PLAYER1, PLAYER2) == 0

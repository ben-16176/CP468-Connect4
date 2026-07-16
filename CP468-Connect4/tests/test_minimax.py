from c4.board import Board, PLAYER1, PLAYER2
from c4.agents import MinimaxAgent
import random

def test_minimax_finds_immediate_win():
    b = Board()
    # set up a position where player1 can win by playing col 3
    b.apply_move(0, PLAYER1)
    b.apply_move(0, PLAYER2)
    b.apply_move(1, PLAYER1)
    b.apply_move(1, PLAYER2)
    b.apply_move(2, PLAYER1)
    rng = random.Random(0)
    agent = MinimaxAgent(PLAYER1, depth=2, rng=rng)
    move = agent.select_move(b)
    assert move == 3

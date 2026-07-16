from c4.board import Board, PLAYER1, PLAYER2
from c4.agents import RandomAgent, RuleBasedAgent
import random

def test_random_agent_returns_legal():
    b = Board()
    rng = random.Random(42)
    a = RandomAgent(PLAYER1, rng)
    move = a.select_move(b)
    assert move in b.legal_moves()

def test_rule_block_immediate_win():
    b = Board()
    # opponent has three in a row at bottom columns 0,1,2
    b.apply_move(0, PLAYER2)
    b.apply_move(1, PLAYER2)
    b.apply_move(2, PLAYER2)
    rng = random.Random(123)
    agent = RuleBasedAgent(PLAYER1, rng)
    move = agent.select_move(b)
    # must block at column 3
    assert move == 3

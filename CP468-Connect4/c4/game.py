import time
from typing import Dict, List, Tuple

from c4.agents import Agent
from c4.board import Board, PLAYER1, PLAYER2


class Game:
    def __init__(self, agent1: Agent, agent2: Agent, verbose: bool = False):
        self.board = Board()
        self.agents = {PLAYER1: agent1, PLAYER2: agent2}
        self.current = PLAYER1
        self.verbose = verbose
        # Per-player list of individual move decision times (seconds),
        # one entry per select_move() call made by that player.
        self.move_times: Dict[int, List[float]] = {PLAYER1: [], PLAYER2: []}

    def play(self, max_moves: int = 1000) -> Tuple[int, int]:
        moves = 0
        while not self.board.is_terminal() and moves < max_moves:
            agent = self.agents[self.current]
            t0 = time.perf_counter()
            move = agent.select_move(self.board, self.current)
            t1 = time.perf_counter()
            self.move_times[self.current].append(t1 - t0)
            self.board.apply_move(move, self.current)
            if self.verbose:
                print(f"Player {self.current} -> col {move}")
                print(self.board)
                print("-" * 20)
            self.current = PLAYER1 if self.current == PLAYER2 else PLAYER2
            moves += 1
        winner = self.board.winner()
        if winner is None:
            return (0, moves)
        return (winner, moves)

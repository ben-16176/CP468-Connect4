import random
from typing import Optional

from c4.board import Board, PLAYER1, PLAYER2
from c4.heuristics import evaluate


class Agent:
    def __init__(self, player: int, rng: Optional[random.Random] = None, seed: Optional[int] = None):
        self.player = player
        self.rng = rng or random.Random(seed)

    def select_move(self, board: Board, player: Optional[int] = None) -> int:
        raise NotImplementedError


class RandomAgent(Agent):
    def select_move(self, board: Board, player: Optional[int] = None) -> int:
        moves = board.legal_moves()
        return self.rng.choice(moves)


class RuleBasedAgent(Agent):
    def __init__(self, player: int, rng: Optional[random.Random] = None, seed: Optional[int] = None):
        super().__init__(player, rng, seed)

    def select_move(self, board: Board, player: Optional[int] = None) -> int:
        active_player = player if player is not None else self.player
        moves = board.legal_moves()
        opp = PLAYER1 if active_player == PLAYER2 else PLAYER2

        winning = []
        for move in moves:
            b = board.copy()
            b.apply_move(move, active_player)
            if b.winner() == active_player:
                winning.append(move)
        if winning:
            return self.rng.choice(winning)

        blocks = []
        for move in moves:
            b = board.copy()
            b.apply_move(move, opp)
            if b.winner() == opp:
                blocks.append(move)
        if blocks:
            return self.rng.choice(blocks)

        # Rule 4: extend own longest line / create threats, scored via the
        # windowed heuristic (this already includes a center-column weight).
        best_score = None
        best_moves = []
        for move in moves:
            b = board.copy()
            b.apply_move(move, active_player)
            score = evaluate(b, active_player)
            if best_score is None or score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        # Rule 3: prefer central columns, applied as a tie-breaker among the
        # moves that are equally good under rule 4. (Using it as a hard
        # filter before rule 4 would make rule 4 unreachable, since some
        # move is always closest to center.)
        center = len(board.grid[0]) // 2
        min_dist = min(abs(m - center) for m in best_moves)
        central_best = [m for m in best_moves if abs(m - center) == min_dist]
        return self.rng.choice(central_best)


class MinimaxAgent(Agent):
    def __init__(self, player: int, depth: int = 4, rng: Optional[random.Random] = None, seed: Optional[int] = None):
        super().__init__(player, rng, seed)
        self.depth = depth

    def select_move(self, board: Board, player: Optional[int] = None) -> int:
        active_player = player if player is not None else self.player
        moves = board.legal_moves()
        best_value = None
        best_moves = []
        for move in moves:
            b = board.copy()
            b.apply_move(move, active_player)
            opponent = PLAYER1 if active_player == PLAYER2 else PLAYER2
            value = self._minimax(b, self.depth - 1, False, active_player, opponent)
            if best_value is None or value > best_value:
                best_value = value
                best_moves = [move]
            elif value == best_value:
                best_moves.append(move)
        return self.rng.choice(best_moves)

    def _minimax(self, board: Board, depth: int, maximizing: bool, root_player: int, current_player: int) -> int:
        winner = board.winner()
        if winner == root_player:
            return 100000 + depth
        if winner is not None:
            return -100000 - depth
        if depth == 0 or board.is_full():
            return evaluate(board, root_player)

        next_player = PLAYER1 if current_player == PLAYER2 else PLAYER2
        moves = board.legal_moves()
        if maximizing:
            value = -10**9
            for move in moves:
                b = board.copy()
                b.apply_move(move, current_player)
                value = max(value, self._minimax(b, depth - 1, False, root_player, next_player))
            return value

        value = 10**9
        for move in moves:
            b = board.copy()
            b.apply_move(move, current_player)
            value = min(value, self._minimax(b, depth - 1, True, root_player, next_player))
        return value

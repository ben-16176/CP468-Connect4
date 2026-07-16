from c4.agents import MinimaxAgent, RandomAgent, RuleBasedAgent
from c4.board import Board, PLAYER1, PLAYER2
from c4.game import Game


def print_match(agent_a_cls, agent_b_cls, games=3, seed=42):
    print(f"Starting {games} games with seed {seed}")
    for idx in range(games):
        player1_cls = agent_a_cls if idx % 2 == 0 else agent_b_cls
        player2_cls = agent_b_cls if idx % 2 == 0 else agent_a_cls
        a = player1_cls(PLAYER1, seed=seed + idx * 10)
        b = player2_cls(PLAYER2, seed=seed + idx * 10 + 1)
        game = Game(a, b)
        winner, moves = game.play()
        print(f"Game {idx + 1}: winner={winner}, moves={moves}")


if __name__ == "__main__":
    print_match(RandomAgent, RuleBasedAgent, games=3, seed=42)

import argparse
import os
import platform
import random
import sys
from statistics import mean

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from c4.agents import MinimaxAgent, RandomAgent, RuleBasedAgent
from c4.board import PLAYER1, PLAYER2
from c4.game import Game


def get_environment_summary():
    return {
        "cpu": platform.processor() or "Unknown",
        "ram": "Unknown",
        "os": platform.platform(),
        "language": "Python",
        "language_version": platform.python_version(),
    }


def run_pairing(agent_a_cls, agent_b_cls, games=30, depth=4, seed=0):
    rng = random.Random(seed)
    # Keep track of wins, draws, and move timings for both agents.
    results = {"A": 0, "B": 0, "draw": 0, "times": {"A": [], "B": []}, "details": []}
    for i in range(games):
        # Alternate who plays first so the results are more balanced.
        if i % 2 == 0:
            a = agent_a_cls(1, seed=rng.randint(0, 10**9)) if agent_a_cls is not None else None
            b = agent_b_cls(2, seed=rng.randint(0, 10**9)) if agent_b_cls is not None else None
            game = Game(a, b)
            start = 1  # A is the first player in this game
        else:
            a = agent_a_cls(2, seed=rng.randint(0, 10**9)) if agent_a_cls is not None else None
            b = agent_b_cls(1, seed=rng.randint(0, 10**9)) if agent_b_cls is not None else None
            game = Game(b, a)
            start = 2  # B is the first player in this game

        winner, num_moves = game.play()

        # Store the timing data for the correct side of the matchup.
        if start == 1:
            a_times = game.move_times[PLAYER1]
            b_times = game.move_times[PLAYER2]
        else:
            a_times = game.move_times[PLAYER2]
            b_times = game.move_times[PLAYER1]
        results["times"]["A"].extend(a_times)
        results["times"]["B"].extend(b_times)

        if winner == 0:
            results["draw"] += 1
            outcome = "draw"
        else:
            if start == 1:
                if winner == 1:
                    results["A"] += 1
                    outcome = "A"
                else:
                    results["B"] += 1
                    outcome = "B"
            else:
                if winner == 1:
                    results["B"] += 1
                    outcome = "B"
                else:
                    results["A"] += 1
                    outcome = "A"
        results["details"].append((i + 1, outcome, num_moves))

    # Average the recorded move times for each agent.
    avg_a = mean(results["times"]["A"]) if results["times"]["A"] else 0
    avg_b = mean(results["times"]["B"]) if results["times"]["B"] else 0
    return {
        "wins_A": results["A"],
        "wins_B": results["B"],
        "draws": results["draw"],
        "avg_time_A_per_move": avg_a,
        "avg_time_B_per_move": avg_b,
        "moves_timed_A": len(results["times"]["A"]),
        "moves_timed_B": len(results["times"]["B"]),
        "seed": seed,
        "details": results["details"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    # Run a few example matchups and print the results.
    env = get_environment_summary()
    print("Environment Specifications")
    print(f"CPU: {env['cpu']}")
    print(f"RAM: {env['ram']}")
    print(f"OS: {env['os']}")
    print(f"Language: {env['language']} {env['language_version']}")
    print()
    print("Random vs Rule-Based")
    result1 = run_pairing(RandomAgent, RuleBasedAgent, games=30, seed=args.seed)
    print({
        "wins_A": result1["wins_A"],
        "wins_B": result1["wins_B"],
        "draws": result1["draws"],
        "avg_time_A_per_move": result1["avg_time_A_per_move"],
        "avg_time_B_per_move": result1["avg_time_B_per_move"],
    })

    print("Rule-Based vs Minimax")
    result2 = run_pairing(RuleBasedAgent, lambda p, seed=None: MinimaxAgent(p, depth=4, seed=seed), games=30, seed=args.seed + 1)
    print({
        "wins_A": result2["wins_A"],
        "wins_B": result2["wins_B"],
        "draws": result2["draws"],
        "avg_time_A_per_move": result2["avg_time_A_per_move"],
        "avg_time_B_per_move": result2["avg_time_B_per_move"],
    })

    print("Minimax vs Random")
    result3 = run_pairing(lambda p, seed=None: MinimaxAgent(p, depth=4, seed=seed), RandomAgent, games=30, seed=args.seed + 2)
    print({
        "wins_A": result3["wins_A"],
        "wins_B": result3["wins_B"],
        "draws": result3["draws"],
        "avg_time_A_per_move": result3["avg_time_A_per_move"],
        "avg_time_B_per_move": result3["avg_time_B_per_move"],
    })

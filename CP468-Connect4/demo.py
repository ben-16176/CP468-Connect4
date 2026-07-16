import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from c4.agents import MinimaxAgent, RandomAgent, RuleBasedAgent
from c4.board import PLAYER1, PLAYER2
from c4.game import Game


def main():
    # Show the available demo options to the user.
    print("\n=== Connect 4 Agent Demo ===\n")
    print("1. Random vs Rule-Based (5 games) - show first game")
    print("2. Rule-Based vs Minimax (5 games) - show first game")
    print("3. Minimax vs Random (5 games) - show first game")
    print("4. Run full experiments (30 games each) - summary only")
    print("5. Watch a single game with full board display")
    print("0. Exit\n")

    choice = input("Select option (0-5): ").strip()

    if choice == "1":
        run_match(RandomAgent, RuleBasedAgent, 5, "Random", "Rule-Based", show_first=True)
    elif choice == "2":
        run_match(RuleBasedAgent, lambda p, seed: MinimaxAgent(p, depth=4, seed=seed), 5, "Rule-Based", "Minimax", show_first=True)
    elif choice == "3":
        run_match(lambda p, seed: MinimaxAgent(p, depth=4, seed=seed), RandomAgent, 5, "Minimax", "Random", show_first=True)
    elif choice == "4":
        run_full_experiments()
    elif choice == "5":
        print("\n1. Random vs Rule-Based")
        print("2. Rule-Based vs Minimax")
        print("3. Minimax vs Random\n")
        watch_choice = input("Select matchup (1-3): ").strip()
        if watch_choice == "1":
            watch_game(RandomAgent, RuleBasedAgent, "Random", "Rule-Based")
        elif watch_choice == "2":
            watch_game(RuleBasedAgent, lambda p, seed: MinimaxAgent(p, depth=4, seed=seed), "Rule-Based", "Minimax")
        elif watch_choice == "3":
            watch_game(lambda p, seed: MinimaxAgent(p, depth=4, seed=seed), RandomAgent, "Minimax", "Random")
    elif choice == "0":
        print("Exiting.")
        return
    else:
        print("Invalid choice.")


def run_match(agent_a_cls, agent_b_cls, games, name_a, name_b, show_first=False):
    # Run a set of games and report the results for the matchup.
    print(f"\n=== {name_a} vs {name_b} ({games} games) ===\n")
    wins_a, wins_b, draws = 0, 0, 0

    for i in range(games):
        verbose = show_first and i == 0
        # Alternate who is Player 1 so both sides get a fair share of turns.
        
        player1_cls = agent_a_cls if i % 2 == 0 else agent_b_cls
        player2_cls = agent_b_cls if i % 2 == 0 else agent_a_cls
        player1_name = name_a if i % 2 == 0 else name_b
        player2_name = name_b if i % 2 == 0 else name_a
        
        a = player1_cls(PLAYER1, seed=42 + i)
        b = player2_cls(PLAYER2, seed=43 + i)
        game = Game(a, b, verbose=verbose)
        
        if verbose:
            print(f"Game {i+1}: {player1_name} (Player 1) vs {player2_name} (Player 2)")
            print("Initial board:\n")
            print(game.board)
            print("-" * 20 + "\n")
        
        winner, moves = game.play()

        if winner == PLAYER1:
            result = player1_name
            if i % 2 == 0:
                wins_a += 1
            else:
                wins_b += 1
        elif winner == PLAYER2:
            result = player2_name
            if i % 2 == 0:
                wins_b += 1
            else:
                wins_a += 1
        else:
            result = "Draw"
            draws += 1

        if verbose:
            print(f"Game {i+1} Result: {result} ({moves} moves)\n")
        else:
            print(f"Game {i+1}: {result} ({moves} moves)")

    print(f"\n{name_a}: {wins_a} wins")
    print(f"{name_b}: {wins_b} wins")
    print(f"Draws: {draws}\n")


def run_full_experiments():
    # Run the full experiment set for each matchup.
    print("\n=== Running Full Experiments (30 games each) ===\n")

    print("Random vs Rule-Based:")
    run_match(RandomAgent, RuleBasedAgent, 30, "Random", "Rule-Based")

    print("Rule-Based vs Minimax:")
    run_match(RuleBasedAgent, lambda p, seed: MinimaxAgent(p, depth=4, seed=seed), 30, "Rule-Based", "Minimax")

    print("Minimax vs Random:")
    run_match(lambda p, seed: MinimaxAgent(p, depth=4, seed=seed), RandomAgent, 30, "Minimax", "Random")


def watch_game(agent_a_cls, agent_b_cls, name_a, name_b):
    """Play one game and show the board after every move."""
    print(f"\n=== {name_a} (Player 1) vs {name_b} (Player 2) ===\n")
    
    a = agent_a_cls(PLAYER1, seed=42)
    b = agent_b_cls(PLAYER2, seed=43)
    game = Game(a, b, verbose=True)
    
    print("Initial board:\n")
    print(game.board)
    print("-" * 20 + "\n")
    
    winner, moves = game.play()
    
    print("\nFinal board:\n")
    print(game.board)
    
    if winner == PLAYER1:
        print(f"\n{name_a} wins in {moves} moves!")
    elif winner == PLAYER2:
        print(f"\n{name_b} wins in {moves} moves!")
    else:
        print(f"\nDraw after {moves} moves!")
    print()


if __name__ == "__main__":
    main()

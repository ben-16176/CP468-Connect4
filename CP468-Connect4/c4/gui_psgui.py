"""
PySimpleGUI-based graphical interface for Connect 4.
Alternative to Tkinter when display environments have issues.
"""

import PySimpleGUI as sg
from c4.board import Board, PLAYER1, PLAYER2, ROWS, COLS
from c4.game import Game
from c4.agents import RandomAgent, RuleBasedAgent, MinimaxAgent


# Set theme
sg.theme('DarkBlue3')


def get_agent_class(agent_name):
    """Return the agent class for the given name."""
    if agent_name == "Random":
        return RandomAgent
    elif agent_name == "Rule-Based":
        return RuleBasedAgent
    elif agent_name == "Minimax":
        return lambda p, seed: MinimaxAgent(p, depth=4, seed=seed)
    else:
        return RandomAgent


def launch_gui():
    """Launch the PySimpleGUI-based Connect 4 interface."""
    
    # Mode selection layout
    mode_layout = [
        [sg.Text("Connect 4 - Select Mode", font=("Helvetica", 16, "bold"))],
        [sg.Text("")],
        [sg.Text("Player 1:", font=("Helvetica", 12))],
        [sg.Radio("Human", "player1", default=True, key="HUMAN_P1"), 
         sg.Radio("Random", "player1", key="RANDOM_P1"),
         sg.Radio("Rule-Based", "player1", key="RULE_P1"),
         sg.Radio("Minimax", "player1", key="MINIMAX_P1")],
        [sg.Text("")],
        [sg.Text("Player 2:", font=("Helvetica", 12))],
        [sg.Radio("Human", "player2", default=False, key="HUMAN_P2"),
         sg.Radio("Random", "player2", default=True, key="RANDOM_P2"),
         sg.Radio("Rule-Based", "player2", key="RULE_P2"),
         sg.Radio("Minimax", "player2", key="MINIMAX_P2")],
        [sg.Text("")],
        [sg.Button("Start Game"), sg.Button("Cancel")]
    ]
    
    mode_window = sg.Window("Connect 4 Setup", mode_layout, finalize=True)
    
    while True:
        event, values = mode_window.read()
        
        if event == sg.WINDOW_CLOSED or event == "Cancel":
            mode_window.close()
            return None
        
        if event == "Start Game":
            mode_window.close()
            
            # Determine player 1 type
            if values["HUMAN_P1"]:
                p1_type = "Human"
            elif values["RANDOM_P1"]:
                p1_type = "Random"
            elif values["RULE_P1"]:
                p1_type = "Rule-Based"
            else:
                p1_type = "Minimax"
            
            # Determine player 2 type
            if values["HUMAN_P2"]:
                p2_type = "Human"
            elif values["RANDOM_P2"]:
                p2_type = "Random"
            elif values["RULE_P2"]:
                p2_type = "Rule-Based"
            else:
                p2_type = "Minimax"
            
            return (p1_type, p2_type)


def render_board(board):
    """Convert board state to visual representation."""
    lines = []
    lines.append("  0 1 2 3 4 5 6")
    for row in range(ROWS):
        row_str = f"{row} "
        for col in range(COLS):
            cell = board.grid[row][col]
            if cell == 0:
                row_str += "· "
            elif cell == PLAYER1:
                row_str += "🔵 "
            else:  # PLAYER2
                row_str += "🔴 "
        lines.append(row_str)
    return "\n".join(lines)


def play_game_gui(p1_type, p2_type):
    """Run a game with the specified agent types."""
    
    board = Board()
    
    # Create agents
    if p1_type == "Human":
        p1_agent = None
    else:
        p1_agent = get_agent_class(p1_type)(PLAYER1, seed=42)
    
    if p2_type == "Human":
        p2_agent = None
    else:
        p2_agent = get_agent_class(p2_type)(PLAYER2, seed=43)
    
    current_player = PLAYER1
    move_count = 0
    game_over = False
    winner = None
    
    # Game loop layout
    layout = [
        [sg.Text("Connect 4 Game", font=("Helvetica", 16, "bold"))],
        [sg.Multiline(render_board(board), size=(25, 15), key="BOARD", disabled=True, font=("Courier", 10))],
        [sg.Text(f"Current: {'Player 1 (Blue)' if current_player == PLAYER1 else 'Player 2 (Red)'}", 
                 key="STATUS", font=("Helvetica", 12))],
        [sg.Button("0"), sg.Button("1"), sg.Button("2"), sg.Button("3"), 
         sg.Button("4"), sg.Button("5"), sg.Button("6"), sg.Button("Restart"), sg.Button("Exit")],
        [sg.Multiline("", size=(40, 8), key="LOG", disabled=True, font=("Courier", 9))]
    ]
    
    game_window = sg.Window("Connect 4", layout, finalize=True)
    log_messages = []
    
    def add_log(msg):
        log_messages.append(msg)
        game_window["LOG"].update("\n".join(log_messages[-20:]))  # Keep last 20 messages
    
    add_log(f"Game Started: {p1_type} vs {p2_type}")
    
    while True:
        event, values = game_window.read(timeout=500)
        
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        
        if event == "Restart":
            game_window.close()
            return
        
        if game_over:
            if event in ["Restart", "Exit"]:
                continue
            game_window["STATUS"].update("Game Over - Click Restart or Exit")
            continue
        
        # AI move
        if current_player == PLAYER1 and p1_agent is not None:
            legal = board.legal_moves()
            if legal:
                move = p1_agent.select_move(board, PLAYER1)
                if board.apply_move(move, PLAYER1):
                    add_log(f"Player 1 ({p1_type}): Column {move}")
                    move_count += 1
                    current_player = PLAYER2
        
        elif current_player == PLAYER2 and p2_agent is not None:
            legal = board.legal_moves()
            if legal:
                move = p2_agent.select_move(board, PLAYER2)
                if board.apply_move(move, PLAYER2):
                    add_log(f"Player 2 ({p2_type}): Column {move}")
                    move_count += 1
                    current_player = PLAYER1
        
        # Check terminal
        winner = board.winner()
        if winner is not None or board.is_full():
            game_over = True
            if winner == PLAYER1:
                add_log(f"Player 1 ({p1_type}) wins!")
                game_window["STATUS"].update(f"Player 1 ({p1_type}) wins in {move_count} moves!")
            elif winner == PLAYER2:
                add_log(f"Player 2 ({p2_type}) wins!")
                game_window["STATUS"].update(f"Player 2 ({p2_type}) wins in {move_count} moves!")
            else:
                add_log("Draw!")
                game_window["STATUS"].update(f"Draw after {move_count} moves!")
        else:
            # Human player move
            if current_player == PLAYER1 and p1_agent is None:
                game_window["STATUS"].update("Player 1 (Blue) - Select a column (0-6)")
            elif current_player == PLAYER2 and p2_agent is None:
                game_window["STATUS"].update("Player 2 (Red) - Select a column (0-6)")
        
        # Handle column selection
        if event in ["0", "1", "2", "3", "4", "5", "6"]:
            col = int(event)
            
            if current_player == PLAYER1 and p1_agent is None:
                if board.apply_move(col, PLAYER1):
                    add_log(f"Player 1 (Human): Column {col}")
                    move_count += 1
                    current_player = PLAYER2
                else:
                    add_log(f"Invalid move: Column {col} is full")
            
            elif current_player == PLAYER2 and p2_agent is None:
                if board.apply_move(col, PLAYER2):
                    add_log(f"Player 2 (Human): Column {col}")
                    move_count += 1
                    current_player = PLAYER1
                else:
                    add_log(f"Invalid move: Column {col} is full")
        
        # Update board display
        game_window["BOARD"].update(render_board(board))
    
    game_window.close()


def main():
    """Launch the PySimpleGUI Connect 4 application."""
    while True:
        result = launch_gui()
        if result is None:
            break
        
        p1_type, p2_type = result
        play_game_gui(p1_type, p2_type)


if __name__ == "__main__":
    main()

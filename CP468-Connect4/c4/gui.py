import tkinter as tk
from typing import Optional

from c4.agents import MinimaxAgent, RandomAgent, RuleBasedAgent
from c4.board import Board, PLAYER1, PLAYER2, ROWS, COLS


class Connect4GUI:
    def __init__(self, root: tk.Tk, player1_mode: str = "human", player2_mode: str = "human", ai_agent1=None, ai_agent2=None):
        self.root = root
        self.root.title("Connect 4")
        self.board = Board()
        self.player1_mode = player1_mode
        self.player2_mode = player2_mode
        self.ai_agent1 = ai_agent1 or self._build_agent(player1_mode, PLAYER1)
        self.ai_agent2 = ai_agent2 or self._build_agent(player2_mode, PLAYER2)
        self.current_player = PLAYER1
        self.cell_size = 80
        self.canvas = tk.Canvas(root, width=COLS * self.cell_size, height=(ROWS + 1) * self.cell_size, bg="#1e3a8a")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(root, textvariable=self.status_var, font=("Arial", 16, "bold"))
        self.status_label.pack(pady=6)
        self.restart_button = tk.Button(root, text="Restart", command=self.reset_game, font=("Arial", 14))
        self.restart_button.pack(pady=4)
        self.back_button = tk.Button(root, text="Back to Menu", command=self.back_to_menu, font=("Arial", 14))
        self.back_button.pack(pady=4)
        self.root.after(100, self.after_start)

    def _build_agent(self, mode: str, player: int):
        if mode == "human":
            return None
        if mode == "random":
            return RandomAgent(player, seed=42)
        if mode == "rule":
            return RuleBasedAgent(player, seed=42)
        if mode == "minimax":
            return MinimaxAgent(player, depth=4, seed=42)
        # Fall back to a basic AI if the mode is unknown.
        return RandomAgent(player, seed=42)

    def after_start(self):
        self._update_status_for_current_player()
        if self.current_player == PLAYER1 and self.player1_mode != "human":
            self.play_ai_turn()
        elif self.current_player == PLAYER2 and self.player2_mode != "human":
            self.play_ai_turn()

    def _is_human_turn(self) -> bool:
        if self.current_player == PLAYER1:
            return self.player1_mode == "human"
        if self.current_player == PLAYER2:
            return self.player2_mode == "human"
        return False

    def _get_status_text(self) -> str:
        if self.current_player is None:
            return "Game over"
        player_color = "red" if self.current_player == PLAYER1 else "yellow"
        if self._is_human_turn():
            return f"Your turn ({player_color})"
        return f"AI turn ({player_color})"

    def _update_status_for_current_player(self):
        self.status_var.set(self._get_status_text())

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x1 = c * self.cell_size
                y1 = (r + 1) * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#dbeafe", outline="")

                if r > 0:
                    self.canvas.create_line(x1, y1, x2, y1, fill="black", width=2)
                self.canvas.create_line(x1, y2, x2, y2, fill="black", width=2)
                self.canvas.create_line(x1, y1, x1, y2, fill="black", width=2)
                self.canvas.create_line(x2, y1, x2, y2, fill="black", width=2)

                value = self.board.grid[r][c]
                if value == PLAYER1:
                    self.canvas.create_oval(x1 + 8, y1 + 8, x2 - 8, y2 - 8, fill="#ef4444")
                elif value == PLAYER2:
                    self.canvas.create_oval(x1 + 8, y1 + 8, x2 - 8, y2 - 8, fill="#facc15")

    def on_click(self, event):
        if not self._is_human_turn():
            return
        col = column_from_x(event.x, self.cell_size, COLS)
        if col is None:
            return
        self.play_human_move(col)

    def play_human_move(self, col: int):
        if self.current_player is None or col not in self.board.legal_moves():
            return
        self.board.apply_move(col, self.current_player)
        self.draw_board()
        if self.board.winner() == self.current_player:
            winner_name = "Player 1" if self.current_player == PLAYER1 else "Player 2"
            self.status_var.set(f"{winner_name} wins!")
            self.current_player = None
            return
        if self.board.is_full():
            self.status_var.set("Draw")
            self.current_player = None
            return
        self.current_player = PLAYER1 if self.current_player == PLAYER2 else PLAYER2
        self._update_status_for_current_player()
        if not self._is_human_turn():
            self.root.after(300, self.play_ai_turn)

    def play_ai_turn(self):
        if self.current_player is None:
            return
        if self.current_player == PLAYER1 and self.player1_mode == "human":
            return
        if self.current_player == PLAYER2 and self.player2_mode == "human":
            return
        if not self.board.legal_moves():
            self.status_var.set("Draw")
            return

        agent = self.ai_agent1 if self.current_player == PLAYER1 else self.ai_agent2
        if agent is None:
            self.current_player = PLAYER1 if self.current_player == PLAYER2 else PLAYER2
            self._update_status_for_current_player()
            return

        move = agent.select_move(self.board, self.current_player)
        self.board.apply_move(move, self.current_player)
        self.draw_board()
        if self.board.winner() == self.current_player:
            winner_name = "Player 1" if self.current_player == PLAYER1 else "Player 2"
            self.status_var.set(f"{winner_name} wins!")
            self.current_player = None
            return
        if self.board.is_full():
            self.status_var.set("Draw")
            self.current_player = None
            return
        self.current_player = PLAYER1 if self.current_player == PLAYER2 else PLAYER2
        self._update_status_for_current_player()
        if not self._is_human_turn():
            self.root.after(300, self.play_ai_turn)

    def reset_game(self):
        self.board = Board()
        self.current_player = PLAYER1
        self.draw_board()
        self._update_status_for_current_player()
        self.root.after(100, self.after_start)

    def back_to_menu(self):
        if self.root is not None:
            self.root.destroy()
        launch_gui()


def column_from_x(x: int, cell_size: int, cols: int) -> Optional[int]:
    if x < 0 or x >= cols * cell_size:
        return None
    return min(cols - 1, x // cell_size)


def launch_gui():
    # Open the setup window as a normal Tk window.
    dialog = tk.Tk()
    dialog.title("Select game mode")
    # Leave the size automatic so all buttons stay visible.

    tk.Label(dialog, text="Choose player 1 mode", font=("Arial", 15, "bold")).pack(pady=(10, 4))
    player1_var = tk.StringVar(value="human")
    tk.Radiobutton(dialog, text="Human", variable=player1_var, value="human").pack(anchor="w", padx=20)
    tk.Radiobutton(dialog, text="Random AI", variable=player1_var, value="random").pack(anchor="w", padx=20)
    tk.Radiobutton(dialog, text="Rule-Based AI", variable=player1_var, value="rule").pack(anchor="w", padx=20)
    tk.Radiobutton(dialog, text="Minimax AI", variable=player1_var, value="minimax").pack(anchor="w", padx=20)

    tk.Label(dialog, text="Choose player 2 mode", font=("Arial", 15, "bold")).pack(pady=(10, 4))
    player2_var = tk.StringVar(value="random")
    tk.Radiobutton(dialog, text="Human", variable=player2_var, value="human").pack(anchor="w", padx=20)
    tk.Radiobutton(dialog, text="Random AI", variable=player2_var, value="random").pack(anchor="w", padx=20)
    tk.Radiobutton(dialog, text="Rule-Based AI", variable=player2_var, value="rule").pack(anchor="w", padx=20)
    tk.Radiobutton(dialog, text="Minimax AI", variable=player2_var, value="minimax").pack(anchor="w", padx=20)

    def start_game():
        p1_mode = player1_var.get()
        p2_mode = player2_var.get()
        dialog.destroy()
        game_root = tk.Tk()
        Connect4GUI(game_root, p1_mode, p2_mode)
        game_root.mainloop()

    tk.Button(dialog, text="Start Game", command=start_game, font=("Arial", 14, "bold")).pack(pady=12)
    dialog.mainloop()


if __name__ == "__main__":
    launch_gui()

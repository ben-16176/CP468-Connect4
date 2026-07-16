from c4.board import Board, PLAYER1, PLAYER2
from c4.gui import Connect4GUI, column_from_x


def test_column_from_x_maps_clicks_to_columns():
    assert column_from_x(40, 80, 7) == 0
    assert column_from_x(120, 80, 7) == 1
    assert column_from_x(200, 80, 7) == 2
    assert column_from_x(9999, 80, 7) is None


def test_play_human_move_uses_current_player_for_player_two():
    gui = Connect4GUI.__new__(Connect4GUI)
    gui.board = Board()
    gui.current_player = PLAYER2
    gui.player1_mode = "human"
    gui.player2_mode = "human"
    gui.root = None
    gui.status_var = None

    def noop(*args, **kwargs):
        return None

    gui.draw_board = noop
    gui._update_status_for_current_player = noop

    gui.play_human_move(0)

    assert gui.board.grid[5][0] == PLAYER2
    assert gui.current_player == PLAYER1

import numpy as np
from agents.common import BoardPiece, NO_PLAYER

def test_initialize_game_state():
    from agents.common import initialize_game_state

    ret = initialize_game_state()

    assert isinstance(ret, np.ndarray)
    assert ret.dtype == BoardPiece
    assert ret.shape == (6, 7)
    assert np.all(ret == NO_PLAYER)

    """
    assert CONDITON , "OutputString"
    """

def test_pretty_print_board():
    from agents.common import pretty_print_board


def test_string_to_board():
    from agents.common import string_to_board

def test_apply_player_action():
    from agents.common import apply_player_action

def test_connected_four():
    from agents.common import connected_four

def test_check_end_state():
    from agents.common import check_end_state




from enum import Enum
from typing import Optional
import numpy as np
from typing import Callable, Tuple


BoardPiece = np.int8  # The data type (dtype) of the board
NO_PLAYER = BoardPiece(0)  # board[i, j] == NO_PLAYER where the position is empty
PLAYER1 = BoardPiece(1)  # board[i, j] == PLAYER1 where player 1 has a piece
PLAYER2 = BoardPiece(2)  # board[i, j] == PLAYER2 where player 2 has a piece

BoardPiecePrint = str  # dtype for string representation of BoardPiece
NO_PLAYER_PRINT = str(' ')
PLAYER1_PRINT = str('X')
PLAYER2_PRINT = str('O')

PlayerAction = np.int8  # The column to be played


class SavedState:
    def __init__(self, computational_result):
        self.computational_result = computational_result

GenMove = Callable[
    [np.ndarray, BoardPiece, Optional[SavedState]],  # Arguments for the generate_move function
    Tuple[PlayerAction, Optional[SavedState]]  # Return type of the generate_move function
]

class GameState(Enum):
    IS_WIN = 1
    IS_DRAW = -1
    STILL_PLAYING = 0


def initialize_game_state() -> np.ndarray:
    """
    Returns an ndarray, shape (6, 7) and data type (dtype) BoardPiece, initialized to 0 (NO_PLAYER).
    """
    board = np.full((6, 7), NO_PLAYER)

    return board
    # raise NotImplementedError() # forget not implemented yet


def pretty_print_board(board: np.ndarray) -> str:
    """
    Should return `board` converted to a human readable string representation,
    to be used when playing or printing diagnostics to the console (stdout). The piece in
    board[0, 0] should appear in the lower-left. Here's an example output:
    |==============|
    |              |
    |              |
    |    X X       |
    |    O X X     |
    |  O X O O     |
    |  O O X X     |
    |==============|
    |0 1 2 3 4 5 6 |
    """

    x, y = np.shape(board)

    board_str = '|'
    for l in range(0,y):
        board_str += '=='
    board_str += '|\n'

    for i in range(0, x):
        string = '|'

        for j in range(0, y):
            if board[i, j] == NO_PLAYER:
                string += NO_PLAYER_PRINT
            elif board[i, j] == PLAYER1:
                string += PLAYER1_PRINT
            elif board[i, j] == PLAYER2:
                string += PLAYER2_PRINT
            string += ' '
        board_str += string + '|\n'

    board_str += '|'
    for l in range(0, y):
        board_str += '=='
    board_str += '|\n'

    board_str += '|'
    for p in range(0,y):
        board_str += str(p) +' '
    board_str += '|'

    return board_str

    # raise NotImplementedError()


def string_to_board(pp_board: str) -> np.ndarray:
    """
    Takes the output of pretty_print_board and turns it back into an ndarray.
    This is quite useful for debugging, when the agent crashed and you have the last
    board state as a string.
    """

    start = 0
    board_out = np.ndarray([])
    for line in pp_board.split('\n'):
        if '=' in line:
            start += 1
        elif '=' not in line and start<2:
            line = line[1:-2:2]
            line_np = np.array([])
            for j in range(0,len(line)):
                if line[j] == NO_PLAYER_PRINT:
                    line_np = np.append(line_np,NO_PLAYER)
                elif line[j] == PLAYER1_PRINT:
                    line_np = np.append(line_np, PLAYER1)
                elif line[j] == PLAYER2_PRINT:
                        line_np = np.append(line_np, PLAYER2)
            board_out = np.append(board_out,line_np,axis = 0)

    return board_out
    # raise NotImplementedError()


def apply_player_action(
        board: np.ndarray, action: PlayerAction, player: BoardPiece, copy: bool = False, pos : bool = False
) :
    """
    Sets board[i, action] = player, where i is the lowest open row. The modified
    board is returned. If copy is True, makes a copy of the board before modifying it.
    :type board: object
    """
    old_board = np.copy(board)
    row = sum(board[:, action] == 0) - 1
    position = 0
    if row>= 0:
        board[row, action] = player
        position = row, action

    if copy and not pos:
        return old_board
    elif pos and not copy:
        return position
    else:
        return old_board, position


def findall(element, matrix):
    result = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == element:
                result.append([i, j])
    return np.array(result)


def connected_four(
        board: np.ndarray, player: BoardPiece, last_action: Optional[PlayerAction] = None,
) -> bool:
    """
    Returns True if there are four adjacent pieces equal to `player` arranged
    in either a horizontal, vertical, or diagonal line. Returns False otherwise.
    If desired, the last action taken (i.e. last column played) can be provided
    for potential speed optimisation.
    """
    indexes = findall(player, board)
    x, y = np.shape(board)

    dirs = np.array([[1, 1], [1, -1], [1, 0], [0, 1]])
    sums = np.zeros((indexes.shape[0], 4))

    for i in range(0, indexes.shape[0]):
        for j in range(0, 4):

            new_ind = indexes[i]
            dim = False
            break_0 = False

            while break_0 == False and dim == False:
                if new_ind[0] > x - 1 or new_ind[1] > y - 1 or new_ind[0] < 0 or new_ind[1] < 0:
                    dim = True
                elif player != board[new_ind[0], new_ind[1]]:
                    break_0 = True
                else:
                    sums[i, j] += 1
                    new_ind = new_ind + dirs[j]

            break_0 = dim = False
            sums[i, j] -= 1
            new_ind = indexes[i]

            while break_0 == False and dim == False:
                if new_ind[0] > x - 1 or new_ind[1] > y - 1 or new_ind[0] < 0 or new_ind[1] < 0:
                    dim = True
                elif player != board[new_ind[0], new_ind[1]]:
                    break_0 = True
                else:
                    sums[i, j] += 1
                    new_ind = new_ind - dirs[j]

    if np.sum(sums >= 4) > 0:
        return True
    else:
        return False
    # raise NotImplementedError()


def check_end_state(
        board: np.ndarray, player: BoardPiece, last_action: Optional[PlayerAction] = None,
) -> object:
    """
    Returns the current game state for the current `player`, i.e. has their last
    action won (GameState.IS_WIN) or drawn (GameState.IS_DRAW) the game,
    or is play still on-going (GameState.STILL_PLAYING)?
    :rtype: object
    """

    if connected_four(board, player):
        return GameState.IS_WIN
    elif np.sum(board == 0) == 0 and not connected_four(board, player):
        return GameState.IS_DRAW
    else:
        return GameState.STILL_PLAYING

    # raise NotImplementedError()


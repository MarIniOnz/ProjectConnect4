import numpy as np
from typing import Optional
from agents.common import GameState, BoardPiece, PlayerAction, SavedState, check_end_state, apply_player_action

""" Minimax algorithm.

This file contains all the necessary functions and values needed for the
execution of the minimax agent in the main.py file.

    Typical usage example:

    human_vs_agent(minimax_action)

"""


class Tree:

    def __init__(self, value, alpha, beta):
        self.value = value
        self.children = []
        self.alpha = alpha
        self.beta = beta

    def add_node(self, value, alpha, beta):
        self.children.append(Tree(value, alpha, beta))


board_values = np.array([[3, 4, 5, 7, 5, 4, 3],
                         [4, 6, 8, 10, 8, 6, 4],
                         [5, 8, 11, 13, 11, 8, 5],
                         [5, 8, 11, 13, 11, 8, 5],
                         [4, 6, 8, 10, 8, 6, 4],
                         [3, 4, 5, 7, 5, 4, 3]])


def minmax_tree() -> Tree:
    alpha = -np.inf
    beta = np.inf
    min_tree = Tree(0, alpha, beta)

    for i in range(0, 7):
        min_tree.add_node(-np.inf, alpha, beta)
        for j in range(0, 7):
            min_tree.children[i].add_node(+np.inf, alpha, beta)
            for k in range(0, 7):
                min_tree.children[i].children[j].add_node(-np.inf, alpha, beta)
                for l in range(0, 7):
                    min_tree.children[i].children[j].children[k].add_node(+np.inf, alpha, beta)

    return min_tree


def assign_weight(board, pos_tree, player, board_values=board_values) -> object:
    old_board, position = apply_player_action(board, pos_tree, player, True, True)
    value = check_end_state(board, player)
    if position != 0:
        val_board = board_values[position]
    else:
        val_board = 100
    if value == GameState.IS_DRAW:
        value = GameState.STILL_PLAYING
    return value, old_board, val_board


def new_max_child(w_tree, index):
    maxi = -np.inf
    idx = np.random.randint(7)
    for l in index:
        new_val = w_tree.children[l].alpha
        if new_val > maxi:
            maxi = new_val
            idx = l
    return idx, maxi


def max_child(w_tree, index):
    maxi = -np.inf
    idx = np.random.randint(7)
    for l in index:
        new_val = w_tree.children[l].value
        if new_val > maxi:
            maxi = new_val
            idx = l
    return idx, maxi


def min_child(w_tree, index):
    mini = np.inf
    idx = np.random.randint(7)
    for l in index:
        new_val = w_tree.children[l].value
        if new_val < mini:
            mini = new_val
            idx = l
    return idx, mini


def eval_step(choice_, board_val, i, idx, game, Min=np.array([1])):
    break_y = False

    if board_val == 100:
        choice_new = Min * np.inf
        break_y = True
    else:
        choice_new = choice_ - Min * board_val
        # choice_new = choice_ + board_val
        idx.append(i)

    if game == GameState.IS_WIN:
        choice_new = -Min * np.inf
        idx.append(i)
        # choice_new = np.inf
        break_y = True

    return break_y, choice_new


def s_minimax_action(board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]):
    # -> Tuple[PlayerAction, Optional[SavedState]]:
    """
        Enter the current state of the board and "best" non-full column
        to perform the next movement, returning it as "action"
    """
    global otherp
    w_tree = minmax_tree()  # Weights tree

    if player == BoardPiece(1):
        otherp = BoardPiece(2)
    elif player == BoardPiece(2):
        otherp = BoardPiece(1)

    idx1 = []
    start = -1

    for i in range(0, 7):  # player plays
        choice_v1 = 0
        old_board = board.copy()

        # It is always best to start with central columnn.
        if sum(sum(old_board[:, :]) == 0) == 7:
            start = 10
            break

        game, board, board_val = assign_weight(old_board, i, player, board_values)
        break_y, choice_v1 = eval_step(choice_v1, board_val, i, idx1, game, Min=np.array([-1]))

        if break_y and choice_v1 > 10000:
            w_tree.children[i].value = choice_v1
            break
        elif break_y and choice_v1 < 10000:
            continue

        idx2 = []

        for j in range(0, 7):  # other player plays
            old_board1 = old_board.copy()

            game, new_b2, board_val = assign_weight(old_board1, j, otherp, board_values)
            break_y, choice_v2 = eval_step(choice_v1, board_val, j, idx2, game)

            if break_y:
                w_tree.children[i].children[j].value = choice_v2
                continue

            idx3 = []
            for k in range(0, 7):  # player plays
                old_board2 = old_board1.copy()
                choice_v3 = 0

                game, new_b3, board_val = assign_weight(old_board2, k, player, board_values)
                break_y, choice_v3 = eval_step(choice_v2, board_val, k, idx3, game, np.array([-1]))

                if break_y:
                    w_tree.children[i].children[j].children[k].value = choice_v3
                    continue
                idx4 = []

                for l in range(0, 7):  # other player plays
                    old_board3 = old_board2.copy()

                    game, _, board_val = assign_weight(old_board3, l, otherp, board_values)
                    break_y, choice_v4 = eval_step(choice_v3, board_val, l, idx4, game)

                    w_tree.children[i].children[j].children[k].children[l].value = choice_v4

                    if break_y:
                        continue

                _, val_4 = min_child(w_tree.children[i].children[j].children[k], idx4)
                w_tree.children[i].children[j].children[k].value = val_4

            _, val_3 = max_child(w_tree.children[i].children[j], idx3)
            w_tree.children[i].children[j].value = val_3
        _, val_2 = min_child(w_tree.children[i], idx2)
        w_tree.children[i].value = val_2
    action, w_tree.value = max_child(w_tree, idx1)

    action = PlayerAction(action)

    if start == 10:
        action = 3

    # return action,w_tree
    return action, saved_state
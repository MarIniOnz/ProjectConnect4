import numpy as np
from typing import Optional
from typing import Callable, Tuple
from agents.common import GameState,BoardPiece, PlayerAction, SavedState, check_end_state, apply_player_action


class Tree:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_node(self,value):
        self.children.append(Tree(value))


def minmax_tree()-> Tree:

    min_tree = Tree(0)

    for i in range(0,7):
        min_tree.add_node(0)
        for j in range(0,7):
            min_tree.children[i].add_node(0)
            for k in range(0, 7):
                min_tree.children[i].children[j].add_node(0)
                for l in range(0,7):
                    min_tree.children[i].children[j].children[k].add_node(0)

    return min_tree


def assign_weight(board,pos_tree,player)-> object:
    new_b = apply_player_action(board,pos_tree,player)
    value = check_end_state(new_b,player)
    if value==-1:
        value=0
    return value,new_b

def max_child(w_tree):
    maxi = -10000
    idx = np.random.randint(7)
    for l in range(0,7):
        new_val = w_tree.children[l].value
        if new_val > maxi:
            maxi = new_val
            idx = l
    return idx,maxi

def min_child(w_tree):
    mini = 10000
    idx = np.random.randint(7)
    for l in range(0,7):
        new_val = w_tree.children[l].value
        if new_val < mini:
            mini = new_val
            idx = l
    return idx,mini


# def minimax_action(board:np.ndarray,player: BoardPiece, saved_state: Optional[SavedState],depth:int=4,) -> Tuple[int,Tree]:

def minimax_action(board: np.ndarray, player: BoardPiece) -> Tuple[int, Tree]:

    # -> Tuple[PlayerAction, Optional[SavedState]]:
    """
        Enter the current state of the board and "best" non-full column
        to perform the next movement, returning it as "action"
    """
    w_tree = minmax_tree() # Weights tree

    if player==BoardPiece(1):
        otherp = BoardPiece(2)
    else:
        otherp = BoardPiece(1)

    for i in range(0,7): # player plays
        choice_v1 = 0
        choice_v2 = 0
        choice_v3 = 0
        choice_v4 = 0

        new_choice,new_b1 = assign_weight(board,i,player)
        if new_choice == GameState.IS_WIN:
            choice_v1 += 1

        for j in range(0,7): # other player plays
            new_choice,new_b2 = assign_weight(new_b1,j,otherp)
            if new_choice == GameState.IS_WIN:
                choice_v2 = choice_v1 - 1

            for k in range(0, 7): #  player plays
                new_choice, new_b3 = assign_weight(new_b2, k, player)
                if new_choice == GameState.IS_WIN:
                    choice_v3 = choice_v2 + 1

                for l in range(0,7): #  other player plays
                    new_choice, new_b4 = assign_weight(new_b3, l, otherp)
                    if new_choice == GameState.IS_WIN:
                        choice_v4 = choice_v3 - 1
                    w_tree.children[i].children[j].children[k].children[l].value = choice_v4

                _,w_tree.children[i].children[j].children[k].value = min_child(w_tree.children[i].children[j].children[k])
            _,w_tree.children[i].children[j].value = max_child(w_tree.children[i].children[j])
        _,w_tree.children[i].value = min_child(w_tree.children[i])
    action,w_tree.value = max_child(w_tree)

    return action,w_tree
    # return action, saved_state







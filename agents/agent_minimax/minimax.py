import numpy as np
from typing import Optional
from typing import Callable, Tuple
from agents.common import BoardPiece, PlayerAction, SavedState

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

def minimax_action(board:np.ndarray,player: BoardPiece, saved_state: Optional[SavedState],depth:int=4,) -> Tuple[PlayerAction, Optional[SavedState]]:
    """
        Enter the current state of the board and "best" non-full column
        to perform the next movement, returning it as "action"
    """

    weights = np.empty((depth**2,depth**2))




    return action, saved_state







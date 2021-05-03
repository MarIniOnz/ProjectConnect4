import numpy as np
from agents.common import findall
from agents.agent_minimax.minimax import minmax_tree

BoardPiece = np.int8
NO_PLAYER = BoardPiece(0)
PLAYER1 = BoardPiece(1)
PLAYER2 = BoardPiece(2)

board = np.ndarray([6, 7]) * NO_PLAYER
board[:] = NO_PLAYER

board[5, 0] = PLAYER2
board[5, 1] = PLAYER1
board[5, 2] = PLAYER2
board[5, 3] = PLAYER1
board[5, 4] = PLAYER1
board[5, 5] = PLAYER1

# print(board)

board_str = ('|==============|\n')
x, y = np.shape(board)

for i in range(0, x):
    string = '|'

    for j in range(0, y):
        if board[i, j] == NO_PLAYER:
            string += '  '
        elif board[i, j] == PLAYER1:
            string += 'X '
        elif board[i, j] == PLAYER2:
            string += '0 '
    board_str += string + '|\n'
board_str += ('|==============|\n|0 1 2 3 4 5 6 |')
# print(board_str)

action = 3
player = BoardPiece(1)
row = sum(board[:, action] == 0) - 1
board[row, action] = player

print(board)

indexes = findall(1, board)
x, y = np.shape(board)

# hor, diag1, diag2, vert
print(indexes)
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

print(sums.shape, sums)

if np.sum(sums>=4)>0:
    ended = 1
else:
    ended= 0

M=minmax_tree()
print(M)
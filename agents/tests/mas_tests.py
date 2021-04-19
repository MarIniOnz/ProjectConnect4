# Sample random board variables
sample_random_board = np.empty((6, 7), dtype=BoardPiece)
sample_random_board.fill(NO_PLAYER)
sample_random_board[0,1] = sample_random_board[1,1] = sample_random_board[0,2] = sample_random_board[2,2] = sample_random_board[1,3] = sample_random_board[1,4] = PLAYER2
sample_random_board[1,2] = sample_random_board[3,2] = sample_random_board[0,3] = sample_random_board[2,3] = sample_random_board[3,3] = sample_random_board[0,4] = sample_random_board[2,4] = PLAYER1
sample_random_pretty_board = '''|==============|
|              |
|              |
|    X X       |
|    O X X     |
|  O X O O     |
|  O O X X     |
|==============|
|0 1 2 3 4 5 6 |'''

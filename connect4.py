import numpy as np
from termcolor import colored

board_rows = 6
board_cols = 7

def create_board()-> np:
    board = np.zeros((board_rows,  board_cols), dtype=int)
    return board

def get_player_selection(board: np, player: int)-> int:
    selection_not_made = True
    while selection_not_made:
        selection = input("Player {} Make your Selection (1-7): ".format(player))
        if selection.isdigit():
            selection = int(selection)-1
            if 0 <= selection <= 6:
                if column_is_free(board, selection):
                    selection_not_made = False
                else:
                    print(colored("Select another column", "red"))
            else:
                print(colored("Select a number between 1-7", "red"))
        else:
            print(colored("Please chose an integer between 1-7", "red"))
    return int(selection)

def column_is_free(board: np, col: int)-> bool:
    return board[board_rows-1][col] == 0

def drop_piece(board: np, row: int, col: int, piece: int):
    board[row][col] = piece

def get_next_open_row(board: np, col: int):
    for r in range(board_rows):
        if board[r][col] == 0:
            return r

def print_board(board: np):
    print(np.flip(board, 0))

def winning_move(board: np, piece: int)-> bool:
    for c in range(board_cols-3):
        for r in range(board_rows):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
            
    for c in range(board_cols):
        for r in range(board_rows-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True    
             
    for c in range(board_cols-3):
        for r in range(board_rows-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True  
            
    for c in range(board_cols-3):
        for r in range(3, board_rows):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True  
    return False
            
#-------------------------------------------------------------------
board = create_board()
print(board)

game_over = False
turn = 0
# Start game
while not game_over:
    if turn == 0:
        player1_col = get_player_selection(board, turn+1)
        player1_row = get_next_open_row(board, player1_col)
        drop_piece(board, player1_row, player1_col, turn+1)
    else:
        player2_col = get_player_selection(board, turn+1)
        player2_row = get_next_open_row(board, player2_col)
        drop_piece(board, player2_row, player2_col, turn+1)

    print(turn)
    print(board)
    print_board(board)

    if winning_move(board, turn+1):
        print("Player {} Wins!".format(turn+1))
        game_over = True

    turn += 1
    turn = turn % 2
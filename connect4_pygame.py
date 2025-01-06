import numpy as np
import pygame
import sys
import math
import random
from termcolor import colored

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
board_rows = 6
board_cols = 7

EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2
AI = 2
WINDOW_LENGTH=4

def create_board()-> np:
    board = np.zeros((board_rows,  board_cols), dtype=int)
    return board

def get_selection(board: np, ai: bool, player: int, diffictulty: int)->int:
    if ai:
        minimax(board, 6, False)
    else:
        get_player_selection(board, player)
    return -1

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

def get_next_open_row(board: np, col: int)->int:
    for r in range(board_rows):
        if board[r][col] == 0:
            return r
    return -1

def print_board(board: np):
    print(np.flip(board, 0))

def draw_board(board):
    for c in range(board_cols):
        for r in range(board_rows):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE)) 
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)    
            else:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)    

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def game_won(board: np, piece: int)-> bool:
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

def game_tied(board: np)-> bool:
    if 0 in board:
        return False
    else:
        return True       

def game_over(board: np)-> bool:
    return game_tied(board) or \
    game_won(board, 1) or \
    game_won(board, 2)

def minimax(board: np, depth: int, alpha: int, beta: int, maximizingPlayer: bool):
    valid_locations = get_valid_locations(board)
    if depth == 0 or game_over(board):
        if game_won(board, AI):
            return (None, 10000)
        elif game_won(board, PLAYER_1):
            return (None, -10000)
        elif game_tied(board):
            return (None, 0)
        else:
            return (None, score_position(board, AI))
        
    if maximizingPlayer:
        value = -math.inf
        column = 2
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_1)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def evaluate_window(window: list, player: int)->int:
    score = 0
    opp_piece = PLAYER_1
    if window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, player: int)->int:
    score=0

    # Score center
    center_array = [int(i) for i in list(board[:, board_cols//2])]
    center_count = center_array.count(player)
    score += center_count*3
    # Score horizontal
    for r in range(board_rows):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(board_cols-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, player)
    
    # Score verticle
    for c in range(board_cols):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(board_rows-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, player)

    # Score positive sloped diagonal
    for r in range(board_rows-3):
        for c in range(board_cols-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, player)
    
    # Score negative sloped diagonal
    for r in range(board_rows-3):
        for c in range(board_cols-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, player)

    return score

def get_valid_locations(board)->list:
    valid_locations = []
    for col in range(board_cols):
        if column_is_free(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board: np, player: int)->int:
    best_score=0
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, player)
        score = score_position(temp_board, player)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

#-------------------------------------------------------------------
pygame.init()
SQUARESIZE=100
RADIUS=int(SQUARESIZE/2 - 5)
width = board_cols * SQUARESIZE
height = (board_rows+1) * SQUARESIZE

size = (width, height)
screen = pygame.display.set_mode(size)
bg = pygame.image.load("Pictures/Pygame/GradientBlue.jpg") # Not used
myfont = pygame.font.SysFont("monospace", 75)

def play(player2_is_ai: bool):
    board = create_board()
    draw_board(np.flip(board, 0))
    pygame.display.update()
    game_over = False
    turn = 0
    # Start game
    while not game_over:
        pygame.display.update()
        player_made_move = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                player_col = int(math.floor(posx/SQUARESIZE))
                if column_is_free(board, player_col):   
                    if turn == 0: 
                        player_row = get_next_open_row(board, player_col)
                        drop_piece(board, player_row, player_col, turn+1)
                        player_made_move = True
                    else:
                        if not player2_is_ai: 
                            player_row = get_next_open_row(board, player_col)
                            drop_piece(board, player_row, player_col, turn+1)
                            player_made_move = True

        if turn==1 and player2_is_ai:
            #player_col = pick_best_move(board, turn+1)
            if len(get_valid_locations(board)) <= 7:
                player_col, minimax_score = minimax(board, 6, -math.inf, math.inf, True)
            elif len(get_valid_locations(board)) <= 5:
                player_col, minimax_score = minimax(board, 7, -math.inf, math.inf, True)
            elif len(get_valid_locations(board)) <= 4:
                player_col, minimax_score = minimax(board, 8, -math.inf, math.inf, True)
            elif len(get_valid_locations(board)) <= 3:
                player_col, minimax_score = minimax(board, 10, -math.inf, math.inf, True)
            player_row = get_next_open_row(board, player_col)
            drop_piece(board, player_row, player_col, turn+1)
            player_made_move = True
        
        if player_made_move:
            draw_board(np.flip(board, 0))
            print_board(board)

            if game_won(board, turn+1):
                print("Player {} Wins!".format(turn+1))
                label = myfont.render("Player {} wins!".format(turn+1), 1, GREEN)
                screen.blit(label, (40,10))
                game_over = True
                pygame.display.update()
            
            if game_tied(board):
                print("Tie")
                label = myfont.render("Tie", 1, GREEN)
                screen.blit(label, (450,10))
                game_over = True
                pygame.display.update()

            turn += 1
            turn = turn % 2
        
        if game_over:
            pygame.time.wait(3000)

def home():
    running = True
    while running:
        screen.fill("black")
        pygame.display.set_caption("Menu")
        #screen.blit(bg, (0, 0))  

        draw_text("Play", myfont, GREEN, 160, 350)
        draw_text("Quit", myfont, GREEN, 160, 450)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                posy = event.pos[1]
                print(posx)
                print(posy)
                if 0<(posx - 160) < 180 and 0<(posy - 350) < 80:
                    play(True)
                if 0<(posx - 160) < 180 and 0<(posy - 450) < 80:
                    pygame.quit()
                    sys.exit()
                    running=False

def main():
    home()

if __name__ == "__main__":
    main()
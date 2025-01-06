# Example file showing a basic pygame "game loop"
import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255 )
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.draw.circle(screen, "red", player_pos, 40)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()


'''
board = np.array([
        [0, 2, 2, 1, 1, 1, 0],
        [0, 0, 0, 2, 1, 2, 0],
        [0, 0, 0, 0, 2, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]])
board = np.flip(board, 1)
'''

'''
def evaluate_window(window: list, player: int)->int:
    score = 0
    opp_piece = PLAYER_1
    if window.count(player) == 4:
        score += 200
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 25
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += 10

    if window.count(opp_piece) == 3 and window.count(player) == 1:
        score += 100

    return score

def score_position(board, player: int)->int:
    score=0
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
'''
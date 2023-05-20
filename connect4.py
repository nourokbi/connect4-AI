import random
import sys
import math
import pygame
import numpy as np

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


############################################################################# MINIMAX ALgorithm

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_score_only_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)

    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def pick_alpha_beta_pruning_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -math.inf  ##############  with alpha-beta pruning
    # best_score = -10000
    best_col = random.choice(valid_locations)

    alpha = -math.inf  ##############  with alpha-beta pruning
    beta = math.inf  ##############  with alpha-beta pruning

    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = minimax(temp_board, 2, alpha, beta, False)[1]  ##############  with alpha-beta pruning
        # score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def pick_best_move_with_randomness(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_moves = []  ##############  with_randomness

    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)

        if score > best_score:
            best_score = score
            best_moves = [col]  ##############  with_randomness
        elif score == best_score:  ##############  with_randomness
            best_moves.append(col)  ##############  with_randomness

    return random.choice(best_moves)  ##############  with_randomness


#########################################################################################

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.set_caption("Connect 4")
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)
start_font = pygame.font.SysFont("monospace", 50)
difficulty_font = pygame.font.SysFont("monospace", 30)


def draw_start_screen():
    screen.fill(BLACK)
    start_label = start_font.render("Click to Start", bool(1), YELLOW)
    screen.blit(start_label, (width / 2 - start_label.get_width() / 2, height / 2 - start_label.get_height() / 2))
    pygame.display.update()


def draw_difficulty_screen():
    screen.fill(BLACK)
    easy_label = difficulty_font.render("Easy", 1, YELLOW)
    medium_label = difficulty_font.render("Medium", 1, YELLOW)
    hard_label = difficulty_font.render("Hard", 1, YELLOW)
    very_hard_label = difficulty_font.render("very hard", 1, YELLOW)
    screen.blit(easy_label, (width / 2 - easy_label.get_width() / 2, height / 2 - 50))
    screen.blit(medium_label, (width / 2 - medium_label.get_width() / 2, height / 2))
    screen.blit(hard_label, (width / 2 - hard_label.get_width() / 2, height / 2 + 50))
    screen.blit(very_hard_label, (width / 2 - very_hard_label.get_width() / 2, height / 2 + 100))
    pygame.display.update()


# draw_start_screen()
draw_difficulty_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            turn = random.randint(PLAYER, AI)
            game_over = False
            if game_over:
                turn = random.randint(PLAYER, AI)
                game_over = False
            else:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if width / 2 - 50 <= mouse_x <= width / 2 + 50 and height / 2 - 50 <= mouse_y <= height / 2 - 10:
                    difficulty = "Easy"
                    print(difficulty)
                elif width / 2 - 60 <= mouse_x <= width / 2 + 60 and height / 2 + 10 <= mouse_y <= height / 2 + 40:
                    difficulty = "Medium"
                    print(difficulty)
                elif width / 2 - 40 <= mouse_x <= width / 2 + 40 and height / 2 + 40 <= mouse_y <= height / 2 + 100:
                    difficulty = "Hard"
                    print(difficulty)
                elif width / 2 - 80 <= mouse_x <= width / 2 + 80 and height / 2 + 100 <= mouse_y <= height / 2 + 150:
                    difficulty = "very hard"
                    print(difficulty)
                else:
                    difficulty = "minimax score with randomness"
                    print(difficulty)

            while not game_over:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    # if event.type == pygame.MOUSEMOTION:
                    #     pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    #     posx = event.pos[0]
                    #     if turn == PLAYER:
                    #         pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

                    pygame.display.update()

                    # if event.type == pygame.MOUSEBUTTONDOWN:
                    #     pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                        # print(event.pos)
                        # Ask for Player 1 Input
                    if turn == PLAYER:
                        # posx = event.pos[0]
                        # col = int(math.floor(posx / SQUARESIZE))
                        col = pick_score_only_move(board, AI_PIECE)

                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, PLAYER_PIECE)

                            if winning_move(board, PLAYER_PIECE):
                                label = myfont.render("Player 1 wins!!", 1, RED)
                                screen.blit(label, (40, 10))
                                game_over = True

                            turn += 1
                            turn = turn % 2

                            print_board(board)
                            draw_board(board)

                # # Ask for Player 2 Input
                if turn == AI and not game_over:

                    '''game difficulties'''

                    if difficulty == 'Easy':
                        # Easy - AI chooses randomly
                        col = random.randint(0, COLUMN_COUNT - 1)
                    elif difficulty == 'Medium':
                        # Medium - AI chooses according to score only
                        col = pick_score_only_move(board, AI_PIECE)
                    elif difficulty == 'Hard':
                        # Hard - AI chooses according to minimax 3 score with alpha beta pruning
                        col = pick_alpha_beta_pruning_move(board, AI_PIECE)
                    elif difficulty == 'very hard':
                        # Hard - AI chooses according to minimax 4 score
                        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
                    else:
                        # Hard - AI chooses according to minimax 4 score with randomness
                        col = pick_best_move_with_randomness(board, AI_PIECE)

                    if is_valid_location(board, col):
                        # pygame.time.wait(500)
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, AI_PIECE)

                        if winning_move(board, AI_PIECE):
                            label = myfont.render("AI wins!!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True

                        print_board(board)
                        draw_board(board)

                        turn += 1
                        turn = turn % 2
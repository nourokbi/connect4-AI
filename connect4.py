
# import numpy as np
# import random
# import pygame
# import sys
# import math

# BLUE = (0,0,255)
# BLACK = (0,0,0)
# RED = (255,0,0)
# YELLOW = (255,255,0)

# ROW_COUNT = 6
# COLUMN_COUNT = 7

# PLAYER = 0
# AI = 1

# EMPTY = 0
# PLAYER_PIECE = 1
# AI_PIECE = 2
# WINDOW_LENGTH = 4

# def create_board():
# 	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
# 	return board

# def drop_piece(board, row, col, piece):
# 	board[row][col] = piece

# def is_valid_location(board, col):
# 	return board[ROW_COUNT-1][col] == 0

# def get_next_open_row(board, col):
# 	for r in range(ROW_COUNT):
# 		if board[r][col] == 0:
# 			return r

# def print_board(board):
# 	print(np.flip(board, 0))

# def winning_move(board, piece):
# 	# Check horizontal locations for win
# 	for c in range(COLUMN_COUNT-3):
# 		for r in range(ROW_COUNT):
# 			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
# 				return True

# 	# Check vertical locations for win
# 	for c in range(COLUMN_COUNT):
# 		for r in range(ROW_COUNT-3):
# 			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
# 				return True

# 	# Check positively sloped diaganols
# 	for c in range(COLUMN_COUNT-3):
# 		for r in range(ROW_COUNT-3):
# 			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
# 				return True

# 	# Check negatively sloped diaganols
# 	for c in range(COLUMN_COUNT-3):
# 		for r in range(3, ROW_COUNT):
# 			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
# 				return True

# def evaluate_window(window, piece):
# 	score = 0
# 	opp_piece = PLAYER_PIECE
# 	if piece == PLAYER_PIECE:
# 		opp_piece = AI_PIECE

# 	if window.count(piece) == 4:
# 		score += 100
# 	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
# 		score += 5
# 	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
# 		score += 2

# 	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
# 		score -= 4

# 	return score

# def minimax_algorithm(board, piece):
# 	score = 0

# 	## Score center column
# 	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
# 	center_count = center_array.count(piece)
# 	score += center_count * 3

# 	## Score Horizontal
# 	for r in range(ROW_COUNT):
# 		row_array = [int(i) for i in list(board[r,:])]
# 		for c in range(COLUMN_COUNT-3):
# 			window = row_array[c:c+WINDOW_LENGTH]
# 			score += evaluate_window(window, piece)

# 	## Score Vertical
# 	for c in range(COLUMN_COUNT):
# 		col_array = [int(i) for i in list(board[:,c])]
# 		for r in range(ROW_COUNT-3):
# 			window = col_array[r:r+WINDOW_LENGTH]
# 			score += evaluate_window(window, piece)

# 	## Score posiive sloped diagonal
# 	for r in range(ROW_COUNT-3):
# 		for c in range(COLUMN_COUNT-3):
# 			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
# 			score += evaluate_window(window, piece)

# 	for r in range(ROW_COUNT-3):
# 		for c in range(COLUMN_COUNT-3):
# 			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
# 			score += evaluate_window(window, piece)

# 	return score
# ############################################################################# MINIMAX ALgorithm

# def is_terminal_node(board):
# 	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# def minimax(board, depth, alpha, beta, maximizingPlayer):
# 	valid_locations = get_valid_locations(board)
# 	is_terminal = is_terminal_node(board)
# 	if depth == 0 or is_terminal:
# 		if is_terminal:
# 			if winning_move(board, AI_PIECE):
# 				return (None, 100000000000000)
# 			elif winning_move(board, PLAYER_PIECE):
# 				return (None, -10000000000000)
# 			else: # Game is over, no more valid moves
# 				return (None, 0)
# 		else: # Depth is zero
# 			return (None, minimax_algorithm(board, AI_PIECE))
# 	if maximizingPlayer:
# 		value = -math.inf
# 		column = random.choice(valid_locations)
# 		for col in valid_locations:
# 			row = get_next_open_row(board, col)
# 			b_copy = board.copy()
# 			drop_piece(b_copy, row, col, AI_PIECE)
# 			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
# 			if new_score > value:
# 				value = new_score
# 				column = col
# 			alpha = max(alpha, value)
# 			if alpha >= beta:
# 				break
# 		return column, value

# 	else: # Minimizing player
# 		value = math.inf
# 		column = random.choice(valid_locations)
# 		for col in valid_locations:
# 			row = get_next_open_row(board, col)
# 			b_copy = board.copy()
# 			drop_piece(b_copy, row, col, PLAYER_PIECE)
# 			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
# 			if new_score < value:
# 				value = new_score
# 				column = col
# 			beta = min(beta, value)
# 			if alpha >= beta:
# 				break
# 		return column, value

# def get_valid_locations(board):
# 	valid_locations = []
# 	for col in range(COLUMN_COUNT):
# 		if is_valid_location(board, col):
# 			valid_locations.append(col)
# 	return valid_locations

# def pick_best_move(board, piece):

# 	valid_locations = get_valid_locations(board)
# 	best_score = -10000
# 	best_col = random.choice(valid_locations)
# 	for col in valid_locations:
# 		row = get_next_open_row(board, col)
# 		temp_board = board.copy()
# 		drop_piece(temp_board, row, col, piece)
# 		score = minimax_algorithm(temp_board, piece)
# 		if score > best_score:
# 			best_score = score
# 			best_col = col

# 	return best_col
# #########################################################################################

# def draw_board(board):
# 	for c in range(COLUMN_COUNT):
# 		for r in range(ROW_COUNT):
# 			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
# 			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
# 	for c in range(COLUMN_COUNT):
# 		for r in range(ROW_COUNT):		
# 			if board[r][c] == PLAYER_PIECE:
# 				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
# 			elif board[r][c] == AI_PIECE: 
# 				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
# 	pygame.display.update()

# board = create_board()
# print_board(board)
# game_over = False

# pygame.init()

# SQUARESIZE = 100

# width = COLUMN_COUNT * SQUARESIZE
# height = (ROW_COUNT+1) * SQUARESIZE

# size = (width, height)

# RADIUS = int(SQUARESIZE/2 - 5)

# screen = pygame.display.set_mode(size)
# draw_board(board)
# pygame.display.update()

# myfont = pygame.font.SysFont("monospace", 75)

# turn = random.randint(PLAYER, AI)

# while not game_over:

# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			sys.exit()

# 		if event.type == pygame.MOUSEMOTION:
# 			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
# 			posx = event.pos[0]
# 			if turn == PLAYER:
# 				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

# 		pygame.display.update()

# 		if event.type == pygame.MOUSEBUTTONDOWN:
# 			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
# 			#print(event.pos)
# 			# Ask for Player 1 Input
# 			if turn == PLAYER:
# 				posx = event.pos[0]
# 				col = int(math.floor(posx/SQUARESIZE))

# 				if is_valid_location(board, col):
# 					row = get_next_open_row(board, col)
# 					drop_piece(board, row, col, PLAYER_PIECE)

# 					if winning_move(board, PLAYER_PIECE):
# 						label = myfont.render("Player 1 wins!!", 1, RED)
# 						screen.blit(label, (40,10))
# 						game_over = True

# 					turn += 1
# 					turn = turn % 2

# 					print_board(board)
# 					draw_board(board)


# 	# # Ask for Player 2 Input
# 	if turn == AI and not game_over:				

# 		#col = random.randint(0, COLUMN_COUNT-1)
# 		#col = pick_best_move(board, AI_PIECE)
# 		col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

# 		if is_valid_location(board, col):
# 			#pygame.time.wait(500)
# 			row = get_next_open_row(board, col)
# 			drop_piece(board, row, col, AI_PIECE)

# 			if winning_move(board, AI_PIECE):
# 				label = myfont.render("Player 2 wins!!", 1, YELLOW)
# 				screen.blit(label, (40,10))
# 				game_over = True

# 			print_board(board)
# 			draw_board(board)

# 			turn += 1
# 			turn = turn % 2

# 	if game_over:
# 		pygame.time.wait(3000)

import numpy as np
import pygame
import sys
import math
import random

# Board and game settings
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 100

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Players and pieces
PLAYER = 0
AGENT = 1
PLAYER_PIECE = 1
AI_PIECE = 2

# Initialize the game
pygame.init()
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_SIZE / 2 - 5)
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 75)


def create_board():
    # Create an empty game board
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    # Place the piece on the board at the specified position
    board[row][col] = piece


def is_valid_location(board, col):
    # Check if a column is not full
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    # Get the next available row for placing a piece in the column
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    # Print the current board state
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check if the specified piece has won the game
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True

    return False


def evaluate_window(window, piece):
    # Evaluate the score of a window of 4 consecutive pieces
    score = 0

    # Player's piece in the window
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    # AI's piece in the window
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score


def evaluate_board(board, piece):
    # Evaluate the score of the board for the specified piece
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c : c + 4]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r : r + 4]
            score += evaluate_window(window, piece)

    # Score positively sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negatively sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    # Check if the game has reached a terminal state
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def get_valid_locations(board):
    # Get the valid column indices where a piece can be placed
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def get_opponent_piece(piece):
    # Get the opponent's piece
    return PLAYER_PIECE if piece == AI_PIECE else AI_PIECE


def minimax(board, depth, alpha, beta, maximizing_player, piece):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return float("inf")
            elif winning_move(board, PLAYER_PIECE):
                return float("-inf")
            else:
                return 0
        else:
            return evaluate_board(board, AI_PIECE)

    if maximizing_player:
        max_eval = float("-inf")
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, piece)
            eval_score = minimax(temp_board, depth - 1, alpha, beta, False, get_opponent_piece(piece))
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float("inf")
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, piece)
            eval_score = minimax(temp_board, depth - 1, alpha, beta, True, get_opponent_piece(piece))
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval


def get_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = float("-inf")
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = minimax(temp_board, 4, float("-inf"), float("inf"), False, get_opponent_piece(piece))
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


def draw_board(board):
    # Draw the game board
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(
                screen,
                BLACK,
                (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),
                RADIUS,
            )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(
                    screen,
                    RED,
                    (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                    RADIUS,
                )
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                    RADIUS,
                )
    pygame.display.update()


board = create_board()
game_over = False
turn = PLAYER

pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if turn == PLAYER:
            # Player's turn
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                # Player's move
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Player wins!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn += 1
                    turn %= 2

                    print_board(board)
                    draw_board(board)

        if turn == AGENT and not game_over:
            # Agent's turn
            col = get_best_move(board, AI_PIECE)

            if is_valid_location(board, col):
                pygame.time.wait(500)

                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Agent wins!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn %= 2

        if game_over:
            pygame.time.wait(3000)

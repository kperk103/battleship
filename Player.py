from Gameboard import Gameboard
from Minimax import Minimax
import pygame
import numpy as np
import sys
import random
import time
import random

#init pygame and constants
pygame.init()
SIZE = 7  #7 rows, 6 cols
WIDTH, HEIGHT = 100 * SIZE, 100 * SIZE #must be multiples of SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
PADDING = 1 * SIZE
BORDER = 1
CELL_WIDTH = (WIDTH - PADDING * 2) / SIZE
CELL_HEIGHT = (HEIGHT - PADDING * 2) / SIZE
OFFSET = CELL_WIDTH / 2
BLANK_BOARD = np.zeros((6, 7), dtype=int)
BLACK, RED, YELLOW, BLUE, BLUEGREY, SKYBLUE = (0, 0, 0), (255, 0, 0), (255, 255, 0), (154, 209, 230), (188, 211, 235), (129, 193, 222)
SKYBLUE, GREY, PINK = (129, 193, 222), (151, 222, 255), (235, 80, 151)
BACKGROUND, HIGHLIGHTED = SKYBLUE, PINK
pygame.display.set_caption("Connect Four")

TIME_DELAY_AFTER_GAME = 0.05 #this lets us see the winning strikethrough line easier
GAMES = 100
DEPTH_PLAYER_ONE = 3
DEPTH_PLAYER_TWO = 'Random' #change to an int if you dont want 'random' word on the display

RANDOMDEPTHS = False #Set true if you want to randomize the depths of the agents, each game
LOWERBOUND = 1 #lower bound for the depth randomization
UPPERBOUND = 4 #upper bound for the depth randomization

#update these accordingly. IF YOU WANT TO PLAY AGAINST THE AI,
#MAKE SURE TO UPDATE bothAI to FALSE. 
PLAYER1 = Minimax(DEPTH_PLAYER_ONE, alphaBeta=True)
PLAYER2 = Minimax(DEPTH_PLAYER_TWO,alphaBeta=True)
BOTHAI = True
#set this to True if you want p2 to be random choice
USERANDOM = True

NEXTNOALPHABETA = [False, 0] #keep this false, we change to true if we detect a click (next game should be w/o pruning)
NOALPHABETAGAMESCOUNT = 2

#draws the gameboard in pygame. If col value is None, we just draw the entire board
#if col value is an int, we only draw the piece that was most recently 
#dropped on that column. (This saves computation time for drawing)
#returns None if no col was specified, returns the rectangle where we drew on
#if a column was specified.
def draw_board(arr, col=None):
    if col == None: 
        SCREEN.fill(BACKGROUND) 
        for row in range(len(arr)):
            for col in range(len(arr[0])):
                #drawing the grid
                pygame.draw.rect(SCREEN, BLUE, (col * CELL_HEIGHT + PADDING, row * CELL_WIDTH + PADDING + OFFSET, CELL_WIDTH + BORDER, CELL_HEIGHT + BORDER))
                pygame.draw.rect(SCREEN, BLACK, (col * CELL_HEIGHT + PADDING, row * CELL_WIDTH + PADDING + OFFSET, CELL_WIDTH + BORDER, CELL_HEIGHT + BORDER), BORDER)
                #draw circle for that color
                if arr[row][col] == 1:
                    pygame.draw.circle(SCREEN, RED, (col * CELL_HEIGHT + PADDING + OFFSET, row * CELL_WIDTH + PADDING + CELL_WIDTH), OFFSET - BORDER)
                    
                if arr[row][col] == 2:
                    pygame.draw.circle(SCREEN, YELLOW, (col * CELL_HEIGHT + PADDING + OFFSET, row * CELL_WIDTH + PADDING + CELL_WIDTH), OFFSET - BORDER)
    else:   
        row = 5

        while arr[row][col] != 0:
            row -= 1
            if row == -1: 
                break
        
        row += 1
        if row == 6:
            #nothing to draw, we are trying to draw an invalid column
            #this should never return
            return 
        
        #draw circle for that color
        if arr[row][col] == 1:
            pygame.draw.circle(SCREEN, RED, (col * CELL_HEIGHT + PADDING + OFFSET, row * CELL_WIDTH + PADDING + CELL_WIDTH), OFFSET - BORDER)

            
        if arr[row][col] == 2:
            pygame.draw.circle(SCREEN, YELLOW, (col * CELL_HEIGHT + PADDING + OFFSET, row * CELL_WIDTH + PADDING + CELL_WIDTH), OFFSET - BORDER)

        return (col * CELL_HEIGHT + PADDING, row * CELL_WIDTH + PADDING + OFFSET, CELL_WIDTH + BORDER, CELL_HEIGHT + BORDER)

def highlight_column(col): 
    if col < 0 or col > 6: return
    line_width = 3

    left_line_start = (col * CELL_WIDTH + PADDING, PADDING + OFFSET)
    left_line_end = (col * CELL_WIDTH + PADDING, HEIGHT - PADDING - OFFSET)
    right_line_start = ((col + 1) * CELL_WIDTH + PADDING, PADDING + OFFSET)
    right_line_end = ((col + 1) * CELL_WIDTH + PADDING, HEIGHT - PADDING - OFFSET)

    pygame.draw.line(SCREEN, HIGHLIGHTED, left_line_start, left_line_end, line_width)
    pygame.draw.line(SCREEN, HIGHLIGHTED, right_line_start, right_line_end, line_width)

def has_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            if BOTHAI: #only do this if both players are ai
                NEXTNOALPHABETA[0] = True
    return False

def has_clicked(): 
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            return True
    return False

def humanChoice(game, clock):
    clock.tick(60)
    #print(f"Player {player} ({'X' if player == 1 else '0'}), Select a column (1-7): ")
    #loop for get col
    picked_col = False
    last_col_hovered = -1
    mouse_exited = True
    while not picked_col:
        #quit on exit
        if has_quit(): 
            pygame.quit()
            sys.exit()

        #pick column
        mouse_windowed = pygame.mouse.get_focused() #if mouse is inside window
        if not mouse_windowed:
            if not mouse_exited: 
                draw_board(game.board)
                pygame.display.flip()
                mouse_exited = True
            continue
        mouse_exited = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x == 0: mouse_x = 1 #prevent divide by zero
        #text = font.render(f"Mouse position: ({mouse_x}, {mouse_y})", True, BLACK)
        #SCREEN.blit(text, (text_x, text_y))
        #pygame.display.flip()
        #SCREEN.fill(BACKGROUND, (text_x, text_y, text_width, text_height))

        #highlight column we are about to select
        col_hovered = int((mouse_x - PADDING) / (CELL_WIDTH))

        #account for left, right, top, and bottom of grid
        if mouse_x < PADDING or mouse_x > WIDTH - PADDING or mouse_y < PADDING + OFFSET or mouse_y > HEIGHT - PADDING - OFFSET: 
            col_hovered = -1 #account for edge of window

        #if cols are dif, refill grid. If they arent, highlight that col
        if col_hovered != last_col_hovered:
            last_col_hovered = col_hovered 
            draw_board(game.board)
        else: 
            highlight_column(col_hovered)

        pygame.display.flip()

        #if we've clicked a column, select it and move on
        if has_clicked(): 
            col = col_hovered + 1
            picked_col = True
            return col

def play_game(player_one_score, player_two_score, ties, player1, player2): 
    #pygame things
    clock = pygame.time.Clock()
    SCREEN.fill(BACKGROUND) 
    draw_board(BLANK_BOARD)
    font = pygame.font.Font(None, 30)
    font_size = 20
    text_x, text_y = WIDTH / 2 - 13.65 * font_size, HEIGHT - HEIGHT / 17

    #blit the scores, and update the display
    SCREEN.blit(font.render(f"Player One: {player_one_score}, Player Two: {player_two_score}, Ties: {ties} ||||| D1: {player1.depth}, D2: {player2.depth}", True, BLACK), (text_x, text_y))
    pygame.display.flip()


    game = Gameboard()


    turn_number = -1 # Turns start on turn # 0.

    #print("Welcome to Connect 4!")

    #Game continues as long as nobody wins... 
    #is there a case when all discs are used and nobody wins?
    while not game.checkWin()[0]:
        #pygame quit
        if has_quit(): break
        turn_number += 1
        invalid_input = True

        while invalid_input:
            #game.toString()
            player = (turn_number % 2) + 1 

           
            if player == 1:
                #if you want to let the human pick a column, just use col = humanChoice(game, clock)
                col = player1.minimax(game.board, 1) + 1

            else:
                #if you want a minimaxer, just use 
                # col = mini.minimax(game.board, 2) + 1
                # 2 for player 2 in param, 1 for player 1
                if not USERANDOM:
                    col = player2.minimax(game.board, 2) + 1
                else: #randomize col
                    validDrop = player2.getValid(game.board)
                    valids = [index for index, value in enumerate(validDrop) if value == 1]

                    mean = 7/2 #middle of columns
                    std_dev = 1 #std dev arbitrary
                    col = int(np.random.normal(mean, std_dev))

                    while col < 0 or col > 6 or validDrop[col] != 1: 
                        col = int(np.random.normal(mean, std_dev))
                    
                    col = col + 1

                    


            #print("\n\n\n---------------------------------------------------")
            
            try:
                col = int(col)
                if col < 1 or col > 7 or not game.addDisc(player, col):
                    print("Invalid Input")
                else:
                    invalid_input = False
            except ValueError:
                print("Invalid Input")
            
            #draw board and update display, if we are playing with 
            #two AIs, we can update only the column we drop on.
            if BOTHAI: 
                rect = draw_board(game.board, col - 1)
                pygame.display.update(rect)
            else: 
                draw_board(game.board)
                pygame.display.flip()

    #print(f"Player {game.checkWin()[0]} wins!")
    #game.toString()

    #display results, close pygame once player closes the game, if we are on last GAME
    #draw line through winning players pieces
    winning_player, location, direction = game.checkWin()
    row = 0
    col = 0
    if winning_player == -1: 
        ties += 1
    else:
        (row, col) = location

    if winning_player == 1: player_one_score += 1
    if winning_player == 2: player_two_score += 1

    if winning_player != -1: #draw the line if there is no tie
        #draw line through winning pieces
        if direction == 0: 
            start_pos = (PADDING + OFFSET + col * CELL_WIDTH, PADDING + OFFSET + row * CELL_WIDTH)
            end_pos = (PADDING + OFFSET + col * CELL_WIDTH, PADDING + OFFSET + row * CELL_WIDTH + 4 * CELL_WIDTH)
        if direction == 1: 
            start_pos = (PADDING + col * CELL_WIDTH, PADDING + CELL_WIDTH + row * CELL_WIDTH)
            end_pos = (PADDING + col * CELL_WIDTH + 4 * CELL_WIDTH, PADDING + CELL_WIDTH + row * CELL_WIDTH)
        if direction == 2: 
            start_pos = (PADDING + col * CELL_WIDTH, PADDING + OFFSET + row * CELL_WIDTH)
            end_pos = (PADDING + col * CELL_WIDTH + 4 * CELL_WIDTH, PADDING + CELL_WIDTH + row * CELL_WIDTH + 3.5 * CELL_WIDTH)
        if direction == 3:
            start_pos = (PADDING + col * CELL_WIDTH, PADDING + CELL_WIDTH + OFFSET + row * CELL_WIDTH)
            end_pos = (PADDING + col * CELL_WIDTH + 4 * CELL_WIDTH, PADDING + CELL_WIDTH + row * CELL_WIDTH - 3.5 * CELL_WIDTH)

        pygame.draw.line(SCREEN, BLACK, start_pos, end_pos, 5)


    pygame.display.flip()
    time.sleep(TIME_DELAY_AFTER_GAME)
    
    if game_count == GAMES - 1: 
        #we are on the last game

        SCREEN.fill(BACKGROUND)
        draw_board(game.board)

        if winning_player != -1: #draw the line if there is no tie

            #draw line through winning pieces
            #should make this into a function later.
            if direction == 0: 
                start_pos = (PADDING + OFFSET + col * CELL_WIDTH, PADDING + OFFSET + row * CELL_WIDTH)
                end_pos = (PADDING + OFFSET + col * CELL_WIDTH, PADDING + OFFSET + row * CELL_WIDTH + 4 * CELL_WIDTH)
            if direction == 1: 
                start_pos = (PADDING + col * CELL_WIDTH, PADDING + CELL_WIDTH + row * CELL_WIDTH)
                end_pos = (PADDING + col * CELL_WIDTH + 4 * CELL_WIDTH, PADDING + CELL_WIDTH + row * CELL_WIDTH)
            if direction == 2: 
                start_pos = (PADDING + col * CELL_WIDTH, PADDING + OFFSET + row * CELL_WIDTH)
                end_pos = (PADDING + col * CELL_WIDTH + 4 * CELL_WIDTH, PADDING + CELL_WIDTH + row * CELL_WIDTH + 3.5 * CELL_WIDTH)
            if direction == 3:
                start_pos = (PADDING + col * CELL_WIDTH, PADDING + CELL_WIDTH + OFFSET + row * CELL_WIDTH)
                end_pos = (PADDING + col * CELL_WIDTH + 4 * CELL_WIDTH, PADDING + CELL_WIDTH + row * CELL_WIDTH - 3.5 * CELL_WIDTH)

        pygame.draw.line(SCREEN, BLACK, start_pos, end_pos, 5)

        SCREEN.blit(font.render(f"Player One: {player_one_score}, Player Two: {player_two_score}, Ties: {ties}", True, BLACK), (text_x, text_y))
        pygame.display.flip()


        while not has_quit():
            clock.tick(60)

    return (player_one_score, player_two_score, ties) #return new scores
            


if __name__ == "__main__":
    SCREEN.fill(BACKGROUND)

    game_count = 0
    player_one_score = player_two_score = ties = 0
    while game_count < GAMES: 
        if RANDOMDEPTHS:
            PLAYER1.depth = random.randint(LOWERBOUND, UPPERBOUND)
            PLAYER2.depth = random.randint(LOWERBOUND, UPPERBOUND)
        if NEXTNOALPHABETA[0]: 
            PLAYER1.alphaBeta = False
            NEXTNOALPHABETA[1] += 1
        #initialize with 0 for each player score and 0 ties
        player_one_score, player_two_score, ties = play_game(player_one_score, player_two_score, ties, PLAYER1, PLAYER2) 
        game_count += 1

        #reset to true alphabeta if we've reached enough games
        if NEXTNOALPHABETA[0] and NEXTNOALPHABETA[1] >= NOALPHABETAGAMESCOUNT:
            PLAYER1.alphaBeta = True
            NEXTNOALPHABETA[0] = False
            NEXTNOALPHABETA[1] = 0

    
    pygame.quit()
    sys.exit()





        

from Gameboard import Gameboard
from Minimax import Minimax
import pygame
import numpy as np
import sys
import math

#init pygame and constants
pygame.init()
SIZE = 7  #7 rows, 6 cols
WIDTH, HEIGHT = 80 * SIZE, 80 * SIZE #must be multiples of SIZE
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


def draw_board(arr):
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
    return False

def has_clicked(): 
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            return True
    return False

if __name__ == "__main__":
    #pygame things
    clock = pygame.time.Clock()
    SCREEN.fill(BACKGROUND) 
    draw_board(BLANK_BOARD)
    pygame.display.flip()
    font = pygame.font.Font(None, 30)
    font_size = 20
    text_x, text_y, text_width, text_height = WIDTH / 2 - 3.5 * font_size, HEIGHT - HEIGHT / 17, 300, 20 

    game = Gameboard()
    mini = Minimax(3)
    turn_number = -1 # Turns start on turn # 0.

    print("Welcome to Connect 4!")

    #Game continues as long as nobody wins... 
    #is there a case when all discs are used and nobody wins?
    while not game.checkWin()[0]:
        #pygame quit
        if has_quit(): break
        turn_number += 1
        invalid_input = True

        while invalid_input:
            game.toString()
            player = (turn_number % 2) + 1 

           
            if player == 1:
                clock.tick(60)
                print(f"Player {player} ({'X' if player == 1 else '0'}), Select a column (1-7): ")
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

            else:
                col = mini.minimax(game.board, 2) + 1

            print("\n\n\n---------------------------------------------------")
            
            try:
                col = int(col)
                if col < 1 or col > 7 or not game.addDisc(player, col):
                    print("Invalid Input")
                else:
                    invalid_input = False
            except ValueError:
                print("Invalid Input")
            
            #draw board and update display
            draw_board(game.board)
            pygame.display.flip()

    print(f"Player {game.checkWin()[0]} wins!")
    game.toString()

    #display results, close pygame once player closes the game
    #draw line through winning players pieces
    while not has_quit():
        winning_player, (row, col), direction = game.checkWin()
        color_of_winner = YELLOW if winning_player == 2 else RED
        SCREEN.blit(font.render(f"Player {winning_player} wins!", True, color_of_winner), (text_x, text_y))
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
        SCREEN.fill(BACKGROUND, (text_x, text_y, text_width, text_height))
        clock.tick(60)
        
    pygame.quit()
    sys.exit()
            






        

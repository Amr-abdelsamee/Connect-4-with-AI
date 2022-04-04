from tkinter import *
from PIL import ImageTk, Image
import pygame
import sys
from puzzle import Puzzle
from circles import Circle
from tree import Tree
from buttons import Button
from agents import MinMax
# from copy import copy

NUM_ROW = 6
NUM_COL = 7

# size constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = SCREEN_WIDTH + 50
SIDES_PADDING = 10

WHITE = (255, 255, 255)
BG_COLOR = WHITE
# back ground color constant
# BGROUND_IMG = pygame.image.load("BG.jpg")

# properties of buttons
# TEXT_COLOR = (150,150,150)
TEXT_COLOR = WHITE
BUTTONS_COLOR = (12,44,130)
BUTTON_WIDTH = SCREEN_WIDTH - (2* SIDES_PADDING)
BUTTON_HEIGHT = 100
FONT_SIZE1 = 50
FONT_SIZE2 = 30



# windows variables
# start_player checks if player or AI
start_players = None
# agent_selected store the selected agent  
pruning_selected = None


# start window contains two buttons play and AI
def start_window():
    global start_players
    buttons = []
    player_button = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100, BUTTON_WIDTH,BUTTON_HEIGHT,BUTTONS_COLOR," 2 Players",TEXT_COLOR,FONT_SIZE1)
    player_button.draw(game_screen)
    buttons.append(player_button)
    AI_button = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + 50 + BUTTON_HEIGHT + SIDES_PADDING, BUTTON_WIDTH,BUTTON_HEIGHT,BUTTONS_COLOR," Play against AI",TEXT_COLOR,FONT_SIZE1)
    AI_button.draw(game_screen)
    buttons.append(AI_button)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_clicked,y_clicked = pygame.mouse.get_pos()
                
                for i in range(len(buttons)):
                    if buttons[i].check_clicked(x_clicked, y_clicked):
                        if i == 0:
                            start_players = True
                            return
                        if i == 1:
                            start_players = False
                            return
                
            pygame.display.update()
    pygame.quit()

# AI window contains three buttons BFS DFS A*
def AI_window():
    game_screen.fill(BG_COLOR)
    global pruning_selected
    buttons = []
    pruning = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100, BUTTON_WIDTH,BUTTON_HEIGHT,BUTTONS_COLOR," Alpha-Beta pruning",TEXT_COLOR,FONT_SIZE1)
    pruning.draw(game_screen)
    buttons.append(pruning)
    no_pruning = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + 50 + BUTTON_HEIGHT + SIDES_PADDING, BUTTON_WIDTH,BUTTON_HEIGHT,BUTTONS_COLOR," No pruning",TEXT_COLOR,FONT_SIZE1)
    no_pruning.draw(game_screen)
    buttons.append(no_pruning)
    
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_clicked,y_clicked = pygame.mouse.get_pos()
                for i in range(len(buttons)):
                    if buttons[i].check_clicked(x_clicked, y_clicked):
                        if i == 0:
                            pruning_selected = True
                            return
                        if i == 1:
                            pruning_selected = False
                            return
            pygame.display.update()
    pygame.quit()


pygame.init()

def message(image_name):
    tree_screen = Tk()
    tree_screen.title("State Tree")
    tree_image = Image.open(image_name)
    tkimage = ImageTk.PhotoImage(tree_image)
    image_height = tkimage.height()
    image_width = tkimage.width()

    tree_screen.geometry(str(image_width) + "x" + str(image_height))
    frame = Frame(tree_screen, width = image_width, height = image_height)
    frame.pack()
    frame.place(anchor='center', relx=0.5, rely=0.5)
    frame.pack()
    img = ImageTk.PhotoImage(tree_image)
    label = Label(frame, image = img)
    label.pack()
    tree_screen.update()
    tree_screen.deiconify()
    tree_screen.mainloop()


def tree_window(states):
    # states = [["1",["1st_state_child1","1st_state_child2","1st_state_child3","1st_state_child4"]],
    #         ["2",["2nd_state_child1","2nd_state_child2","2nd_state_child3","2nd_state_child4"]],
    #         ["3",["3rd_state_child"]],
    #         ["4",["4th_state_child1","4th_state_child3","4th_state_child4"]],
    #         ["6",["6th_state_child1","4th_state_child3"]],
    #         ["7",["7th_state_child1","4th_state_child3"]]
    #         ]
    tree = Tree(states, NUM_COL, NUM_ROW)
    image_name = tree.png_name +'.'+tree.extension
    message(image_name)



# starting the pygame screen
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# draw the background 
game_screen.fill(BG_COLOR)
# game_screen.blit(BGROUND_IMG,(0,0))
# set the title
pygame.display.set_caption("Connect 4")
# set the logo
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)



start_window()
if start_players:
    puzzle = Puzzle(game_screen, NUM_ROW, NUM_COL, SCREEN_WIDTH, SCREEN_HEIGHT)
    agent = MinMax(5, NUM_ROW, NUM_COL)
    
    playing_circle = Circle(game_screen, puzzle.circles[0].x_pos, puzzle.circles[0].y_pos - puzzle.diameter-10, puzzle.player1_color, puzzle.diameter/2)
    playing_circle.draw()

    running = True # running condition
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                x_hovered, y_hovered = pygame.mouse.get_pos()
                if x_hovered > puzzle.circles[0].x_pos and x_hovered < puzzle.circles[NUM_COL-1].x_pos:
                    clear_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 140)
                    pygame.draw.rect(game_screen, BG_COLOR, clear_rect)
                    playing_circle.change_pos(x_hovered, puzzle.circles[0].y_pos - puzzle.diameter-10)
            
            playing_circle.update(puzzle.player1_color)
            if puzzle.player_turn == puzzle.player1 and event.type == pygame.MOUSEBUTTONDOWN:
                # store the coordinates of the clicked position
                x_clicked, y_clicked = pygame.mouse.get_pos()
                puzzle.play(x_clicked , y_clicked)
                print("player1 turn and current turn is",puzzle.player_turn)
                
            if puzzle.player_turn == puzzle.player2:
                playing_circle.update(puzzle.player2_color)
                pygame.display.update()
                ai_state,_ = agent.work(puzzle.current_state)
                puzzle.update_board(ai_state)
                print("player2 turn and current turn is",puzzle.player_turn)
                # tree_window(puzzle.current_state)
            

            pygame.display.update()
else:
    AI_window()

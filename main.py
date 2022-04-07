from tkinter import *
from PIL import ImageTk, Image
import pygame
import sys
from puzzle import Puzzle
from circles import Circle
from tree import Tree
from buttons import Button
from agents import MinMax, PrunMinMax

# from copy import copy

NUM_ROW = 6
NUM_COL = 7

# size constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = SCREEN_WIDTH + 100
SIDES_PADDING = 10

WHITE = (255, 255, 255)
BG_COLOR = WHITE
# back ground color constant
# BGROUND_IMG = pygame.image.load("BG.jpg")

# properties of buttons
# TEXT_COLOR = (150,150,150)
TEXT_COLOR = WHITE
BUTTONS_COLOR = (12, 44, 130)
BUTTON_WIDTH = SCREEN_WIDTH - (2 * SIDES_PADDING)
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
    player_button = Button((SCREEN_WIDTH // 2) - (BUTTON_WIDTH // 2), (SCREEN_HEIGHT // 2) - (BUTTON_HEIGHT // 2) - 100,
                           BUTTON_WIDTH, BUTTON_HEIGHT, BUTTONS_COLOR, " 2 Players", TEXT_COLOR, FONT_SIZE1)
    player_button.draw(game_screen)
    buttons.append(player_button)
    AI_button = Button((SCREEN_WIDTH // 2) - (BUTTON_WIDTH // 2),
                       (SCREEN_HEIGHT // 2) - (BUTTON_HEIGHT // 2) -
                       100 + 50 + BUTTON_HEIGHT + SIDES_PADDING,
                       BUTTON_WIDTH, BUTTON_HEIGHT, BUTTONS_COLOR, " Play against AI", TEXT_COLOR, FONT_SIZE1)
    AI_button.draw(game_screen)
    buttons.append(AI_button)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_clicked, y_clicked = pygame.mouse.get_pos()

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


def AI_window():
    game_screen.fill(BG_COLOR)
    global pruning_selected
    buttons = []
    pruning = Button((SCREEN_WIDTH // 2) - (BUTTON_WIDTH // 2), (SCREEN_HEIGHT // 2) - (BUTTON_HEIGHT // 2) - 100,
                     BUTTON_WIDTH, BUTTON_HEIGHT, BUTTONS_COLOR, " Alpha-Beta pruning", TEXT_COLOR, FONT_SIZE1)
    pruning.draw(game_screen)
    buttons.append(pruning)
    no_pruning = Button((SCREEN_WIDTH // 2) - (BUTTON_WIDTH // 2),
                        (SCREEN_HEIGHT // 2) - (BUTTON_HEIGHT // 2) -
                        100 + 50 + BUTTON_HEIGHT + SIDES_PADDING,
                        BUTTON_WIDTH, BUTTON_HEIGHT, BUTTONS_COLOR, " No pruning", TEXT_COLOR, FONT_SIZE1)
    no_pruning.draw(game_screen)
    buttons.append(no_pruning)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_clicked, y_clicked = pygame.mouse.get_pos()
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


def end_winodw(player1_score, player2_score, player1_type, player2_type):
    clear_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 140)
    pygame.draw.rect(game_screen, BG_COLOR, clear_rect)

    game_ends_label = Button((BUTTON_WIDTH // 4),
                            50,
                            BUTTON_WIDTH//2,
                            BUTTON_HEIGHT//1.3,
                            BUTTONS_COLOR,
                            "   Game Over",
                            TEXT_COLOR,
                            FONT_SIZE1)
    game_ends_label.draw(game_screen)

    player1_label = Button((SCREEN_WIDTH // 2) - (BUTTON_WIDTH // 2),
                           (SCREEN_HEIGHT // 2) - (BUTTON_HEIGHT // 2) - 150 + BUTTON_HEIGHT + SIDES_PADDING,
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT//1.3,
                            BUTTONS_COLOR,
                            " " + player1_type + " score: " + str(player1_score),
                            TEXT_COLOR,
                            FONT_SIZE1)
    player1_label.draw(game_screen)

    player2_label = Button((SCREEN_WIDTH // 2) - (BUTTON_WIDTH // 2),
                           (SCREEN_HEIGHT // 2) - (BUTTON_HEIGHT // 2) -
                            50 + BUTTON_HEIGHT + SIDES_PADDING,
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT//1.3,
                            BUTTONS_COLOR,
                            " " + player2_type + " score: " + str(player2_score),
                            TEXT_COLOR,
                            FONT_SIZE1)
    player2_label.draw(game_screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update()


pygame.init()


def message(image_name):
    tree_screen = Tk()
    tree_screen.title("State Tree")
    tree_image = Image.open(image_name)
    tkimage = ImageTk.PhotoImage(tree_image)
    image_height = tkimage.height()
    image_width = tkimage.width()

    tree_screen.geometry(str(image_width) + "x" + str(image_height))
    frame = Frame(tree_screen, width=image_width, height=image_height)
    frame.pack()
    frame.place(anchor='center', relx=0.5, rely=0.5)
    frame.pack()
    img = ImageTk.PhotoImage(tree_image)
    label = Label(frame, image=img)
    label.pack()
    tree_screen.update()
    tree_screen.deiconify()
    tree_screen.mainloop()


def tree_window(states):
    tree = Tree(states, NUM_COL, NUM_ROW)
    image_name = tree.png_name + '.' + tree.extension
    # message(image_name)


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
    playing_circle = Circle(game_screen, puzzle.circles[0].x_pos, puzzle.circles[0].y_pos - puzzle.diameter - 10,
                            puzzle.player1_color, puzzle.diameter / 2)
    playing_circle.draw()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                x_hovered, y_hovered = pygame.mouse.get_pos()
                if x_hovered > puzzle.circles[0].x_pos and x_hovered < puzzle.circles[NUM_COL - 1].x_pos:
                    clear_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 140)
                    pygame.draw.rect(game_screen, BG_COLOR, clear_rect)
                    playing_circle.change_pos(
                        x_hovered, puzzle.circles[0].y_pos - puzzle.diameter - 10)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # store the coordinates of the clicked position
                x_clicked, y_clicked = pygame.mouse.get_pos()
                puzzle.play(x_clicked, y_clicked)
                if puzzle.player_turn == puzzle.player1:
                    playing_circle.update(
                        puzzle.player1_color, puzzle.player_turn)
                else:
                    playing_circle.update(
                        puzzle.player2_color, puzzle.player_turn)
            
            pygame.display.update()
            
            if puzzle.board_is_full:
                end_winodw(puzzle.player1_score, puzzle.player2_score,"Player 1", "Player 2")


else:
    AI_window()
    puzzle = Puzzle(game_screen, NUM_ROW, NUM_COL, SCREEN_WIDTH, SCREEN_HEIGHT)
    playing_circle = Circle(game_screen, puzzle.circles[0].x_pos, puzzle.circles[0].y_pos - puzzle.diameter - 10,
                            puzzle.player1_color, puzzle.diameter / 2)
    playing_circle.draw()

    if pruning_selected:
        agent = PrunMinMax(4, NUM_ROW, NUM_COL)
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    x_hovered, y_hovered = pygame.mouse.get_pos()
                    if puzzle.circles[0].x_pos < x_hovered < puzzle.circles[NUM_COL - 1].x_pos:
                        clear_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 140)
                        pygame.draw.rect(game_screen, BG_COLOR, clear_rect)
                        playing_circle.change_pos(
                            x_hovered, puzzle.circles[0].y_pos - puzzle.diameter - 10)

                playing_circle.update(puzzle.player1_color, puzzle.player_turn)
                if puzzle.player_turn == puzzle.player1 and event.type == pygame.MOUSEBUTTONDOWN:
                    # store the coordinates of the clicked position
                    x_clicked, y_clicked = pygame.mouse.get_pos()
                    puzzle.play(x_clicked, y_clicked)

                if puzzle.player_turn == puzzle.player2:
                    playing_circle.update(
                        puzzle.player2_color, puzzle.player_turn)
                    pygame.display.update()
                    ai_state, ai_col = agent.work(puzzle.current_state)
                    puzzle.play(x_clicked, y_clicked, ai_col)
                    pygame.display.update()
                    ai_tree = agent.tree
                    tree_window(ai_tree)
                pygame.display.update()

                if puzzle.board_is_full:
                    end_winodw(puzzle.player1_score, puzzle.player2_score,"Your", "AI")

    else:
        agent = MinMax(3, NUM_ROW, NUM_COL)
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    x_hovered, y_hovered = pygame.mouse.get_pos()
                    if puzzle.circles[0].x_pos < x_hovered < puzzle.circles[NUM_COL - 1].x_pos:
                        clear_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 140)
                        pygame.draw.rect(game_screen, BG_COLOR, clear_rect)
                        playing_circle.change_pos(
                            x_hovered, puzzle.circles[0].y_pos - puzzle.diameter - 10)

                playing_circle.update(puzzle.player1_color, puzzle.player_turn)
                if puzzle.player_turn == puzzle.player1 and event.type == pygame.MOUSEBUTTONDOWN:
                    # store the coordinates of the clicked position
                    x_clicked, y_clicked = pygame.mouse.get_pos()
                    puzzle.play(x_clicked, y_clicked)

                if puzzle.player_turn == puzzle.player2:
                    playing_circle.update(
                        puzzle.player2_color, puzzle.player_turn)
                    pygame.display.update()
                    ai_state, ai_col = agent.work(puzzle.current_state)
                    puzzle.play(x_clicked, y_clicked, ai_col)
                    pygame.display.update()
                    ai_tree = agent.tree
                    tree_window(ai_tree)
                pygame.display.update()

                if puzzle.board_is_full:
                    end_winodw(puzzle.player1_score, puzzle.player2_score,"Your", "AI")

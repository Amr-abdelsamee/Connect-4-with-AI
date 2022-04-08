from copy import copy
import pygame
from circles import Circle
from buttons import Button
# screen constants
SIDES_PADDING = 10
UPPER_PADDING = 150
LOWER_PADDING = 10
INBTWN_SPACE = 4

WIN_CONNECTION = 4
# blocks constants
CIRCLE_COLOR = (200, 200, 200)
RECT_COLOR = (0, 0, 0)
PLAYER1_COLOR = (12, 90, 55)
PLAYER2_COLOR = (120, 9, 5)


class Puzzle:

    def __init__(self, screen, num_row, num_col, screen_width, screen_height, game_mode):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_row = num_row
        self.num_col = num_col

        self.circles = []   # array of obj
        self.playable = []  # array of ints used to drop the pieces
        self.occupied = []  # array of ints used to check if board if full
        self.states = [] # array of strs contain the histry of plays
        self.board_is_full = False # called in the main to display the final score window
        
        self.current_state = '0' * (self.num_row * self.num_col) # initial state of the board
        self.states.append(self.current_state)

        self.diameter = ((self.screen_width - (2 * SIDES_PADDING)) - ((self.num_col - 1) * INBTWN_SPACE)) / self.num_col
        self.player1 = '1'
        self.player2 = '2'
        self.player1_color = PLAYER1_COLOR
        self.player2_color = PLAYER2_COLOR
        self.player1_score = 0
        self.player2_score = 0
        self.player_turn = '1' # player 1 plays first 

        self.game_mode = game_mode # 1 if player Vs player ,2 if player Vs AI
        if self.game_mode == 2:
            # tree control buttons displayed only in the AI board
            self.create_tree_button = None
            self.display_tree_button = None
            self.create_tree = True
            self.display_tree = True

        self.create_circles()
        self.generate_playable()


    # create_circles creates the circle of the game
    def create_circles(self):
        """creare_circles used to create the game circles. 
        It fills self.circles with objects from the class Circle in circles.py file
        """
        # initial cordinates of the first circle
        x = SIDES_PADDING + self.diameter / 2
        y = UPPER_PADDING + self.diameter / 2

        if self.game_mode == 2:
            self.create_tree_button = Button(0,0, 120, 25, (0,255,0), " Create tree: ON", (255,255,255), 15)
            self.create_tree_button.draw(self.screen)
            
            self.display_tree_button = Button(130,0, 120, 25, (0,255,0), " Diplay tree: ON", (255,255,255), 15)
            self.display_tree_button.draw(self.screen)


        self.rect = pygame.Rect(SIDES_PADDING - 5, UPPER_PADDING - 5, self.screen_width - (2 * SIDES_PADDING) + 10,
                                self.screen_height - UPPER_PADDING - LOWER_PADDING)
        pygame.draw.rect(self.screen, RECT_COLOR, self.rect)

        for _ in range(0, self.num_row):
            for _ in range(0, self.num_col):
                circle = Circle(self.screen, x, y, CIRCLE_COLOR, self.diameter / 2)
                circle.draw()
                self.circles.append(circle)
                x = x + self.diameter + INBTWN_SPACE
            x = SIDES_PADDING + self.diameter / 2
            y = y + self.diameter + INBTWN_SPACE


    def generate_playable(self):
        """It is used to fill self.playable with arrays each index of array represent a column
        each array contain the indexes that can be used to insert a circle in in that column
        """
        temp = []
        for i in range(self.num_col):
            inc = i
            for j in range(self.num_row):
                temp.append(inc)
                inc += self.num_col
            self.playable.append(copy(temp))
            temp.clear()


    def get_col_clicked(self, x_clicked, y_clicked):
        """It's used to get the index of the clicked column
        if the clicked position was not a column it returns None

        Args:
            x_clicked (int): the x coordinates of the clicked position
            y_clicked (int): the y coordinates of the clicked position

        Returns:
            i (int): the index of the column
        """
        last_circle_index = (self.num_col * self.num_row) - 1
        y_end = self.circles[last_circle_index].y_pos + (self.diameter / 2)
        for i in range(self.num_col):
            x_start = self.circles[i].x_pos - (self.diameter / 2)
            x_end = self.circles[i].x_pos + (self.diameter / 2)
            y_start = self.circles[i].y_pos - (self.diameter / 2)
            if (x_start <= x_clicked < x_end
                    and y_start <= y_clicked < y_end):
                return i


    def drop_piece(self, x_clicked, y_clicked, color, owner, col=-1):
        """ It's used to drop the played piece in its position which is represented by 
            the column index.
            self.playable is used here to pop the max index in the clicked column 
            this index is the place of the dropped piece

        Args:
            x_clicked (int): the x coordinates of the clicked position
            y_clicked (int): the y coordinates of the clicked position
            color (tuple): color of the owner ,RGB value
            owner (str): indicate the wwho played this piece
            col (int): default value is -1 if player turn other wise it's sent from the AI agent

        Returns:
            
            (bool): in case of player's turn it returns true to confirm the piece is dropped , false if column is full
        """
        
        col_index = self.get_col_clicked(x_clicked, y_clicked)
        if col != -1:
            col_index = col
        if col_index is not None:
            if self.playable[col_index]:
                circle_index = max(self.playable[col_index])
                self.circles[circle_index].update(color, owner)
                self.playable[col_index].remove(circle_index)
                self.occupied.append(circle_index)
                self.update_state(circle_index, owner)
                return True
            else:
                return False


    def update_state(self, index, player):
        """ It's used to update the state of the board

        Args:
            index (int): the index of the droped 
            player (str): the player who played last piece
        """
        print(type(player))
        self.current_state = list(self.current_state)
        self.current_state[index] = player
        self.current_state = "".join(self.current_state)
        self.states.append(self.current_state)


    def check_horiz(self, state, p):
        """used to calculate the piece of the player horizontally

        Args:
            state (str): the current state of the board
            p (str): the player

        Returns:
            points (int): points of the player from the horizontal calculations
        """
        points = 0
        connected = 0
        for i in range(self.num_row):
            j = -1
            while j < self.num_col:
                j += 1
                while j < self.num_col and state[i * self.num_col + j] == p:
                    connected += 1
                    j += 1
                if connected > 3:
                    points += connected - 3
                connected = 0
        return points


    def check_vert(self, state, p):
        """used to calculate the piece of the player vertically

        Args:
            state (str): the current state of the board
            p (str): the player

        Returns:
            points (int): points of the player from the vertical calculations
        """
        points = 0
        connected = 0
        for i in range(self.num_col):
            j = -1
            while j < self.num_row:
                j += 1
                while j < self.num_row and state[j * self.num_col + i] == p:
                    connected += 1
                    j += 1
                if connected > 3:
                    points += connected - 3
                connected = 0
        return points


    def check_ldiag(self, state, p):
        """used to calculate the piece of the player in left diagonals

        Args:
            state (str): the current state of the board
            p (str): the player

        Returns:
            points (int): points of the player from the left diagonals calculations
        """
        points = 0
        connected = 0
        for i in range(self.num_row):
            j = 0
            while i < self.num_row and j < self.num_col:
                if state[i * self.num_col + j] == p:
                    connected += 1
                else:
                    if connected > 3:
                        points += connected - 3
                    connected = 0
                j += 1
                i += 1
            if connected > 3:
                points += connected - 3
            connected = 0

        for i in range(self.num_row):
            j = 1 + i
            i = 0

            while i < self.num_row and j < self.num_col:
                if state[i * self.num_col + j] == p:
                    connected += 1
                else:
                    if connected > 3:
                        points += connected - 3
                    connected = 0
                j += 1
                i += 1
            if connected > 3:
                points += connected - 3
            connected = 0
        return points


    def check_rdiag(self, state, p):
        """used to calculate the piece of the player in right diagonals

        Args:
            state (str): the current state of the board
            p (str): the player

        Returns:
            points (int): points of the player from the right diagonals calculations
        """
        points = 0
        connected = 0
        for i in range(self.num_row):
            j = self.num_col - 1
            while i < self.num_row and j > -1:
                if state[i * self.num_col + j] == p:
                    connected += 1
                else:
                    if connected > 3:
                        points += connected - 3
                    connected = 0
                j -= 1
                i += 1
            if connected > 3:
                points += connected - 3
            connected = 0

        for i in range(self.num_row):
            j = self.num_col - 2 - i
            i = 0
            while i < self.num_row and j > -1:
                if state[i * self.num_col + j] == p:
                    connected += 1
                else:
                    if connected > 3:
                        points += connected - 3
                    connected = 0
                j -= 1
                i += 1
            if connected > 3:
                points += connected - 3
            connected = 0
        return points


    def get_final_score(self, state, player):
        """used to calculate the total score of the player

        Args:
            state (str): the current state of the board
            player (str): the player

        Returns:
            points (int): total points of the player
        """
        points = 0
        points += self.check_horiz(state, player)
        points += self.check_vert(state, player)
        points += self.check_ldiag(state, player)
        points += self.check_rdiag(state, player)
        return points


    def play(self, x_clicked, y_clicked, col=-1):
        """the start method which called in main.py 
            it's called whenever a player or an AI plays

        Args:
            x_clicked (int): the x coordinates of the clicked position
            y_clicked (int): the y coordinates of the clicked position
            col (int, optional): default value is -1 if player turn other wise it's sent from the AI agent
        """
        if self.player_turn == self.player1:
            switch_player = self.drop_piece(x_clicked, y_clicked, self.player1_color, self.player_turn, col)
            if switch_player:
                self.player_turn = self.player2
        elif self.player_turn == self.player2:
            switch_player = self.drop_piece(x_clicked, y_clicked, self.player2_color, self.player_turn, col)
            if switch_player:
                self.player_turn = self.player1
        
        # buttons that controlls the tree it is displayed only in the AI board
        if self.game_mode == 2 :
            if self.create_tree_button.check_clicked(x_clicked, y_clicked):
                if self.create_tree:
                    self.create_tree_button.update(" Create tree: OFF", (255,0,0))
                    self.create_tree_button.draw(self.screen)
                    self.create_tree = False
                    self.display_tree_button.update(" Diplay tree: OFF", (255,0,0))
                    self.display_tree_button.draw(self.screen)
                    self.display_tree = False
                else:
                    self.create_tree_button.update(" Diplay tree: ON", (0,255,0))
                    self.create_tree_button.draw(self.screen)
                    self.create_tree = True

            if self.create_tree and self.display_tree_button.check_clicked(x_clicked, y_clicked):
                if self.display_tree:
                    self.display_tree_button.update(" Diplay tree: OFF", (255,0,0))
                    self.display_tree_button.draw(self.screen)
                    self.display_tree = False
                else:
                    self.display_tree_button.update(" Diplay tree: ON", (0,255,0))
                    self.display_tree_button.draw(self.screen)
                    self.display_tree = True

        # check if the board is full to calculate the final score of each player
        if len(self.occupied) == self.num_col*self.num_row:
            self.player1_score = self.get_final_score(self.current_state, '1')
            self.player2_score = self.get_final_score(self.current_state, '2')
            print("player 1 score : ",self.player1_score)
            print("player 2 score : ",self.player2_score)
            self.board_is_full = True

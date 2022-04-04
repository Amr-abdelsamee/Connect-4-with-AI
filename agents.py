import math


class MinMax:
    def __init__(self, depth, num_row, num_col):
        self.num_row = num_row
        self.num_col = num_col
        self.tree = ''
        self.state = ''
        self.depth = depth
        self.current_depth = 0

    def update(self, state):
        self.state = state

    def calc_score(self, connected, index=0):
        if connected == 0:
            return 0
        if connected == 1:
            if self.num_col - index == self.num_col - self.num_col/2:
                return 5
            if 0 < index < self.num_col-1:
                return 3
            else :
                return 1
        return pow(10, connected - 1)

    def check_horiz(self, state, p):
        points = 0
        connected = 0
        for i in range(self.num_row):
            j = -1
            while j < self.num_col:
                j += 1
                while j < self.num_col and state[i * self.num_col + j] == p:
                    connected += 1
                    j += 1
                points += self.calc_score(connected, j-1)
                connected = 0
        return points

    def check_vert(self, state, p):
        points = 0
        connected = 0
        for i in range(self.num_col):
            j = -1
            while j < self.num_row:
                j += 1
                while j < self.num_row and state[j * self.num_col + i] == p:
                    connected += 1
                    j += 1
                points += self.calc_score(connected, i)
                connected = 0
        return points

    def check_ldiag(self, state, p):
        points = 0
        connected = 0
        for i in range(self.num_row):
            j = 0
            while i < self.num_row and j < self.num_col:
                if state[i * self.num_col + j] == p:
                    connected += 1
                else:
                    points += self.calc_score(connected, j)
                    connected = 0
                j += 1
                i += 1
            points += self.calc_score(connected, j-1)
            connected = 0

        for i in range(self.num_row):
            j = 1 + i
            i = 0

            while i < self.num_row and j < self.num_col:
                if state[i * self.num_col + j] == p:
                    connected += 1
                else:
                    points += self.calc_score(connected, j)
                    connected = 0
                j += 1
                i += 1
            points += self.calc_score(connected, j-1)
            connected = 0
        return points

    def check_rdiag(self, state, p):
        points = 0
        connected = 0
        for i in range(self.num_row):
            j = self.num_col - 1
            while i < self.num_row and j > -1:
                if state[i * self.num_col + j] == p:
                    connected += 1
                else:
                    points += self.calc_score(connected, j)
                    connected = 0
                j -= 1
                i += 1
            points += self.calc_score(connected, j+1)
            connected = 0

        for i in range(self.num_row):
            j = self.num_col - 2 - i
            i = 0
            while i < self.num_row and j > -1:
                if state[i * self.num_col + j] == p:
                    connected += 1
                else:
                    points += self.calc_score(connected, j)
                    connected = 0
                j -= 1
                i += 1
            points += self.calc_score(connected, j+1)
            connected = 0
        return points

    def get_points(self, state, p):
        points = 0
        points += self.check_horiz(state, p)
        points += self.check_vert(state, p)
        points += self.check_ldiag(state, p)
        points += self.check_rdiag(state, p)
        return points

    def heu(self, state):
        player = self.get_points(state, '1')
        AI = self.get_points(state, '2')
        return AI - player

    def maximize(self, state, d):
        if d == self.depth:
            return None, 0, self.heu(state)
        max_child, max_column, max_utility = None, 0, float('-inf')
        children = self.get_next_states(state, True)
        for child, column in children:
            _, _, utility = self.minimize(child, d + 1)
            if utility > max_utility:
                max_child, max_column, max_utility = child, column, utility
        return max_child, max_column, max_utility

    def minimize(self, state, d):
        if d == self.depth:
            return None, 0, self.heu(state)
        min_child, min_column, min_utility = None, 0, float('inf')
        children = self.get_next_states(state, False)
        for child, column in children:
            _, _, utility = self.maximize(child, d + 1)
            if utility < min_utility:
                min_child, min_column, min_utility = child, column, utility
        return min_child, min_column, min_utility

    def decision(self):
        child, column, utility = self.maximize(self.state, 0)
        return child, column, self.tree

    def get_next_states(self, state, turn):  # turn is True for AI, False for Human
        if turn:
            char = '2'
        else:
            char = '1'
        children = []
        for i in range(self.num_col):
            index = -1
            column = 0
            changed = False
            child = ""
            for j in range(len(state) - 1, -1, -1):
                if state[j] == '0':
                    index += 1
                    if j + 7 >= len(state) or state[j + 7] != '0':
                        if index == i:
                            child = char + child
                            changed = True
                            column = j % self.num_col
                        else:
                            child = state[j] + child
                    else:
                        child = state[j] + child
                        index -= 1
                else:
                    child = state[j] + child
            if changed is False:
                break
            tup = (child, column)
            children.append(tup)

        return children

    def work(self, state):
        self.update(state)
        newState, column, tree = self.decision()
        return newState, column, tree

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
                if connected > 3:
                    points += connected - 3
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
            return None, self.heu(state)
        max_child, max_utility = None, float('-inf')
        children = self.get_next_states(state, True)
        for child in children:
            _, utility = self.minimize(child, d + 1)
            if utility > max_utility:
                max_child, max_utility = child, utility
        return max_child, max_utility

    def minimize(self, state, d):
        if d == self.depth:
            return None, self.heu(state)
        min_child, min_utility = None, float('inf')
        children = self.get_next_states(state, False)
        for child in children:
            _, utility = self.maximize(child, d + 1)
            if utility < min_utility:
                min_child, min_utility = child, utility
        return min_child, min_utility

    def decision(self):
        child, utility = self.maximize(self.state, 0)
        return child, self.tree

    def get_next_states(self, state, turn):  # turn is True for AI, False for Human
        if turn:
            char = '2'
        else:
            char = '1'
        children = []
        for i in range(self.num_col):
            index = -1
            child = ""
            for j in range(len(state) - 1, -1, -1):
                if state[j] == '0':
                    index += 1
                    if (j + 7 >= len(state) or state[j + 7] != '0'):
                        if index == i:
                            child = char + child
                        else:
                            child = state[j] + child
                    else:
                        child = state[j] + child
                        index -= 1
                else:
                    child = state[j] + child
            children.append(child)
        return children

    def work(self, state):
        self.update(state)
        newState, tree = self.decision()
        return newState, tree

import math

class MinMax:
    def __init__(self, depth):
        self.state = ''
        self.depth = depth
        self.current_depth = 0

    def update(self, state):
        self.state = state

    def heu(self, state):
        pass

    def maximize(self, state):
        if math.log(self.current_depth, 7) - 1 == self.depth:
            return None, heu(state)
        max_child, max_utility = None, float('-inf')
        children = self.get_next_states(state, True)
        for child in children:
            _, utility = minimize(child)
            if utility > max_utility:
                max_child, max_utility = child, utility
        self.current_depth += 1
        return max_child, max_utility

    def minimize(self, state):
        if math.log(self.current_depth, 7) - 1 == self.depth:
            return None, heu(state)
        min_child, min_utility = None, float('inf')
        children = self.get_next_states(state, False)
        for child in children:
            _, utility = maximize(child)
            if utility < min_utility:
                min_child, min_utility = child, utility
        self.current_depth += 1
        return min_child, min_utility

    def decision(self):
        self.current_depth = 0
        child, utility = self.maximize(state)
        return child

    def get_next_states(state, turn):  # turn is True for AI, False for Human
        if turn:
            char = '2'
        else:
            char = '1'
        children = []
        for i in range(7):
            index = -1
            child = ""
            for character in state[::-1]:
                if character == '0':
                    index += 1
                if character == '0' and index == i:
                    child = char + child
                else:
                    child = character + child
            children.append(child)
        return children

    def work(self):
        return col, tree

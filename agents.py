import math

class MinMax:
    def __init__(self, depth):
        self.state = ''
        self.depth = depth

    def update(self, state):
        self.state = state

    def heu(self, state):
        pass

    def maximize(self, state, d):
        if d == self.depth:
            return None, heu(state)
        max_child, max_utility = None, float('-inf')
        children = self.get_next_states(state, True)
        for child in children:
            _, utility = minimize(child, d + 1)
            if utility > max_utility:
                max_child, max_utility = child, utility
        return max_child, max_utility

    def minimize(self, state, d):
        if d == self.depth:
            return None, heu(state)
        min_child, min_utility = None, float('inf')
        children = self.get_next_states(state, False)
        for child in children:
            _, utility = maximize(child, d + 1)
            if utility < min_utility:
                min_child, min_utility = child, utility
        return min_child, min_utility

    def decision(self):
        child, utility = self.maximize(state, 0)
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

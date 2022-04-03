class MinMax:
    def __init__(self, depth):
        self.state = ''
        self.depth = depth

    def update(self, state):
        self.state = state

    def heu(self, state):
        pass

    def maximize(self,state):
        return maxChild, maxUtility

    def minimize(self,state):
        return minChild, minUtility

    def decision(self):
        child, utility = self.maximize(state)
        return child

    def get_next_states(self, state):
        pass

    def work(self):
        return col, tree

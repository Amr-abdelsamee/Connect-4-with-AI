class Agents:
    def __init__(self, depth, num_row, num_col):
        self.num_row = num_row
        self.num_col = num_col
        self.tree = []
        self.state = ''
        self.depth = depth
        self.current_depth = 0
        self.parent = 0
        self.index = 0

    def update(self, state):
        self.state = state
        self.tree.clear()
        self.parent = 0
        self.index = 0
        self.current_depth = 0

    def calc_score(self, connected, index=0):
        if connected == 0:
            return 0
        if connected == 1:
            if self.num_col - index == self.num_col - self.num_col / 2:
                return 5
            if 0 < index < self.num_col - 1:
                return 3
            else:
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
                points += self.calc_score(connected, j - 1)
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
            points += self.calc_score(connected, j - 1)
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
            points += self.calc_score(connected, j - 1)
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
            points += self.calc_score(connected, j + 1)
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
            points += self.calc_score(connected, j + 1)
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

    def decision(self):
        pass

    def search_tree(self, tree, parent):
        for branch in tree:
            try:
                if branch[0][0] != None and branch[0][0] == parent:
                    return branch
            except:
                print("aaaaaaaaaaaaaaaaaaaaaa")
                print(branch)

        return None

    def create_tree(self):
        newtree = [(self.tree[0], self.tree[1])]   # new node = parent,children
        for children in self.tree[1:]:
            for child in children:
                x = self.search_tree(self.tree[1:], child[1])
                if x is not None:
                    newnode = child, x
                    newtree.append(newnode)
        return newtree


class MinMax(Agents):
    def maximize(self, state, d, p):
        gp = []
        if d == self.depth:
            return None, 0, self.heu(state)
        max_child, max_column, max_utility = None, 0, float('-inf')
        children = self.get_next_states(state, True)
        self.index += len(children)
        index = self.index
        for child, column in children:
            _, _, utility = self.minimize(child, d + 1, index)
            node = (p, index, column, utility, 'minGate')
            index -= 1
            gp.append(node)
            if utility > max_utility:
                max_child, max_column, max_utility = child, column, utility
        if len(gp) != 0: 
            self.tree.append(gp)
        return max_child, max_column, max_utility

    def minimize(self, state, d, p):
        gp = []
        if d == self.depth:
            return None, 0, self.heu(state)
        min_child, min_column, min_utility = None, 0, float('inf')
        children = self.get_next_states(state, False)
        self.index += len(children)
        index = self.index
        for child, column in children:
            _, _, utility = self.maximize(child, d + 1, index)
            node = (p, index, column, utility, 'maxGate')
            index -= 1
            gp.append(node)
            if utility < min_utility:
                min_child, min_column, min_utility = child, column, utility
        if len(gp) != 0: 
            self.tree.append(gp)
        return min_child, min_column, min_utility

    def decision(self):
        child, column, utility = self.maximize(self.state, 0, 0)
        return child, column, utility

    def work(self, state):
        self.update(state)
        newState, column, utility = self.decision()
        self.tree.append((state, 0, column, utility, 'maxgate'))
        self.tree.reverse()
        self.tree = self.create_tree()
        return newState, column


class PrunMinMax(Agents):
    def maximize(self, state, d, p, alpha, beta):
        gp = []
        if d == self.depth:
            return None, 0, self.heu(state)
        max_child, max_column, max_utility = None, 0, float('-inf')
        children = self.get_next_states(state, True)
        self.index += len(children)
        index = self.index
        for child, column in children:
            _, _, utility = self.minimize(child, d + 1, index, alpha, beta)
            node = (p, index, column, utility, 'minGate')
            index -= 1
            gp.append(node)
            if utility > max_utility:
                max_child, max_column, max_utility = child, column, utility
            if max_utility >= beta:
                break
            if max_utility > alpha:
                alpha = max_utility
        if len(gp) != 0: 
            self.tree.append(gp)
        return max_child, max_column, max_utility

    def minimize(self, state, d, p, alpha, beta):
        gp = []
        if d == self.depth:
            return None, 0, self.heu(state)
        min_child, min_column, min_utility = None, 0, float('inf')
        children = self.get_next_states(state, False)
        self.index += len(children)
        index = self.index
        for child, column in children:
            _, _, utility = self.maximize(child, d + 1, index, alpha, beta)
            node = (p, index, column, utility, 'maxGate')
            index -= 1
            gp.append(node)
            if utility < min_utility:
                min_child, min_column, min_utility = child, column, utility
            if min_utility <= alpha:
                break
            if min_utility > beta:
                alpha = min_utility
        if len(gp) != 0: 
            self.tree.append(gp)
        return min_child, min_column, min_utility

    def decision(self):
        child, column, utility = self.maximize(self.state, 0, 0, float('-inf'), float('inf'))
        return child, column, utility

    def work(self, state):
        self.update(state)
        newState, column, utility = self.decision()
        self.tree.append((state, 0, column, utility, 'maxgate'))
        self.tree.reverse()
        self.tree = self.create_tree()
        return newState, column


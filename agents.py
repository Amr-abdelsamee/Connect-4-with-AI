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

    def calc_score(self, connected, index=0, p='1'):
        v = 1
        if p == '1':
            v = -1
        if connected == 0:
            return 0
        if connected == 1:
            if self.num_col - index == self.num_col - self.num_col / 2:
                return 5 * v
            if 0 < index < self.num_col - 1:
                return 3 * v
            else:
                return 1 * v
        return pow(10, connected - 1) * v

    def swap(self, v):
      if v == '1':
        return '2'
      else:
        return '1'

    def check_horiz(self, state):
        points = 0
        connected = 0
        v = '1'
        for i in range(self.num_row):
            j = -1
            while j < self.num_col:
                j += 1
                while j < self.num_col and state[i * self.num_col + j] == v:
                    connected += 1
                    j += 1
                points += self.calc_score(connected, j - 1,v)
                connected = 1
                v = self.swap(v)
        return points

    def check_vert(self, state):
        points = 0
        connected = 0
        v = '1'
        for i in range(self.num_col):
            j = -1
            while j < self.num_row:
                j +=1
                while j < self.num_row and state[j * self.num_col + i] == v:
                    connected += 1
                    j += 1
                points += self.calc_score(connected, i, v)
                connected = 1
                v = self.swap(v)
        return points

    def check_ldiag(self, state):
        points = 0
        connected = 0
        v = '1'
        for i in range(self.num_row):
            j = 0
            while i < self.num_row and j < self.num_col:
                if state[i * self.num_col + j] == v:
                    connected += 1
                else:
                    points += self.calc_score(connected, j, v)
                    connected = 1
                    v = self.swap(v)
                j += 1
                i += 1
            points += self.calc_score(connected, j - 1, v)
            connected = 0

        for i in range(self.num_row):
            j = 1 + i
            i = 0
            while i < self.num_row and j < self.num_col:
                if state[i * self.num_col + j] == v:
                    connected += 1
                else:
                    points += self.calc_score(connected, j, v)
                    connected = 1
                    v = self.swap(v)
                j += 1
                i += 1
            points += self.calc_score(connected, j - 1, v)
            connected = 0
        return points

    def check_rdiag(self, state):
        points = 0
        connected = 0
        v = '1'
        for i in range(self.num_row):
            j = self.num_col - 1
            while i < self.num_row and j > -1:
                if state[i * self.num_col + j] == v:
                    connected += 1
                else:
                    points += self.calc_score(connected, j, v)
                    connected = 1
                    v = self.swap(v)
                j -= 1
                i += 1
            points += self.calc_score(connected, j + 1, v)
            connected = 0

        for i in range(self.num_row):
            j = self.num_col - 2 - i
            i = 0
            while i < self.num_row and j > -1:
                if state[i * self.num_col + j] == v:
                    connected += 1
                else:
                    points += self.calc_score(connected, j, v)
                    connected = 1
                    v = self.swap(v)
                j -= 1
                i += 1
            points += self.calc_score(connected, j + 1, v)
            connected = 0
        return points

    def get_points(self, state):
        points = 0
        points += self.check_horiz(state)
        points += self.check_vert(state)
        points += self.check_ldiag(state)
        points += self.check_rdiag(state)
        return points

    def heu(self, state):
        return self.get_points(state)

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


    def create_tree(self):
        x = len(self.tree) - 2
        newTree = [(self.tree[x+1], self.tree[x])]
        for i in range(x,-1,-1):
            if self.tree[i][0][0] != -1:
                for parent in self.tree[i]:
                    newTree.append((parent, self.tree[parent[0]]))
        return newTree


class MinMax(Agents):
    def maximize(self, state, d, p):
        gp = []
        if d == self.depth:
            return None, 0, self.heu(state), -1
        max_child, max_column, max_utility = None, 0, float('-inf')
        children = self.get_next_states(state, True)
        self.index += len(children)
        index = self.index
        for child, column in children:
            _, _, utility,i = self.minimize(child, d + 1, index)
            node = (i, p, index, column, utility, 'minGate')
            index -= 1
            gp.append(node)
            if utility > max_utility:
                max_child, max_column, max_utility = child, column, utility
        if len(gp) != 0:
            self.tree.append(gp)
        return max_child, max_column, max_utility, len(self.tree)-1

    def minimize(self, state, d, p):
        gp = []
        if d == self.depth:
            return None, 0, self.heu(state), -1
        min_child, min_column, min_utility = None, 0, float('inf')
        children = self.get_next_states(state, False)
        self.index += len(children)
        index = self.index
        i = len(children)
        for child, column in children:
            _, _, utility, i = self.maximize(child, d + 1, index)
            node = (i, p, index, column, utility, 'maxGate')
            index -= 1
            gp.append(node)
            if utility < min_utility:
                min_child, min_column, min_utility = child, column, utility
        if len(gp) != 0:
            self.tree.append(gp)
        return min_child, min_column, min_utility, len(self.tree)-1

    def decision(self):
        child, column, utility, i = self.maximize(self.state, 0, 0)
        return child, column, utility, i

    def work(self, state):
        self.update(state)
        newState, column, utility, i = self.decision()
        self.tree.append((i, state, 0, column, utility, 'maxgate'))
        self.tree = self.create_tree()
        return newState, column


class PrunMinMax(Agents):
    def maximize(self, state, d, p, alpha, beta):
        gp = []
        if d == self.depth:
            return None, 0, self.heu(state), -1
        max_child, max_column, max_utility = None, 0, float('-inf')
        children = self.get_next_states(state, True)
        self.index += len(children)
        index = self.index
        for child, column in children:
            _, _, utility, i = self.minimize(child, d + 1, index, alpha, beta)
            node = (i, p, index, column, utility, 'minGate')
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
        return max_child, max_column, max_utility, len(self.tree)-1

    def minimize(self, state, d, p, alpha, beta):
        gp = []
        if d == self.depth:
            return None, 0, self.heu(state),-1
        min_child, min_column, min_utility = None, 0, float('inf')
        children = self.get_next_states(state, False)
        self.index += len(children)
        index = self.index
        for child, column in children:
            _, _, utility,i = self.maximize(child, d + 1, index, alpha, beta)
            node = (i, p, index, column, utility, 'maxGate')
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
        return min_child, min_column, min_utility,len(self.tree)-1

    def decision(self):
        child, column, utility,i = self.maximize(self.state, 0, 0, float('-inf'), float('inf'))
        return child, column, utility,i

    def work(self, state):
        self.update(state)
        newState, column, utility,i = self.decision()
        self.tree.append((i,state, 0, column, utility, 'maxgate'))
        self.tree = self.create_tree()
        return newState, column

from graphviz import Digraph

class Tree:
    def __init__(self, states, num_col, num_row):
        self.graph = Digraph()
        self.states = states
        self.png_name = 'states_tree'
        self.extension = 'png'
        self.num_col = num_col
        self.num_row = num_row
        self.adjust_states()
        self.create_tree()
        self.save_tree()

    def adjust_states(self):
        for i in range(len(self.states)):
            self.states[i] = list(self.states[i])
            temp = self.num_col -1
            for j in range(self.num_row):
                self.states[i][temp] += '\n'
                temp += self.num_col
            self.states[i] = "".join(self.states[i])
            # print(self.states[i])
            # print()


    def create_tree(self):
        states_len = len(self.states)
        self.graph.attr('node', shape='box', fontsize="10")#, fixedsize='true', width='0.9')
        # print(states_len)
        for i in range(states_len):
            if i+1 < states_len:
                
                self.graph.edge(str(self.states[i]),str(self.states[i+1]))


    # def create_tree(self):
    #     states_len = len(self.states)
    #     self.graph.attr('node', shape='box')
    #     # print(states_len)
    #     for i in range(states_len):
    #         for j in range(len(self.states[i][1])):
    #             # print(states[i][1][j])
    #             self.graph.edge(str(self.states[i][0]),str(self.states[i][1][j]))#,len='1.00')
    #         if i+1 < states_len:
    #             # print(i)
    #             self.graph.edge(str(self.states[i][0]),str(self.states[i+1][0]))#,len='1.00')

    

    def save_tree(self):
        self.graph.format = self.extension
        tree = self.graph.unflatten(stagger = 3)
        tree.render(self.png_name)

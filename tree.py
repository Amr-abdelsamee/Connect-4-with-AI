from graphviz import Digraph

class Tree:
    def __init__(self, tree, num_col, num_row):
        self.graph = Digraph()
        self.tree = tree
        self.png_name = 'states_tree'
        self.extension = 'png'
        self.num_col = num_col
        self.num_row = num_row
        self.create_tree()
        self.save_tree()


    def create_tree(self):
        tree_len = len(self.tree)
        self.graph.attr('node', shape='box')
        for i in range(tree_len):
            self.graph.node(str(self.tree[i][0]), str(self.tree[i][0][5]) +'\n'+ str(self.tree[i][0][4]) +'\n'+ str(self.tree[i][0][3]))
            for j in range(len(self.tree[i][1])):
                self.graph.node(str(self.tree[i][1][j]), str(self.tree[i][1][j][5]) +'\n'+ str(self.tree[i][1][j][4]) +'\n'+ str(self.tree[i][1][j][3]))
                self.graph.edge(str(self.tree[i][0]), str(self.tree[i][1][j]))

    def save_tree(self):
        self.graph.format = self.extension
        tree = self.graph.unflatten(stagger = 3)
        tree.render(self.png_name)

from graphviz import Digraph
from random import randint

class Node:
    def __init__(self, ntype, *args):
        self.type = ntype
        self.args = args

def print_ast(node: Node, depth=0):
    print(f'{"  " * depth}type: {node.type}')
    for arg in node.args:
        if isinstance(arg, Node):
            print_ast(arg, depth + 1)
        else:
            print(f'{"  " * depth}arg: {arg}')

def render_ast(node: Node):
    dot = Digraph(comment='Abstract Syntax Tree')
    _render_ast(node, dot)

    dot.render(view=True)

def _render_ast(node: Node, dot: Digraph):
    node_ident = f'{node.type}{randint(0,1000000)}'
    dot.node(node_ident, f'{node.type} - {",".join(map(lambda x: str(x), filter(lambda n: not isinstance(n, Node), node.args)))}')

    for arg in node.args:
        if isinstance(arg, Node):
           dot.edge(node_ident, _render_ast(arg, dot))


    return node_ident
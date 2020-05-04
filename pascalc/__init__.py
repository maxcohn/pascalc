__version__ = '0.1.0'
from . import lexer
from . import parser
from .ast import *
import sys

def main():
    lex = lexer.PLex()
    parse = parser.PParser()
    '''
    n=Node('asd',
        Node('zxc'),
        Node('shit',
            Node('fuck')
        ),
        Node('foo', 'asdaaaa', 'asdasd')
    )
    print_ast(n)
    '''
    all_source = ''
    with open(sys.argv[1], 'r') as f:
        all_source = ''.join(f.readlines()) 

    ast = parse.parse(lex.tokenize(all_source))
    print_ast(ast)
    render_ast(ast)
    
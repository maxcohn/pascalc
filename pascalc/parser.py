from sly import Parser
from . import lexer
from .ast import Node

class PParser(Parser):
    tokens = lexer.PLex.tokens
    
    @_('expression_list')
    def program(self, p):
        return p[0]
    '''
    @_('variable ASSIGNOP expression')
    def statement(self, p):
        return Node('assign_statement', p.variable, p.expression)
    
    @_('procedure_statement')
    def statement(self, p):
        #TODO: maybe just return p.procedure_statement ???
        return Node('prodcedure_statement_statement', p.procedure_statement)

    @_('compound_statement')
    def statement(self, p):
        #TODO: maybe just return p.compound_statement ???
        return Node('compound_statement_statement', p.compound_statement)

    @_('IF expression THEN statement ELSE statement')
    def statement(self, p):
        #TODO: make else optional?
        return Node('if_statement', p.expression, p.statement[0], p.statement[1])
    
    @_('WHILE expression DO statement')
    def statement(self, p):
        return Node('while_statement', p.expression, p.statement)

    @_('ID')
    def variable(self, p):
        return Node('variable', p.ID)

    @_('ID "[" expression "]"')
    def variable(self, p):
        return Node('variable_array', p.ID, p.expression)

    @_('ID "(" expression_list ")"')
    def procedure_statement(self, p):
        return Node('procedure_statement_args', p.ID, p.expression_list)

    @_('ID')
    def procedure_statement(self, p):
        return Node('procedure_statement', p.ID)
    '''
    @_( '"="',
        'NOTEQUAL',
        '"<"',
        'LTEQ',
        '">"',
        "GTEQ")
    def relop(self, p):
        return Node('relop', p[0])

    @_( '"*"',
        '"/"',
        'MOD',
        'DIV',
        'AND')
    def mulop(self, p):
        return Node('mulop', p[0])

    @_( '"+"',
        '"-"',
        'OR')
    def addop(self, p):
        return Node('addop', p[0])

    @_( '"-"',
        '"+"')
    def sign(self, p):
        return Node('sign', p[0])

    @_('expression { "," expression }')
    def expression_list(self, p):
        return Node('expression_list', p[0], *p[1])

    @_('simple_expression')
    def expression(self, p):
        return Node('simple_expression', p.simple_expression)

    @_('simple_expression relop simple_expression')
    def expression(self, p):
        return Node('relop', p.simple_expression, p.relop, p.simple_expression)

    @_('term')
    def simple_expression(self, p):
        return Node('term', p.term)

    @_('sign term')
    def simple_expression(self, p):
        return Node('sign', p.sign, p.term)

    @_('simple_expression addop term')
    def simple_expression(self, p):
        return Node('addop', p.simple_expression, p.addop, p.term)

    @_('factor')
    def term(self, p):
        return Node('factor', p.factor)

    @_('term mulop factor')
    def term(self, p):
        return Node('mulop', p.term, p.mulop, p.factor)

    @_('ID')
    def factor(self, p):
        return Node('variable_expr', p.ID)
        #return ('factor', 'variable', p.ID)

    @_('ID "(" expression_list ")"')
    def factor(self, p):
        return Node('func_call', p.ID, p.expression_list)
        #return ('factor', 'func_call', p.ID, p.expression_list)

    @_('NUM')
    def factor(self, p):
        return Node('num', int(p.NUM))

    @_('"(" expression ")"')
    def factor(self, p):
        return Node('expression', p.expression)
        #return ('factor', p.expression_list)

    @_('NOT factor')
    def factor(self, p):
        return Node('not', p.factor)
        #return ('factor', 'not', p.factor)


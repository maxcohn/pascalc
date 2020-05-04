from sly import Parser
from . import lexer
from .ast import Node

class PParser(Parser):
    tokens = lexer.PLex.tokens
    
    @_('PROGRAM ID "(" identifier_list ")" ";" declarations subprogram_declarations compound_statement "."')
    def program(self, p):
        return Node('program', p.ID, p.identifier_list, p.declarations, p.subprogram_declarations, p.compound_statement)

    @_('ID { "," ID }')
    def identifier_list(self, p):
        return Node('identifier_list', p.ID0, *p.ID1)


    @_('VAR identifier_list ":" ptype ";"')
    def declaration(self, p):
        return Node('declaration', p.identifier_list, p.ptype)

    @_('{ declaration }')
    def declarations(self, p):
        #TODO: maybe turn into list of declarations instead of multiple args?
        return Node('declarations', *p.declaration)

    @_('ARRAY "[" NUM RANGE NUM "]" OF standard_type')
    def ptype(self, p):
        #TODO: change node name?
        return Node('type_array', int(p.NUM0), int(p.NUM1), p.standard_type)
    
    @_('standard_type')
    def ptype(self, p):
        return Node('type', p.standard_type)

    @_( 'INTEGER',
        'REAL')
    def standard_type(self, p):
        #TODO: just propogate str?
        return Node('standard_type', p[0])

    @_('{ subprogram_declaration } ";"')
    def subprogram_declarations(self, p):
        #TODO: maybe turn into list of subpriograms instead of multiple args?
        return Node('subprogram_declarations', *p.subprogram_declaration)

    @_('subprogram_head declarations compound_statement')
    def subprogram_declaration(self, p):
        return Node('subprogram_declaration', p.subprogram_head, p.declarations, p.compound_statement)

    @_('FUNCTION ID arguments ":" standard_type ";"')
    def subprogram_head(self, p):
        return Node('function_head', p.ID, p.arguments, p.standard_type)

    @_('PROCEDURE ID arguments ";"')
    def subprogram_head(self, p):
        #TODO: can probably make the same and propogate the fact that one is a function and one is a procedure
        return Node('procedure_head', p.ID, p.arguments)

    @_('')
    def arguments(self, p):
        return Node('arguments')

    @_('"(" parameter_list ")"')
    def arguments(self, p):
        return Node('arguments', p.parameter_list)

    @_('parameter_list ";" identifier_list ":" ptype')
    def parameter_list(self, p):
        return Node('parameter_list', p.identifier_list, p.ptype)
    
    @_('identifier_list ":" ptype')
    def parameter_list(self, p):
        return Node('parameter_list', p.identifier_list, p.ptype)

    @_('BEGIN optional_statements END')
    def compound_statement(self, p):
        #TODO: might be able to just propogate isntead. Related to statement
        return Node('compound_statement', p.optional_statements)

    @_('statement_list')
    def optional_statements(self, p):
        #TODO: miht have to make a new node instead of propogating. Related to statement
        return p.statement_list

    @_('')
    def optional_statements(self, p):
        return Node('statement_list')

    @_('statement { ";" statement }')
    def statement_list(self, p):
        return Node('statement_list', p.statement0, *p.statement1)
    
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
        return Node('if_statement', p.expression, p.statement0, p.statement1)
    
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
        return Node('expression_list', p.expression0, *p.expression1)

    @_('simple_expression')
    def expression(self, p):
        return Node('simple_expression', p.simple_expression)

    @_('simple_expression relop simple_expression')
    def expression(self, p):
        return Node('relop', p.simple_expression0, p.relop, p.simple_expression1)

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


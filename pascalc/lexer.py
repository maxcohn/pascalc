from sly import Lexer


class PLex(Lexer):
    tokens = {
        ID, NUM, RELOP, ADDOP, MULOP, ASSIGNOP, PROGRAM, VAR, ARRAY, INTEGER,
        REAL, FUNCTION, PROCEDURE, BEGIN, END, IF, THEN, ELSE, WHILE, DO, NOT,
        MOD, AND, OR, DIV, NOTEQUAL, LTEQ, GTEQ, RANGE, OF
    }

    literals = {';', ':', '[', ']', '(', ')', '.', ',', '-', '+', '=', '<', '>', '*', '/'}

    ignore = ' \t\n'

    ID = r'[_a-zA-Z]\w*'
    NUM = r'\d+(\.\d+)?([Ee][-+]?\d+)?'
    NOTEQUAL = r'<>'
    LTEQ = r'<='
    GTEQ = r'>='
    RANGE = r'\.\.'
    ASSIGNOP = r':='

    ID['program'] = PROGRAM
    ID['var'] = VAR
    ID['array'] = ARRAY
    ID['OF'] = OF
    ID['integer'] = INTEGER
    ID['real'] = REAL
    ID['function'] = FUNCTION
    ID['procedure'] = PROCEDURE
    ID['begin'] = BEGIN
    ID['end'] = END
    ID['if'] = IF
    ID['then'] = THEN
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['do'] = DO
    ID['not'] = NOT
    ID['mod'] = MOD
    ID['or'] = OR
    ID['div'] = DIV
    ID['and'] = AND


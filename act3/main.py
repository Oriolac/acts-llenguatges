from ply import lex, yacc
from generator.stable import *

class Parser:

    def __init__(self):
        self.lex = lex.lex(module=self)
        self.yacc = yacc.yacc(module=self)
        self.num_line = 1

    identificadors = ('IDENTIFIER',)
    constants = ('INTEGER', 'FLOAT', 'BOOLEAN')
    op_arit = ( 'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD', 'POW')
    op_logics = ('AND', 'OR', 'XOR')
    op_relacionals = ('NOT', 'EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE')
    reserved = ('IF', 'ELSE', 'WHILE')
    tokens = identificadors + constants + op_arit + op_logics + op_relacionals + reserved

    literals = (';', '=', '(', ')', '{', '}')

    t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

    t_INTEGER = r'\d+'
    t_FLOAT = r'\d+\.\d*'
    t_BOOLEAN = r'(True|False)'
    
    t_SUMA = r'\+'
    t_RESTA = r'-'
    t_MULT = r'\*'
    t_DIV = r'\/'
    t_MOD = r'%'
    t_POW = r'\*\*'
    
    t_AND = r'and'
    t_OR = r'or'
    t_XOR = r'xor'
    t_NOT = r'(not|\!)'
    t_EQ = r'=='
    t_NEQ = r'!='
    t_GT = r'>'
    t_LT = r'<'
    t_GE = r'>='
    t_LE = r'<='
    t_IF = r'if'
    t_ELSE = r'else'
    t_WHILE = r'while'
    t_ignore = ' \t'

    precedence = (
        ('right', 'XOR'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'GT', 'LT', 'GE', 'LE'),
        ('left', 'EQ', 'NEQ'),
        ('right', 'NOT'),
        ('left', 'SUMA', 'RESTA'),
        ('left', 'MULT', 'DIV', 'MOD'),
        ('left', 'POW'),
        ('right', 'USUMA', 'URESTA'),
    )

    def p_programa(self, p):
        """
        programa :  programa sentence
                    | empty
        """
        pass

    def p_sentence(self, p):
        """
        sentence :  empty ';'
                    | asig ';'
        """
        self.num_line += 1
    
    def p_empty(self, p):
        """empty :"""
        pass
    
    def p_asig(self, p):
        """
        asig : IDENTIFIER '=' expr
        """
        print(f'{p[1]} = {p[3]};')

    def p_expr_int_suma(self, p):
        """
        expr : expr SUMA expr
        """
        tmp = self.add_variable()
        print(f'{tmp} = {p[1]} SUMA {p[3]}')
        p[0] = tmp

    def p_expr_int_const(self, p):
        """
        expr : INTEGER
        """
        p[0] = p[1]

    def p_expr_int_uresta(self, p):
        """
        expr :  RESTA expr  %prec URESTA
        """
        tmp = self.add_variable()
        print(f'{tmp} = URESTA {p[2]}')
        p[0] = f"{tmp}"

    def p_expr_int_usuma(self, p):
        """
        expr : SUMA expr %prec USUMA
        """
        p[0] = f"{p[2]}"

    def add_variable(self):
        return "tmp"

    def run(self):
        while True:
            try:
                s = input()
            except EOFError:
                break
            if not s:
                continue
            yacc.parse(s)

Parser().run()
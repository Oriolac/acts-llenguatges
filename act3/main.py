from ply import lex, yacc
from generator.stable import *
import generator.tokens as tok 

class Parser:

    def __init__(self):
        self.lex = lex.lex(module=self)
        self.yacc = yacc.yacc(module=self)
        self.num_line = 1

    identificadors = ('IDENTIFIER')
    constants = ('INTEGER', 'FLOAT', 'BOOLEAN')
    op_arit = ( 'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD', 'POW')
    op_logics = ('AND', 'OR', 'XOR')
    op_relacionals = ('NOT', 'EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE')
    tokens = identificadors + constants + op_arit + op_logics + op_relacionals

    literals = (';', '=', '(', ')')

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
    
    t_AND = r'\&'
    t_OR = r'\|'
    t_XOR = r'\^'
    t_NOT = r'!'
    t_EQ = r'=='
    t_NEQ = r'!='
    t_GT = r'>'
    t_LT = r'<'
    t_GE = r'>='
    t_LE = r'<='

    t_ignore = ' \t\n'
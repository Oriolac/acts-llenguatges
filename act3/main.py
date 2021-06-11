from ply import lex, yacc
from computils.stable import *
from computils.expr import Expr, Type, Boolean, Integer, Float, Char

class Parser:

    identificadors = ('IDENTIFIER',)
    constants = ('INTEGER', 'FLOAT', 'BOOLEAN', 'CHAR')
    op_arit = ( 'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD', 'POW')
    op_logics = ('AND', 'OR', 'XOR')
    op_relacionals = ('NOT', 'EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE')
    reserved = ('IF', 'ELSE', 'WHILE')
    tokens = identificadors + constants + op_arit + op_logics + op_relacionals + reserved

    def __init__(self):
        self.lex = lex.lex(module=self)
        self.yacc = yacc.yacc(module=self)
        self.num_line = 1
        self.root_table: SymbolTable = SymbolTable(None, 'global')
        self.dict_ops_arit = dict(zip(['+', '-', '*', '/', '%', '**'], self.op_arit))
        self.current_table: SymbolTable = self.root_table

    literals = (';', '=', '(', ')', '{', '}')

    t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

    t_INTEGER = r'\d+'
    t_FLOAT = r'\d+\.\d*'
    t_BOOLEAN = r'(True|False)'
    t_CHAR = r'\'.\''
    
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
        self.current_table.put(VariableSymbol(p[1], p[3].tipus))
        print(f'{p[1]} = {p[3].value};')


    def p_expr_op(self, p):
        """
        expr :   expr SUMA expr
                    | expr RESTA expr
                    | expr MULT expr
                    | expr DIV expr
                    | expr MOD expr
                    | expr POW expr
        """
        tmp = self.add_variable(Integer())
        print(f'{tmp} = {p[1].value} {self.dict_ops_arit[p[2]]} {p[3].value};')
        p[0] = Expr(Integer(), tmp)

    def p_expr_const(self, p):
        """
        expr :   INTEGER 
        """
        p[0] = Expr(Integer(), p[1])

    def p_expr_ident(self, p):
        """
        expr : IDENTIFIER
        """
        var = self.current_table.get(p[1])
        if var:
            p[0] = Expr(Integer(), p[1])
        else:
            raise Exception(f"lineno {self.num_line}: {p[1]} not found.")

    def p_expr_uresta(self, p):
        """
        expr :  RESTA expr  %prec URESTA
        """
        tmp = self.add_variable(Integer())
        print(f'{tmp} = URESTA {p[2]};')
        p[0] = f"{tmp}"

    def p_intexpr_usuma(self, p):
        """
        expr : SUMA expr %prec USUMA
        """
        tmp = self.add_variable(Integer())
        print(f'{tmp} = USUMA {p[2]};')
        p[0] = f"{tmp}"

    def add_variable(self, tipus: Type):
        name = "tmp" + f"{self.current_table.length()}"
        if not self.current_table.put(VariableSymbol(name, tipus)) :
            raise Exception("State unreachable.")
        return name

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
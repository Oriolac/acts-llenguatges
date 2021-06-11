from ply import lex, yacc
from generator.stable import *

class Parser:

    def __init__(self):
        self.lex = lex.lex(module=self)
        self.yacc = yacc.yacc(module=self)
        self.num_line = 1
        self.parent_table = SymbolTable(None, 'global')

    identificadors = ('IDENTIFIER',)
    constants = ('INTEGER', 'FLOAT', 'BOOLEAN', 'CHAR')
    op_arit = ( 'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD', 'POW')
    op_logics = ('AND', 'OR', 'XOR')
    op_relacionals = ('NOT', 'EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE')
    reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'funk' : 'FUNCTION',
    'return' : 'RETURN',
    'int': 'INT_TYPE',
    'float' : 'FLOAT_TYPE',
    'char' : 'CHAR_TYPE',
    'bool' : 'BOOL_TYPE',
    'true' : 'TRUE',
    'false' : 'FALSE'
    } 

    tokens = identificadors + constants + op_arit + op_logics + op_relacionals + tuple(reserved.values())

    literals = (';', '=', '(', ')', '{', '}', ',', ':')

    
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        reserved = {
        'if' : 'IF',
        'else' : 'ELSE',
        'while' : 'WHILE',
        'funk' : 'FUNCTION',
        'retrunk' : 'RETURN',
        'int': 'INT_TYPE',
        'float' : 'FLOAT_TYPE',
        'char' : 'CHAR_TYPE',
        'bool' : 'BOOL_TYPE',
        'true' : 'TRUE',
        'false' : 'FALSE'
        } 
        t.type = reserved.get(t.value,'IDENTIFIER')
        return t

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
    
    t_ignore = ' \t\n'

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
        print("program")
        pass

    def p_sentence(self, p):
        """
        sentence :  empty ';'
                    | asig ';'
                    | funk
        """
        print("sentence")
        self.num_line += 1
    

    def p_funk(self, p):
        """
        funk : FUNCTION returntype IDENTIFIER '(' paramsdef ')' '{' sentences '}'
        """
        print("funk")
        pass

    def p_returntype(self, p):
        """
        returntype : INT_TYPE
                      | FLOAT_TYPE
                      | BOOL_TYPE
                      | CHAR_TYPE
        """
        

    def p_paramsdef(self, p):
        """
        paramsdef : paramdef ',' paramsdef
                 | paramdef
        """

    def p_paramdef(self, p):
        """
        paramdef : INT_TYPE ':' IDENTIFIER
                | FLOAT_TYPE ':' IDENTIFIER
                | CHAR_TYPE ':' IDENTIFIER
                | BOOL_TYPE ':' IDENTIFIER
                | empty
        """

    def p_sentences(self, p):
        """
        sentences : sentence sentences
                   | RETURN sentence
                   | empty
        """

    def p_empty(self, p):
        """empty :"""
        pass
    
    def p_asig(self, p):
        """
        asig : IDENTIFIER '=' expr
               | IDENTIFIER '=' funkcall
        """
        print(f'{p[1]} = {p[3]};')

    def p_funkcall(self, p):
        """
        funkcall : IDENTIFIER '(' paramscall ')' 
        """

    def p_paramscall(self, p):
        """
        paramscall : paramcall ',' paramscall
                    | paramcall
        """

    def p_paramcall(self, p):
        """
        paramcall : IDENTIFIER
                    | INTEGER
                    | FLOAT
                    | BOOLEAN
                    | CHAR
                    | empty
        """

    def p_expr(self, p):
        """
        expr : intexpr 
        """
        p[0] = p[1]

    def p_intexpr_suma(self, p):
        """
        intexpr : intexpr SUMA intexpr
        """
        tmp = self.add_variable()
        print(f'{tmp} = {p[1]} SUMA {p[3]};')
        p[0] = tmp

    def p_intexpr_const(self, p):
        """
        intexpr : INTEGER
        """
        p[0] = p[1]

    def p_intexpr_uresta(self, p):
        """
        intexpr :  RESTA intexpr  %prec URESTA
        """
        tmp = self.add_variable()
        print(f'{tmp} = URESTA {p[2]};')
        p[0] = f"{tmp}"

    def p_intexpr_usuma(self, p):
        """
        intexpr : SUMA intexpr %prec USUMA
        """
        tmp = self.add_variable()
        print(f'{tmp} = USUMA {p[2]};')
        p[0] = f"{tmp}"

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
            yacc.parse(s, debug=1)

Parser().run()
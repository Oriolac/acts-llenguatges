from ply import lex, yacc
import sys
from computils.stable import *
from computils.expr import Expr, Type, Boolean, Integer, Float, Char
from computils.exceptions import CompileException

class Parser:

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

    def __init__(self):
        self.lex = lex.lex(module=self)
        self.yacc = yacc.yacc(module=self)
        self.num_line = 1
        self.root_table: SymbolTable = SymbolTable(None, 'global')
        self.dict_ops_arit = dict(zip(['+', '-', '*', '/', '%', '**'], self.op_arit))
        self.current_table: SymbolTable = self.root_table

<<<<<<< HEAD
    literals = (';', '=', '(', ')', '{', '}', ',', ':')
=======
    
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
>>>>>>> c554fe045551d6419b1e5476148a37d90c64fc94

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
        pass

    def p_sentence(self, p):
        """
        sentence :  empty ';'
                    | asig ';'
                    | funk
        """
        self.num_line += 1
    

    def p_funk(self, p):
        """
        funk : FUNCTION returntype IDENTIFIER '(' paramsdef ')' '{' sentences '}'
        """
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
        self.current_table.put(VariableSymbol(p[1], p[3].tipus))
        print(f'{p[1]} = {p[3].value};')


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

    def p_expr_op(self, p):
        """
        expr :   expr SUMA expr
                    | expr RESTA expr
                    | expr MULT expr
                    | expr DIV expr
                    | expr MOD expr
                    | expr POW expr
        """
        if (p[1].tipus == p[3].tipus):
            tmp = self.add_variable(p[1].tipus)
        elif (isinstance(p[1].tipus, (Float, Integer)) and isinstance(p[3].tipus, (Float, Integer))):
            tmp = self.add_variable(Float())
        else:
            raise CompileException(self, f"Not supported types for operating the operation {p[2]}")
        tmp = self.add_variable(Integer())
        print(f'{tmp} = {p[1].value} {self.dict_ops_arit[p[2]]} {p[3].value};')
        p[0] = Expr(Integer(), tmp)

    def p_expr_const_int(self, p):
        """
        expr :   INTEGER 
        """
        p[0] = Expr(Integer(), p[1])


    def p_expr_const_float(self, p):
        """
        expr :   FLOAT
        """
        p[0] = Expr(Float(), p[1])

    def p_expr_const_char(self, p):
        """
        expr :   CHAR
        """
        p[0] = Expr(Char(), p[1])

    def p_expr_const_boolean(self, p):
        """
        expr :   BOOLEAN
        """
        p[0] = Expr(Boolean(), p[1])

    def p_expr_ident(self, p):
        """
        expr : IDENTIFIER
        """
        var = self.current_table.get(p[1])
        if var:
            p[0] = Expr(var.type, p[1])
        else:
            raise CompileException(self, f"{p[1]} not found.")

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
            raise CompileException(self, "State unreachable.")
        return name

    def run(self):
        while True:
            try:
                s = input()
            except EOFError:
                break
            if not s:
                continue
            try:
                yacc.parse(s, debug=0)
            except CompileException as e:
                print(e.get_msg());
                sys.exit();

Parser().run()
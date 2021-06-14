import re
from ply import lex, yacc
import sys
from computils.stable import *
from computils.expr import Expr, Type, Boolean, Integer, Float, Char
from computils.exceptions import CompileException

class Parser:

    identificadors = ('IDENTIFIER',)
    constants = ('INTEGER_VALUE', 'FLOAT_VALUE', 'BOOL_VALUE', 'CHAR_VALUE')
    op_arit = ( 'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD', 'POW')
    op_logics = ('AND', 'OR', 'XOR')
    op_relacionals = ('NOT', 'EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE')
    reserved = ('IF', 'ELSE', 'WHILE', 'FUNCTION', 'RETURN', 'INT_TYPE', 'FLOAT_TYPE', 'CHAR_TYPE', 'BOOL_TYPE')
    tokens = identificadors + constants + op_arit + op_logics + op_relacionals + reserved
    literals = (';', '=', '(', ')', '{', '}', ',', ':')

    def __init__(self):
        self.lex = lex.lex(module=self)
        self.yacc = yacc.yacc(module=self)
        self.num_line = 1
        self.root_table: SymbolTable = SymbolTable(None, 'global')
        self.dict_ops_arit = dict(zip(['+', '-', '*', '/', '%', '**'], self.op_arit))
        self.current_table: SymbolTable = self.root_table
        self.dict_types = {'int': Integer(), 'float': Float(), 'char': Char(), 'bool': Boolean()}

    t_INTEGER_VALUE = r'\d+'
    t_FLOAT_VALUE = r'\d+\.\d*'
    t_BOOL_VALUE = r'(True|False)'
    t_CHAR_VALUE = r'\'.\''
    
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
    t_FUNCTION = r'funk'
    t_RETURN = r'retrunk'
    t_INT_TYPE = r'int'
    t_FLOAT_TYPE = r'float'
    t_CHAR_TYPE = r'char'
    t_BOOL_TYPE = r'bool'

    reserved = {
        t_IF : 'IF',
        t_ELSE : 'ELSE',
        t_WHILE : 'WHILE',
        t_FUNCTION : 'FUNCTION',
        t_RETURN : 'RETURN',
        t_INT_TYPE : 'INT_TYPE',
        t_FLOAT_TYPE : 'FLOAT_TYPE',
        t_CHAR_TYPE : 'CHAR_TYPE',
        t_BOOL_TYPE : 'BOOL_TYPE',
        t_BOOL_VALUE : 'BOOL_VALUE',
    } 
    
    
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        matches = list(filter(lambda x: re.match(x, t.value), self.reserved.keys()))
        t.type = 'IDENTIFIER' if not matches else self.reserved.get(matches[0], 'IDENTIFIER')
        return t

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
        funk : heading '(' middlefunk ')' footing
        """
        self.current_table.put(FunctionSymbol(p[1][1], p[1][0], p[3]))
        p[0] = p[1:]

    def p_funk_empy(self, p):
        """
        funk : heading '(' ')' footing
        """
        self.current_table.put(FunctionSymbol(p[1][1], p[1][0], []))

    def p_middlefunk(self, p):
        """
        middlefunk : paramsdef
        """
        for i, param in enumerate(p[1]):
            print(f'{self.current_table.tabulation()}{param[0]}:= param', i+1)
        p[0] = p[1]

    def p_heading(self, p):
        """
        heading : FUNCTION typename IDENTIFIER
        """
        print(f'{self.current_table.tabulation()}{self.t_FUNCTION} {p[3]}:')
        self.current_table = SymbolTable(self.current_table, p[3])
        p[0] = p[2], p[3]
        
    def p_footing(self, p):
        """
        footing : '{' bodyfunk '}'
        """
        self.current_table = self.current_table.parent

    def p_typename(self, p):
        """
        typename : INT_TYPE
                      | FLOAT_TYPE
                      | BOOL_TYPE
                      | CHAR_TYPE
        """ 
        p[0] = p[1]

    def p_paramsdef(self, p):
        """
        paramsdef : paramdef ',' paramsdef
                 | paramdef
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]
            
    
    def p_paramdef(self, p):
        """
        paramdef : typename ':' IDENTIFIER
        """
        self.current_table.put(VariableSymbol(p[3], self.dict_types[p[1]]))
        p[0] = (p[3] , p[1])
   
   
    def p_bodyfunk(self, p):
        """
        bodyfunk : bodysentence bodyfunk
                   | RETURN returnsentence
        """
        

    def p_bodysentence(self, p):
        """
        bodysentence : tabreturn sentence
        """

    def p_returnsentence(self, p):
        """
        returnsentence : tabreturn expr ';'
        """
        print(f'{self.current_table.tabulation()}{self.t_RETURN} {p[2].value};')

    def p_tabreturn(self, p):
        """
        tabreturn : empty
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
        print(f'{self.current_table.tabulation()}{p[1]} = {p[3].value};')
        p[0] = p[1:]


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
                    | INTEGER_VALUE
                    | FLOAT_VALUE
                    | BOOL_VALUE
                    | CHAR_VALUE
        """

        # comrprovar tipus de params amb simbols de la taula

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
        print(f'{self.current_table.tabulation()}{tmp} = {p[1].value} {self.dict_ops_arit[p[2]]} {p[3].value};')
        p[0] = Expr(Integer(), tmp)
        

    def p_expr_const_int(self, p):
        """
        expr :   INTEGER_VALUE
        """
        p[0] = Expr(Integer(), p[1])


    def p_expr_const_float(self, p):
        """
        expr :   FLOAT_VALUE
        """
        p[0] = Expr(Float(), p[1])

    def p_expr_const_char(self, p):
        """
        expr :   CHAR_VALUE
        """
        p[0] = Expr(Char(), p[1])

    def p_expr_const_boolean(self, p):
        """
        expr :   BOOL_VALUE
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
        with open(sys.argv[1]) as f:
            input = f.read()
        yacc.parse(input)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"usage: python main.py <file>")
        sys.exit()
    Parser().run()
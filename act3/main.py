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
    reserved = ('IF', 'ELSE', 'ELIF', 'WHILE', 'FUNCTION', 'RETURN', 'INT_TYPE', 'FLOAT_TYPE', 'CHAR_TYPE', 'BOOL_TYPE')
    tokens = identificadors + constants + op_arit + op_logics + op_relacionals + reserved
    literals = (';', '=', '(', ')', '{', '}', ',', ':')

    def __init__(self):
        self.lex = lex.lex(module=self)
        self.yacc = yacc.yacc(module=self)
        self.num_line = 1
        self.root_table: SymbolTable = SymbolTable(None, '')
        self.dict_ops_arit = dict(zip(['+', '-', '*', '/', '%', '**'], self.op_arit))
        self.dict_ops_bool = dict(zip(['and', 'or', 'xor'], self.op_logics))
        self.dict_ops_rel = dict(zip([self.t_NOT, self.t_EQ, self.t_NEQ, self.t_GT, self.t_LT, self.t_GE, self.t_LE], self.op_relacionals))
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
    t_ELIF = r'elif'
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
        t_ELIF : 'ELIF',
        t_WHILE : 'WHILE',
        t_FUNCTION : 'FUNCTION',
        t_RETURN : 'RETURN',
        t_INT_TYPE : 'INT_TYPE',
        t_FLOAT_TYPE : 'FLOAT_TYPE',
        t_CHAR_TYPE : 'CHAR_TYPE',
        t_BOOL_TYPE : 'BOOL_TYPE',
        t_BOOL_VALUE : 'BOOL_VALUE',
    } 
    
    def t_error(self, t):
        print(f"No sha reconegut token en la línea: {self.num_line}")
        t.lexer.skip(1)
    
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
                    | cond
        """
        self.num_line += 1
    
    def p_cond(self, p):
        """
        cond : headCond '{' bodyCond '}' footCond
        """
        print("AA")

    def p_headCond(self, p):
        """
        headCond : IF boolExpr
        """

    def p_boolExpr(self, p):
        """
        boolExpr : expr
        """

    def p_bodyCond(self, p):
        """
        bodyCond :  sentence bodyCond
                    | empty
        """

    def p_footCond(self, p):
        """
        footCond :  ELIF boolExpr '{' bodyCond '}' footCond
                    | ELSE '{' '}'
                    | empty
        """

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
        middlefunk : listfunkparams
        """
        for i, param in enumerate(p[1]):
            print(f'{self.current_table.tabulation()}{param[0]} = param', i+1)
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

    def p_listfunkparams(self, p):
        """
        listfunkparams : funkparam ',' listfunkparams
                 | funkparam
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]
            
    
    def p_funkparam(self, p):
        """
        funkparam : typename ':' IDENTIFIER
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
        bodysentence : sentence
        """

    def p_returnsentence(self, p):
        """
        returnsentence : expr ';'
        """
        print(f'{self.current_table.tabulation()}{self.t_RETURN} {p[1].value};')

    def p_empty(self, p):
        """empty :"""
        pass
    
    def p_asig(self, p):
        """
        asig : IDENTIFIER '=' expr
        """
        self.current_table.put(VariableSymbol(p[1], p[3].tipus))
        print(f'{self.current_table.tabulation()}{p[1]} = {p[3].value};')
        p[0] = p[1:]



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

    def p_expr_funkcall(self, p):
        """
        expr : IDENTIFIER '(' paramscall ')' 
        """
        p[0] = Expr(Integer(), p[1])

    def p_expr(self, p):
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
    
    

    def p_expr_boolop(self, p):
        """
        expr :  expr AND expr
                | expr OR expr
                | expr XOR expr
        """
        if isinstance(p[1].tipus, Boolean) and p[1].tipus != p[3].tipus:
            raise CompileException(self, f"Not supported types for operating the operation {p[2]}")
        tmp = self.add_variable(Boolean())
        print(f'{self.current_table.tabulation()}{tmp} = {p[1].value} {self.dict_ops_bool[p[2]]} {p[3].value};')
        p[0] = Expr(Boolean(), tmp)

    def p_expr_boolcomparison(self, p):
        """
        expr : expr EQ expr
                | expr NEQ expr
                | expr GT expr
                | expr LT expr
                | expr GE expr
                | expr LE expr
        """
        if p[1].tipus == p[3].tipus or isinstance(p[1].tipus, (Float, Integer)) and isinstance(p[3].tipus, (Float, Integer)):
            tmp = self.add_variable(Boolean())
            print(f'{self.current_table.tabulation()}{tmp} = {p[1].value} {self.dict_ops_rel[p[2]]} {p[3].value};')
            p[0] = Expr(Boolean(), tmp)
        else:
            raise CompileException(self, f"Not supported types for operating the operation {p[2]}")

    def p_expr_bool_not(self, p):
        """
        expr :  NOT expr
        """
        if not isinstance(p[2].tipus, Boolean):
            raise CompileException(self, f"Not supported types for operating the operation {p[0]}")
        p[0] = Expr(Boolean(), p)

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

    def p_expr_const_bool(self, p):
        """
        expr :   BOOL_VALUE
        """
        p[0] = Expr(Boolean(), p[1])

    def p_expr_ident(self, p):
        """
        expr : IDENTIFIER
        """
        var = self.current_table.get(p[1])
        if var and isinstance(var.type, (Float, Integer)):
            p[0] = Expr(var.type, p[1])
        else:
            raise CompileException(self, f"{p[1]} not found.")

    def p_expr_uresta(self, p):
        """
        expr :  RESTA expr  %prec URESTA
        """
        if not isinstance(p[2].tipus, (Float, Integer)):
            raise CompileException(f"RESTA is not allowed for type {p[2].tipus}")
        tmp = self.add_variable(p[2].tipus)
        print(f'{tmp} = URESTA {p[2].value};')
        p[0] = Expr(p[2].tipus, tmp)

    def p_expr_usuma(self, p):
        """
        expr : SUMA expr %prec USUMA
        """
        if not isinstance(p[2].tipus, (Float, Integer)):
            raise CompileException(f"SUMA is not allowed for type {p[2].tipus}")
        tmp = self.add_variable(p[2].tipus)
        print(f'{tmp} = USUMA {p[2].value};')
        p[0] = Expr(p[2].tipus, tmp)

    def add_variable(self, tipus: Type):
        name = "tmp" + f"{self.current_table.length()}"
        if not self.current_table.put(VariableSymbol(name, tipus)) :
            raise CompileException(self, "State unreachable.")
        return name

    def run(self):
        with open(sys.argv[1]) as f:
            input = f.read()
        yacc.parse(input, debug=False)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"usage: python main.py <file>")
        sys.exit()
    Parser().run()
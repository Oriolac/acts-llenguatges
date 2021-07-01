import re
from ply import lex, yacc
import sys
from computils.stable import *
from computils.expr import Expr, Type, Boolean, Integer, Float, Char, List
from computils.exceptions import CompileException
from computils.node import Node

class Parser:

    identificadors = ('IDENTIFIER',)
    constants = ('INTEGER_VALUE', 'FLOAT_VALUE', 'BOOL_VALUE', 'CHAR_VALUE')
    op_arit = ('SUMA', 'RESTA', 'MULT', 'DIV', 'MOD', 'POW')
    op_logics = ('AND', 'OR', 'XOR', 'NOT')
    op_relacionals = ('EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE')
    reserved = ('IF', 'ELSE', 'ELIF', 'WHILE', 'FUNCTION', 'RETURN', 'INT_TYPE',
                'FLOAT_TYPE', 'CHAR_TYPE', 'BOOL_TYPE', 'FOR', 'REPEAT', 'UNTIL')
    tokens = identificadors + constants + op_arit + \
        op_logics + op_relacionals + reserved
    literals = (';', '=', '(', ')', '{', '}', ',', ':', '[', ']')

    def __init__(self):
        self.lex = lex.lex(module=self)
        self.yacc = yacc.yacc(module=self)
        self.num_line = 1
        self.root_table: SymbolTable = SymbolTable(None, '')
        self.dict_ops_arit = dict(
            zip(['+', '-', '*', '/', '%', '**'], self.op_arit))
        self.dict_ops_bool = dict(zip(['and', 'or', 'xor'], self.op_logics))
        self.dict_ops_rel = dict(zip(
            [self.t_EQ, self.t_NEQ, self.t_GT, self.t_LT, self.t_GE, self.t_LE], self.op_relacionals))
        self.current_table: SymbolTable = self.root_table
        self.dict_types = {'int': Integer(), 'float': Float(),
                           'char': Char(), 'bool': Boolean()}
        self.num_cond_label = 0
        self.level_if = 0

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
    t_NOT = r'(not)'
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
    t_FOR = r'for'
    t_REPEAT = r'repeat'
    t_UNTIL = r'until'

    reserved = {
        t_IF: 'IF',
        t_ELSE: 'ELSE',
        t_ELIF: 'ELIF',
        t_WHILE: 'WHILE',
        t_FUNCTION: 'FUNCTION',
        t_RETURN: 'RETURN',
        t_INT_TYPE: 'INT_TYPE',
        t_FLOAT_TYPE: 'FLOAT_TYPE',
        t_CHAR_TYPE: 'CHAR_TYPE',
        t_BOOL_TYPE: 'BOOL_TYPE',
        t_BOOL_VALUE: 'BOOL_VALUE',
        t_AND: 'AND',
        t_OR: 'OR',
        t_XOR: 'XOR',
        t_NOT: 'NOT',
        t_FOR: 'FOR',
        t_REPEAT: 'REPEAT',
        t_UNTIL: 'UNTIL'
    }

    def t_error(self, t):
        print(f"No sha reconegut token en la línea: {self.num_line}")
        t.lexer.skip(1)

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        matches = list(filter(lambda x: re.match(
            x, t.value), self.reserved.keys()))
        t.type = 'IDENTIFIER' if not matches else self.reserved.get(
            matches[0], 'IDENTIFIER')
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

    def p_start(self, p):
        """
        start : programa
        """
        p[1].print()

    def p_programa(self, p):
        """
        programa :  sentence programa
                    | empty
        """
        p[0] = Node(None, p[1], p[2]) if len(p[1:]) == 2 else Node(None, p[1])


    def p_sentence(self, p):
        """
        sentence :  empty ';'
                    | asig ';'
                    | funkdef
                    | cond
                    | loop
                    | repeat
                    | for
        """
        self.num_line += 1
        p[0] = p[1]

    def p_sentence_funkcall(self, p):
        """
        sentence : funkcall
        """
        p[0] = p[1].node

    def p_cond(self, p):
        """
        cond : ifCond elseCond
        """
        p[0] = Node(None, p[1], p[2])

    def p_ifCond(self, p):
        """
        ifCond : headCond '{' bodyCond '}'
        """
        antec = Node(None, p[1][1], p[3])
        node = Node(f"{self.tab()}Label {p[1][0]}:", antec)
        self.level_if += 1
        p[0] = node

    def p_headCond(self, p):
        """
        headCond : IF expr 
        """
        if not isinstance(p[2].tipus, Boolean):
            raise CompileException("The condition is not boolean")
        etiq = self.add_cond_label()
        node = Node(f"{self.tab()}if false {p[2].value} goto {etiq}", p[2].node)
        p[0] = etiq, node

    def p_bodyCond(self, p):
        """ 
        bodyCond :  sentence bodyCond
                    | empty
        """
        node = Node(None, p[1], p[2]) if len(p[1:]) == 2 else Node(None, p[1])
        p[0] = node

    def p_elseCond_else(self, p):
        """
        elseCond :   ELSE '{' bodyCond '}'
        """
        self.level_if -= 1
        p[0] = Node(None, p[3])

    def p_elseCond_noop(self, p):
        """
        elseCond : empty
        """
        p[0] = Node(f"{self.tab()}noop;", p[1])
        self.level_if -= 1

    def p_elifCond(self, p):
        """
        elifCond : ELIF expr
        """
        if not isinstance(p[2].tipus, Boolean):
            raise CompileException(self, "The condition is not boolean")
        etiq = self.add_cond_label()
        node = Node(f"{self.tab()}if false {p[2].value} goto {etiq}", p[2].node)
        p[0] = etiq, node

    def p_headElifCond(self, p):
        """
        headElifCond : elifCond  '{' bodyCond '}'
        """
        antec = Node(None, p[1][1], p[3])
        p[0] = Node(f"{self.tab()}Label {p[1][0]}:", antec)
        self.level_if += 1

    def p_elseCond_elif(self, p):
        """
        elseCond : headElifCond elseCond
        """
        p[0] = Node(None, p[1], p[2])

    def p_for(self, p):
        """
        for : forcond
        """
        self.level_if -= 1
        labeltag = Node(f"{self.tab()}Label {p[1][0]}:")
        self.level_if += 1
        halt = Node(f"{self.tab()}halt")
        self.level_if -= 1
        antec = Node(None, labeltag, halt)
        p[0] = Node(None, p[1][1], antec)

    def p_forcond(self, p):
        """
        forcond : FOR '(' asig ';' checkAssig ';' forasigs ')' '{' forBody '}'
        """
        left = Node(None, p[3], p[5][1])
        right =Node(None, p[10], p[7])
        node = Node(None, left, right)
        p[0] =  p[5][0], node

    def p_forasigs(self, p):
        """
        forasigs : asig forasigs
                    | asig
        """
        p[0] = Node(None, p[1], p[2]) if len(p[1:]) == 2 else Node(None, p[1])

    def p_checkAssig(self, p):
        """
        checkAssig : startLabel condExpr
        """
        etiq = self.add_cond_label()
        antec = Node(None, p[1][1], p[2].node)
        node = Node(f"{self.tab()}if false goto {etiq}", antec)
        p[0] = etiq, node

    def p_startLabel(self, p):
        """
        startLabel : empty
        """
        etiq = self.add_cond_label()
        node = Node(f"{self.tab()}Label {etiq}")
        self.level_if += 1
        p[0] = etiq, node

    def p_forBody(self, p):
        """
        forBody : sentence forBody
                    | empty
        """
        p[0] = Node(None, p[1], p[2]) if len(p[1:]) == 2 else Node(None, p[1])


    def p_repeat(self, p):
        """
        repeat : startRepeat REPEAT '{' repeatBody '}' UNTIL '(' expr ')'
        """
        left = Node(None, p[1][1], p[4])
        right = Node(None, p[8].node)
        antec = Node(None, left, right)
        cond = p[8].value
        tmp = self.add_variable(Boolean())
        first = Node(f"{self.tab()}{tmp} = NOT {cond}")
        second = Node(f"{self.tab()}if false {tmp} go to {p[1][0]}")
        post = Node(None, first, second)
        node = Node(None, antec, post)
        self.level_if -= 1
        p[0] = node

    def p_startRepeat(self, p):
        """
        startRepeat : empty
        """
        etiq = self.add_cond_label()
        node = Node(f"{self.tab()}Label {etiq}:")
        self.level_if += 1
        p[0] = etiq, node

    def p_repeatBody(self, p):
        """
        repeatBody : sentence repeatBody
                    | empty 
        """
        p[0] = Node(None, p[1], p[2]) if len(p[1:]) == 2 else Node(None, p[1])

    def p_loop(self, p):
        """
        loop : headWhile footWhile
        """
        antec = Node(None, p[1][1], p[2])
        first = Node(f"{self.tab()}goto {p[1][0]}")
        self.level_if -= 1
        second = Node(f"{self.tab()}Label {p[1][0]}:")
        self.level_if += 1
        third = Node(f"{self.tab()}halt")
        self.level_if -= 1
        left = Node(None, antec, first)
        right = Node(None, second, third)
        p[0] = Node(None, left, right)

    def p_headWhile(self, p):
        """
        headWhile : addLabelWhile condExpr
        """
        antec = Node(None, p[1][2], p[2].node)
        node = Node(f"{self.tab()}if false {p[2].value} goto {p[1][1]}", antec)
        p[0] = p[1][1], node

    def p_addLabelWhile(self, p):
        """
        addLabelWhile : WHILE
        """
        etiq = self.add_cond_label()
        node = Node(f'{self.tab()}Label {etiq}:')
        self.level_if += 1
        etiqEnd = self.add_cond_label()
        p[0] = etiq, etiqEnd, node

    def p_condExpr(self, p):
        """
        condExpr : expr
        """
        if not isinstance(p[1].tipus, Boolean):
            raise CompileException(self, "Expression must be boolean.")
        p[0] = p[1]

    def p_footWhile(self, p):
        """
        footWhile : '{' bodyWhile '}' 
        """
        p[0] = p[2]

    def p_bodyWhile(self, p):
        """
        bodyWhile : sentence bodyWhile
                    | empty
        """
        p[0] = Node(None, p[1], p[2]) if len(p[1:]) == 2 else Node(None, p[1])

    def p_funkdef(self, p):
        """
        funkdef : heading '(' middlefunk ')' footing
        """
        self.current_table.put(FunctionSymbol(p[1][1], p[1][0], p[3][0]))
        left = Node(None, p[1][2], p[3][1])
        node = Node(None, left, p[5])
        p[0] = node

    def p_funk_empy(self, p):
        """
        funkdef : heading '(' ')' footing
        """
        self.current_table.put(FunctionSymbol(p[1][1], p[1][0], []))
        p[0] = Node(None, p[1][2], p[4])

    def p_middlefunk(self, p):
        """
        middlefunk : listfunkparams
        """
        prec = Node()
        for i, param in enumerate(p[1]):
            prec = Node(f'{self.tab()}{param[0]} = param {i+1}', prec)
        p[0] = p[1], prec

    def p_heading(self, p):
        """
        heading : FUNCTION typename IDENTIFIER
        """
        node = Node(f'{self.tab()}{self.t_FUNCTION} {p[3]}:')
        self.current_table = SymbolTable(self.current_table, p[3])
        p[0] = p[2], p[3], node

    def p_footing(self, p):
        """
        footing : '{' bodyfunk '}'
        """
        self.current_table = self.current_table.parent
        p[0] = p[2]

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
        p[0] = (p[3], p[1])

    def p_bodyfunk(self, p):
        """
        bodyfunk : bodysentence bodyfunk
                   | RETURN returnsentence empty
        """
        p[0] = Node(None, p[1], p[2]) if len(p[1:]) == 2 else Node(None, p[2])


    def p_bodysentence(self, p):
        """
        bodysentence : sentence
        """
        p[0] = p[1]

    def p_returnsentence(self, p):
        """
        returnsentence : expr ';'
        """
        p[0] = Node(f'{self.tab()}{self.t_RETURN} {p[1].value};', p[1].node)

    def p_empty(self, p):
        """
        empty :
        """
        p[0] = Node()

    def p_asig(self, p):
        """
        asig : memoryVariable '=' expr
        """
        self.current_table.put(VariableSymbol(p[1], p[3].tipus))
        node = Node(f'{self.tab()}{p[1]} = {p[3].value};', p[3].node)
        p[0] = node

    def p_memoryVariable_identifier(self, p):
        """
        memoryVariable : IDENTIFIER
        """
        p[0] = p[1]

    def p_paramscall(self, p):
        """
        paramscall : paramcall ',' paramscall
                    | paramcall
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_paramcall(self, p):
        """
        paramcall : expr
        """
        p[0] = p[1]

    def p_funkcall(self, p):
        """
        funkcall : IDENTIFIER '(' paramscall ')'
        """
        if not self.current_table.has(p[1]):
            raise CompileException(
                self, f"Function {p[1]} is not defined yet.")

        funk = self.current_table.get(p[1])

        if len(funk.arguments) > len(p[3]):
            raise CompileException(
                self, f"Not enough arguments for function {p[1]}")
        elif len(funk.arguments) < len(p[3]):
            raise CompileException(
                self, f"Too many arguments for function {p[1]}")

        prec = Node()
        for i, expr in enumerate(reversed(p[3])):
            actual_type = expr.tipus
            ident = expr.value
            expected_type = self.dict_types.get(
                funk.arguments[len(p[3]) - i - 1][1])
            if expected_type != actual_type:
                raise CompileException(
                    self, f"Argument {ident} type is {actual_type} and should be {expected_type}")
            prec = Node(f'{self.tab()}param {ident}', prec)

        node = Node(f'{self.tab()}call {p[1]}', prec)
        p[0] = Expr(funk.type, '$SP', node)

    def p_funkcall_empty(self, p):
        """
        funkcall : IDENTIFIER '(' ')'
        """
        if not self.current_table.has(p[1]):
            raise CompileException(
                self, f"Function {p[1]} is not defined yet.")

        funk = self.current_table.get(p[1])

        if len(funk.arguments) != 0:
            raise CompileException(
                self, f"Function {p[1]} doesn't accept any argument.")

        node = Node(f'{self.tab()}call {p[1]}')
        p[0] = Expr(funk.type, '$SP', node)

    def p_expr_list(self, p):
        """
        expr : '[' listElem ']'
                | '[' ']'
        """
        if len(p[1:]) == 2:
            tipus = List()
            tmp = self.add_variable(tipus)
        else:
            print(p[2])
            tipus = List(p[2])
            print(tipus)
            tmp = self.add_variable(tipus)
        p[0] = Expr(tipus=tipus, value=tmp)

    def p_listElem(self, p):
        """
        listElem : expr
                    | expr ',' listElem
        """
        if len(p[1:]) == 1:
            p[0] = [p[1]]
        else:
            if not p[1].tipus.isInstance(p[3][-1].tipus):
                raise CompileException(self, "List is not the same tipus")

            p[0] = [p[1]] + p[3]

    def p_expr_funkcall(self, p):
        """
        expr : funkcall
        """
        p[0] = p[1]

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
            raise CompileException(
                self, f"Not supported types for operating the operation {p[2]}")
        antec = Node(None, p[1].node, p[3].node)
        node = Node(
            f'{self.tab()}{tmp} = {p[1].value} {self.dict_ops_arit[p[2]]} {p[3].value};', antec)
        p[0] = Expr(Integer(), tmp, node)

    def p_expr_boolop(self, p):
        """
        expr :  expr AND expr
                | expr OR expr
                | expr XOR expr
        """
        if isinstance(p[1].tipus, Boolean) and p[1].tipus != p[3].tipus:
            raise CompileException(
                self, f"Not supported types for operating the operation {p[2]}")
        tmp = self.add_variable(Boolean())
        antec = Node(None, p[1].node, p[3].node)
        node = Node(
            f'{self.tab()}{tmp} = {p[1].value} {self.dict_ops_bool[p[2]]} {p[3].value};', antec)
        p[0] = Expr(Boolean(), tmp, node)

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
            antec = Node(None, p[1].node, p[3].node)
            node = Node(
                f'{self.tab()}{tmp} = {p[1].value} {self.dict_ops_rel[p[2]]} {p[3].value};', antec)
            p[0] = Expr(Boolean(), tmp, node)
        else:
            raise CompileException(
                self, f"Not supported types for operating the operation {p[2]}")

    def p_expr_bool_not(self, p):
        """
        expr :  NOT expr
        """
        if not isinstance(p[2].tipus, Boolean):
            raise CompileException(
                self, f"Not supported types for operating the operation {p[0]}")
        tmp = self.add_variable(p[2].tipus)
        node = Node(f'{self.tab()}{tmp} = NOT {p[2].value};', p[2].node)
        p[0] = Expr(Boolean(), tmp, node)

    def p_expr_const_int(self, p):
        """
        expr :   INTEGER_VALUE
        """
        p[0] = Expr(Integer(), p[1], Node())

    def p_expr_const_float(self, p):
        """
        expr :   FLOAT_VALUE
        """
        p[0] = Expr(Float(), p[1], Node())

    def p_expr_const_char(self, p):
        """
        expr :   CHAR_VALUE
        """
        p[0] = Expr(Char(), p[1], Node())

    def p_expr_const_bool(self, p):
        """
        expr :   BOOL_VALUE
        """
        p[0] = Expr(Boolean(), p[1], Node())

    def p_expr_ident(self, p):
        """
        expr : IDENTIFIER
        """
        var = self.current_table.get(p[1])
        if var:
            p[0] = Expr(var.type, p[1], Node())
        else:
            raise CompileException(self, f"{p[1]} not found.")

    def p_expr_uresta(self, p):
        """
        expr :  RESTA expr  %prec URESTA
        """
        if not isinstance(p[2].tipus, (Float, Integer)):
            raise CompileException(
                f"RESTA is not allowed for type {p[2].tipus}")
        tmp = self.add_variable(p[2].tipus)
        node = Node(f'{self.tab()}{tmp} = URESTA {p[2].value};', p[2].node)
        p[0] = Expr(p[2].tipus, tmp, node)

    def p_expr_usuma(self, p):
        """
        expr : SUMA expr %prec USUMA
        """
        if not isinstance(p[2].tipus, (Float, Integer)):
            raise CompileException(
                f"SUMA is not allowed for type {p[2].tipus}")
        tmp = self.add_variable(p[2].tipus)
        node = Node(f'{self.tab()}{tmp} = USUMA {p[2].value};', p[2].node)
        p[0] = Expr(p[2].tipus, tmp, node)

    def add_variable(self, tipus: Type):
        name = "tmp" + f"{self.current_table.length()}"
        if not self.current_table.put(VariableSymbol(name, tipus)):
            raise CompileException(self, "State unreachable.")
        return name

    def add_cond_label(self):
        self.num_cond_label += 1
        return f"etiq{self.num_cond_label}"

    def level_tab_if(self):
        return ''.join(['\t'] * self.level_if)

    def tab(self):
        return f"{self.current_table.tabulation()}{self.level_tab_if()}"

    def run(self):
        with open(sys.argv[1]) as f:
            input = f.read()
        yacc.parse(input, debug=False)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"usage: python main.py <file>")
        sys.exit()
    try:
        Parser().run()
    except CompileException as e:
        print(e.get_msg())

from ply import lex, yacc
from collections import defaultdict


class Parser:

    def __init__(self):
        self.lex = lex.lex(module=self)
        self.yacc = yacc.yacc(module=self)
        self.num_line = 1
        self.variables = defaultdict()
        self.binary_operations = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
            "%": lambda x, y: x % y,
            "&": lambda x, y: x & y,
            "|": lambda x, y: x | y,
            "^": lambda x, y: x ^ y,
            ">>":  lambda x, y: x >> y,
            "<<": lambda x, y: x << y,
        }

    tokens = ('VINTEGER', 'VFLOAT', 'INTEGER', 'FLOAT', 'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD', 'CA1', 'RSHIFT', 'LSHIFT', 'AND', 'OR', 'XOR')
    literals = (';', '=')

    t_VINTEGER = r'[a-z]'
    t_VFLOAT = r'[A-Z]'
    t_INTEGER = r'\d+'
    t_FLOAT = r'\d+\.\d*'
    t_SUMA = r'\+'
    t_RESTA = r'-'
    t_MULT = r'\*'
    t_DIV = r'\/'
    t_MOD = r'%'
    t_CA1 = r'~'
    t_RSHIFT = r'>>'
    t_LSHIFT = r'<<'
    t_AND = r'\&'
    t_OR = r'\|'
    t_XOR = r'\^'
    t_ignore = ' \t\n'

    def p_error(self, p):
        print("Syntax error at line %s." % self.num_line)

    def t_error(self, t):
        print("ERROR")
        t.lexer.skip(1)

    precedence = (
        ('right', 'XOR'),
        ('left', 'OR', 'CA1'),
        ('left', 'AND'),
        ('left', 'RSHIFT', 'LSHIFT'),
        ('left', 'SUMA', 'RESTA'),
        ('left', 'MULT', 'DIV', 'MOD'),
        ('right', 'USUMA', 'URESTA'),
    )

    def p_calculadora(self, p):
        """
        calculadora :   calculadora sentence 
                        | empty
        """
        pass

    def p_sentence(self, p):
        """
        sentence :  empty ';'
                    | assignment ';'
                    | print ';'
        """
        self.num_line += 1

    def p_empty(self, p):
        """empty :"""
        pass

    def p_print(self, p):
        """
        print : expression
        """
        print(p[1])

    def p_expression(self, p):
        """
        expression :    intExpression
                        | floatExpression
        """
        p[0] = p[1]

    def p_assignment(self, p):
        """
        assignment :    VINTEGER '=' intExpression
                        | VFLOAT '=' floatExpression
        """
        self.variables[p[1]] = p[3]

    def p_intExpression_binary(self, p):
        """
        intExpression : intExpression SUMA intExpression
                        | intExpression RESTA intExpression
                        | intExpression MULT intExpression
                        | intExpression DIV intExpression
                        | intExpression MOD intExpression
                        | intExpression AND intExpression
                        | intExpression OR intExpression
                        | intExpression XOR intExpression
                        | intExpression RSHIFT intExpression
                        | intExpression LSHIFT intExpression
                        | RESTA intExpression  %prec URESTA
                        | SUMA intExpression %prec USUMA
        """
        if len(p) == 3:
            p[0] = self.binary_operations[p[1]](0, p[2])
        elif p[2] == "/" and int(p[3]) == 0:
            print("ERROR")
        else:
            p[0] = self.binary_operations[p[2]](p[1], p[3])

    def p_intExpression_unary(self, p):
        """
        intExpression : CA1 intExpression
        """
        p[0] = ~p[2]

    def p_intExpression_integer(self, p):
        """
        intExpression : INTEGER
        """
        p[0] = int(p[1])

    def p_intExpression_variable(self, p):
        """
        intExpression : VINTEGER
        """
        if p[1] in self.variables.keys():
            p[0] = self.variables[p[1]]
        else:
            print(f"Not found variable {p[1]}!")

    def p_floatExpression_binary(self, p):
        """
        floatExpression : floatExpression SUMA floatExpression
                        | floatExpression RESTA floatExpression
                        | floatExpression MULT floatExpression
                        | floatExpression DIV floatExpression
                        | floatExpression MOD floatExpression
                        | RESTA floatExpression %prec URESTA
                        | SUMA floatExpression %prec USUMA
        """
        if len(p) == 3:
            p[0] = self.binary_operations[p[1]](0, p[2])
        elif (p[2] == "/" and int(p[3]) == 0):
            print("ERROR")
        else:
            p[0] = self.binary_operations[p[2]](p[1], p[3])

    def p_floatExpression_float(self, p):
        """
        floatExpression : FLOAT
        """
        p[0] = float(p[1])

    def p_floatExpression_variable(self, p):
        """
        floatExpression : VFLOAT
        """
        if p[1] in self.variables.keys():
            p[0] = self.variables[p[1]]
        else:
            print(f"Not found variable {p[1]}!")

    def run(self):
        while True:
            try:
                s = input()
            except EOFError:
                break
            if not s:
                continue
            yacc.parse(s)
        print('\n'.join(map(lambda x: f"{str(x[0])} : {str(x[1])}" , self.variables.items())))

Parser().run()
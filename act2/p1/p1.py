from ply import lex, yacc
from collections import defaultdict
import parser

class Parser:

    def __init__(self):
        self.lex = lex.lex(module=self)
        self.yacc = yacc.yacc(module=self)
        self.num_line = 1
        self.variables = defaultdict()
        self.binary_operations: {
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
        self.unary_operations: {
            "+": lambda x: x,
            "-": lambda x: -x,
            "~": lambda x: ~x,
        }
    
    tokens = ('VINTEGER', 'VFLOAT', 'INTEGER', 'FLOAT', 'SUMA', 'SUMA_UNARIA','RESTA', 'RESTA_UNARIA', 'MULT', 'DIV', 'MOD', 'CA1', 'RSHIFT', 'LSHIFT', 'AND', 'OR', 'XOR')
    literals = (';', '=')

    t_VINTEGER = r'[a-z]'
    t_VFLOAT = r'[A-Z]'
    t_INTEGER = r'\d+'
    t_FLOAT = r'\d+\.\d*'
    t_SUMA = r'\+'
    t_RESTA = r'-'
    t_RESTA_UNARIA = r'-'
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
        ('left', 'SUMA', 'RESTA'),
        ('left', 'MULT', 'DIV', 'MOD'),
        ('right', 'RESTA_UNARIA', 'SUMA_UNARIA'),
    )
    
    def p_sentence(self, p):
        """
        sentence :  empty ';'
                    | assignment ';'
                    | print ';'
        """
        self.num_line += 1
    
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
        assignment :    VINTEGER = intExpression
                        | VFLOAT = floatExpression
        """
        variables[p[1]] = p[3]
        
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
        """
        if (p[2] == "/" and int(p[3]) == 0):
            print("ERROR")
        p[0] = self.binary_operations[p[2]](p[1], p[3])

    def p_intExpression_unary(self, p):
        """
        intExpression : RESTA_UNARIA intExpression
                        | SUMA_UNARIA intExpression
                        | CA1 intExpression
        """
        p[0] = self.unary_operations[p[1]](p[2])

    def p_intExpression_integer(self, p):
        """
        intExpression : INTEGER
        """
        return int(p[1])

    def p_intExpression_binary(self, p):
        """
        intExpression : intExpression SUMA intExpression
                        | intExpression RESTA intExpression
                        | intExpression MULT intExpression
                        | intExpression DIV intExpression
                        | intExpression MOD intExpression
        """
        if (p[2] == "/" and int(p[3]) == 0):
            print("ERROR")
        p[0] = self.binary_operations[p[2]](p[1], p[3])

    def p_floatExpression_unary(self, p):
        """
        floatExpression : RESTA_UNARIA floatExpression
                        | SUMA_UNARIA floatExpression
        """
        p[0] = self.unary_operations[p[1]](p[2])

    def p_floatExpression_float(self, p):
        """
        floatExpression : FLOAT
        """
        return float(p[1])

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
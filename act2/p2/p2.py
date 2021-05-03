from ply import lex, yacc

class Parser:

    def __init__(self):
        self.lex = lex.lex(module=self)
        self.yacc = yacc.yacc(module=self)
        self.num_line = 1

    tokens = ('INTEGER', 'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD')
    literals = ('(', ')', ';')

    t_INTEGER = r'\d+'
    t_SUMA = r'\+'
    t_RESTA = r'-'
    t_MULT = r'\*'
    t_DIV = r'\/'
    t_MOD = r'%'
    t_ignore = ' \t\n'

    def t_error(self, t):
        print("ERROR")
        t.lexer.skip(1)

    precedence = (
        ('left', 'SUMA', 'RESTA'),
        ('left', 'MULT', 'DIV', 'MOD')
    )

    def p_calculadora(self, p):
        """
        calculadora :   calculadora sentence 
                        | empty
        """

    def p_sentencia(self, p):
        """
        sentence : expr ';'
        """
        p[0] = p[1]
        print(p[1])
        self.num_line += 1

    def p_sentencia_buida(self, p):
        """
        sentence : empty ';'
        """
        self.num_line += 1

    def p_expr(self, p):
        """
        expr : '(' expr ')'
              | expr SUMA expr
              | expr RESTA expr
              | expr MULT expr
              | expr DIV expr
              | expr MOD expr
              | INTEGER
        """
        if (len(p) == 4):
            if (p[1] == '('):
                p[0] = f"{p[2]}"
            else:
                p[0] = f"{p[1]} {p[3]} {p[2]}"
        else:
            p[0] = f"{p[1]}"
    
    def p_empty(self, p):
        'empty :'
        pass

    def p_error(self, p):
        print("Syntax error at line %s." % self.num_line)
    

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
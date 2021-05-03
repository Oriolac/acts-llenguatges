from ply import lex, yacc


class Parser:

    def __init__(self):
        self.lex = lex.lex(module=self)
        self.yacc = yacc.yacc(module=self)
        self.num_line = 1

    tokens = ('SYMBOL', 'LAMBDA', 'COMMENT')

    literals = ['|', '.', '*', '+', '?', '(', ')', ';']

    t_SYMBOL = r'[a-d]'
    t_LAMBDA = r'(?i)buida'
    t_COMMENT = r'\#.*'
    t_ignore = ' \t'

    precedence = (
        ('left', '|'),
        ('left', '.'),
        ('left', '*', '+', '?'),
    )

    def t_newline(self, t):
        r'\n'
        global num_line
        num_line += 1

    def t_error(self, t):
        t.lexer.skip(1)

    def p_error(self, p):
        print("Syntax error at line %s." % self.num_line)

    def p_empty(self, p):
        """empty :"""
        pass

    def p_thompson(self, p):
        """
        thompson :   thompson regex
                        | empty
        """

    def p_regex(self, p):
        """
        regex :  empty ';'
                    | expr ';'
        """
        self.num_line += 1

    def p_expr_OR(self, p):
        """
        expr : expr '|' expr
        """

    def p_expr_CON(self, p):
        """
        expr : expr '.' expr
        """

    def p_expr_Kleene(self, p):
        """
        expr : expr '*'
        """
    def p_expr_POS(self, p):
        """
        expr : expr '+'
        """

    def p_expr_OPT(self, p):
        """
        expr: expr '?'
        """

    def p_expr_use(self, p):
        """
            expr: SYMBOL
        """
        p[0] = p[1]

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

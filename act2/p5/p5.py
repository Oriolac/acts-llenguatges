from ply import lex, yacc

class Parser:

    def __init__(self):
        self.lex = lex.lex(module=self)
        self.yacc = yacc.yacc(module=self)
        self.num_line = 1

    tokens = ('VARS', 'AND', 'OR', 'NEG', 'IMPLIES', 'DIMPLY')
    literals = ('(', ')', ';')

    t_VARS = r'[A-Z]'
    t_AND = r'\^'
    t_OR = r'v'
    t_NEG = r'\!'
    t_IMPLIES = r'\->'
    t_DIMPLY = r'\<->'
    t_ignore = ' \t\n'

    def t_error(self, t):
        print("ERROR")
        t.lexer.skip(1)

    precedence = (
        ('left', 'DIMPLY', 'IMPLIES'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('right', 'NEG'),
    )

    def p_entrada(self, p):
        """
        entrada :   entrada sentence 
                        | empty
        """
        pass

    def p_sentencia(self, p):
        """
        sentence : expr ';'
        """
        p[0] = f"{p[1]}"
        print(p[1])
        self.num_line += 1

    def p_expr_conjs(self, p):
        """
        expr : expr AND expr
                | expr OR expr
                | '(' expr ')'
        """
        p[0] = f"{p[1]} {p[2]} {p[3]}"

    def p_expr_neg(self, p):
        """
        expr : NEG expr
        """
        p[0] = f"!{p[2]}"

    def p_expr_implies(self, p):
        """ 
        expr : expr IMPLIES expr
        """
        p[0] = f"! ({p[1]}) v ({p[3]})"

    def p_expr_dimply(self, p):
        """ 
        expr : expr DIMPLY expr
        """
        p[0] = f"(!({p[1]}) v ({p[3]})) ^ (!({p[3]}) v ({p[1]}))"

    def p_expr_lit(self, p):
        """
        expr : VARS
        """
        p[0] = f"{p[1]}"

    def p_empty(self, p):
        'empty :'
        pass

    def p_error(self, p):
        print(p)
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
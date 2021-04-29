from ply import lex, yacc


class Expression:
    
    def __init__(self, isP, prioritat, expression):
        self.isParent: bool = isP
        self.prioritat: int = prioritat
        self.expression: str = expression

    def __str__(self):
        return f"[tP: {self.isParent}, pr: {self.prioritat}, ex: {self.expression}]"

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

    def p_sentencia(self, p):
        """
        sentence : expr ';'
        """
        p[0] = p[1]
        print(p[0].expression)
        self.num_line += 1

    def p_sentencia_buida(self, p):
        """
        sentence : empty ';'
        """
        self.num_line += 1

    def p_expr(self, p):
        """
        expr :   '(' expr ')'
              | INTEGER
        """
        if self.is_integer(p):
            p[0] = Expression(False, 0, f"{p[1]}")  
        elif self.has_parenthesis(p):
            p[0] = Expression(True, p[2].prioritat, p[2].expression)


    def p_expr_prioritat_alta(self, p):
        """
        expr : expr MULT expr
              | expr DIV expr
              | expr MOD expr
        """
        left, right = p[1].expression, p[3].expression
        if p[1].isParent and p[1].prioritat < 1:
            left = "(" + p[1].expression + ")"
        if p[3].isParent and p[3].prioritat < 1:
            right = "(" + p[3].expression + ")"
        p[0] = Expression(False, 1, f"{left} {p[2]} {right}")


    def p_expr_prioritat_baixa(self, p):
        """
        expr :      expr SUMA expr
                |   expr RESTA expr
        """
        p[0] = Expression(False, 0, f"{p[1].expression} {p[2]} {p[3].expression}")

    def is_integer(self,p):
        return len(p) == 2

    def has_parenthesis(self, p):
        return p[1] == '('

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
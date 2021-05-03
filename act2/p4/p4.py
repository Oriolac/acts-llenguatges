from __future__ import annotations
from ply import lex, yacc
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Estat:
    index: int
    simbol: str
    estats: List[Estat]


class Parser:

    def __init__(self):
        self.lex = lex.lex(module=self)
        self.yacc = yacc.yacc(module=self)
        self.num_line = 1
        self.num_estats = 0
        self.estats = dict()

    tokens = ('SYMBOL',)

    literals = ['|', '.', '*', '+', '?', '(', ')', ';']

    t_SYMBOL = r'[a-d]'
    t_ignore = ' \t\n'

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

    def p_thompson(self, p):
        """
        thompson :   thompson regex
                        | empty
        """
        pass

    def p_error(self, p):
        print("Syntax error at line %s." % self.num_line)

    def p_empty(self, p):
        """empty :"""
        pass

    def p_regex_expr(self, p):
        """
        regex : expr ';'
        """
        print(f"Estat numerats del 1 al {self.num_estats + 1}")
        for num, estat in self.estats.items():
            next_index = [self.num_estats + 1] if not estat.estats else list(map(lambda e: e.index, estat.estats))
            print(f"[Estat {estat.index}, Símbol {estat.simbol}] Go to {' or '.join(map(str, next_index))}")
        self.num_line += 1
        print(f"Estat inicial: {p[1][0].index}")
        print(f"Estat final: {self.num_estats + 1}")
        self.num_estats = 0
        self.estats = dict()

    def p_regex_empty(self, p):
        """
        regex : empty ';'
        """
        self.num_line += 1

    def p_regex_parent(self, p):
        """
        expr : '(' expr ')'
        """
        p[0] = p[2]

    def p_expr_OR(self, p):
        """
        expr : expr '|' expr
        """
        self.num_estats += 1
        initial = Estat(self.num_estats, "LAMBDA", [p[1][0], p[3][0]])
        self.estats[self.num_estats] = initial
        self.num_estats += 1
        final = Estat(self.num_estats, "LAMBDA", None)
        self.estats[self.num_estats] = final
        p[1][-1].estats = [final]
        p[3][-1].estats = [final]
        p[0] = [initial, final]



    def p_expr_CON(self, p):
        """
        expr : expr '.' expr
        """
        self.num_estats += 1
        inter = Estat(self.num_estats, "LAMBDA", [p[3][0]])
        p[1][-1].estats = [inter]
        self.estats[self.num_estats] = inter
        p[0] = p[1] + [inter] + p[3]

    def p_expr_Kleene(self, p):
        """
        expr : expr '*'
        """
        self.num_estats += 1
        final = Estat(self.num_estats, "LAMBDA", None)
        self.estats[self.num_estats] = final
        self.num_estats += 1
        initial = Estat(self.num_estats, "LAMBDA", [p[1][0], final])
        self.estats[self.num_estats] = initial
        p[1][-1].estats = [p[1][0], final]
        p[0] = [initial, final]

    def p_expr_POS(self, p):
        """
        expr : expr '+'
        """
        self.num_estats += 1
        final = Estat(self.num_estats, "LAMBDA", None)
        self.estats[self.num_estats] = final
        self.num_estats += 1
        initial = Estat(self.num_estats, "LAMBDA", [p[1][0]])
        self.estats[self.num_estats] = initial
        p[1][-1].estats = [p[1][0], final]
        p[0] = [initial, final]

    def p_expr_OPT(self, p):
        """
        expr : expr '?'
        """
        self.num_estats += 1
        final = Estat(self.num_estats, "LAMBDA", None)
        self.estats[self.num_estats] = final
        self.num_estats += 1
        initial = Estat(self.num_estats, "LAMBDA", [p[1][0], final])
        self.estats[self.num_estats] = initial
        p[1][-1].estats = [final]
        p[0] = [initial, final]

    def p_expr_symbol(self, p):
        """
            expr : SYMBOL
        """
        self.num_estats += 1
        estat = Estat(self.num_estats, p[1], None)
        p[0] = [estat]
        self.estats[self.num_estats] = estat

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

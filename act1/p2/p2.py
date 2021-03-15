from ply import lex
import sys


num_line = 1

class MyLexer:

    tokens = ('VARIABLE', 'IMPLICACIO', 'DOBLE_IMPLICACIO', 'COMENTARI')

    literals = ['!', '^', '∨', '(', ')']

    states = (
        ('panic', 'exclusive'),
    )

    t_VARIABLE = r'[A-Z]'
    t_IMPLICACIO = r'->'
    t_DOBLE_IMPLICACIO = r'<->'
    t_COMENTARI = r'\#.*'
    t_ignore = ' \t'
    t_panic_ignore = '.*'

    def t_newline(self, t):
        r'\n'
        global num_line
        num_line += 1

    def t_panic_newline(self, t):
        r'\n'
        t.lexer.begin('INITIAL')
        global num_line
        num_line += 1

    def t_panic_error(self, t):
        t.lexer.skip(1)

    def t_error(self, t):
        print(f"Error línea {num_line}: {t.value[0]} no es reconeix.")
        t.lexer.begin('panic')
        t.lexer.skip(1)

    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

m = MyLexer()
m.build()           # Build the lexer
while True:
    try:
        data = input()
        m.lexer.input(data + '\n')
        token = m.lexer.token()
        while token:
            token = m.lexer.token()
    except EOFError:
        break
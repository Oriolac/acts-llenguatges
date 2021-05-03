from __future__ import annotations
from ply import lex, yacc
from dataclasses import dataclass
from abc import ABC, abstractmethod

negate_ops = {
    "v": "^",
    "^": "v",
}

priority_ops = {
    "v": 1,
    "^": 2,
}

class Node(ABC):

    @abstractmethod
    def curry_neg(self, last_neg=False) -> Node:
        pass

    @abstractmethod
    def delete_parents(self, must_remove=False) -> Node:
        pass


@dataclass
class BinaryNode(Node):
    left: Node
    op: str
    right: Node

    def curry_neg(self, last_neg=False) -> Node:
        op = negate_ops[self.op] if last_neg else self.op
        return BinaryNode(self.left.curry_neg(last_neg), op, self.right.curry_neg(last_neg))


    def delete_parents(self, must_remove=False) -> Node:
        print(f"BinaryNode {self} -> delete_parents")
        self.left = self.check_parent(self.left, self.op)
        self.right = self.check_parent(self.right, self.op)
        return self


    def check_parent(self, node: Node, op: str):
        print(f"BinaryNode {self} -> check_parents: {node}")
        if isinstance(node, PNode):
            print(f"BinaryNode {self} -> check_parents: {node} is PNode")
            if  not isinstance(node.child, BinaryNode):
                print(f"BinaryNode {self} -> check_parents: child {node.child} is not BinaryNode")
                return node.child.delete_parents()
            elif priority_ops[self.op] == priority_ops[node.child.op]:
                print(f"BinaryNode {self} -> check_parents: child {node.child} is BinaryNode ==")
                return node.child.delete_parents(True)
            else:
                print(f"BinaryNode {self} -> check_parents: child {node.child} is BinaryNode !=")
                return PNode(node.child.delete_parents())
        return node.delete_parents()


    def __str__(self):
        return f"{self.left} {self.op} {self.right}"


@dataclass
class SymbolNode(Node):
    value: str

    def curry_neg(self, last_neg=False) -> SymbolNode:
        return SymbolNode(f"!{self.value}") if last_neg else self

    def delete_parents(self, must_remove=False) -> Node:
        return self

    def __str__(self):
        return f"{self.value}"


@dataclass
class NegNode(Node):
    child: Node

    def curry_neg(self, last_neg=False) -> Node:
        return PNode(self.child.curry_neg(True and not last_neg))

    def delete_parents(self, must_remove=False) -> Node:
        return self.child.delete_parents()

    def __str__(self):
        return f"!{self.child}"


@dataclass
class PNode(Node):
    child: Node

    def curry_neg(self, last_neg=False) -> Node():
        return PNode(self.child.curry_neg(last_neg))

    def delete_parents(self, must_remove=False) -> Node:
        print(f"PNode {self} -> delete_parents")
        if must_remove:
            return self.child.delete_parents()
        if isinstance(self.child, PNode):
            return self.child.delete_parents(True)
        return self.child

    def __str__(self):
        return f"({self.child})"


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
        res = p[1].curry_neg()
        print("BEFORE: ", res)
        res = res.delete_parents()
        print("AFTER: ", res)
        self.num_line += 1

    def p_expr_conjs(self, p):
        """
        expr : expr AND expr
                | expr OR expr
        """
        p[0] = BinaryNode(p[1], p[2], p[3])

    def p_expr_pare(self, p):
        """
        expr : '(' expr ')'
        """
        p[0] = PNode(p[2])

    def p_expr_neg(self, p):
        """
        expr : NEG expr
        """
        p[0] = NegNode(p[2])

    def p_expr_implies(self, p):
        """ 
        expr : expr IMPLIES expr
        """
        p[0] = BinaryNode(
            NegNode(p[1]),
            "v",
            p[3]
        )

    def p_expr_dimply(self, p):
        """ 
        expr : expr DIMPLY expr
        """
        p[0] = BinaryNode(
            PNode(
                BinaryNode(
                    NegNode(p[1]),
                    "v",
                    p[3])
            ),
            "^",
            PNode(
                BinaryNode(
                    NegNode(p[3]),
                    "v",
                    p[1]
                )
            )
        )

    def p_expr_lit(self, p):
        """
        expr : VARS
        """
        p[0] = SymbolNode(f"{p[1]}")

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

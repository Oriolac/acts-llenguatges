import unittest
from p6 import Node, PNode, BinaryNode, SymbolNode, NegNode

class BinaryCase(unittest.TestCase):

    def setUp(self):
        a = SymbolNode("A")
        b = SymbolNode("B")
        c = SymbolNode("C")
        self.node: BinaryNode = BinaryNode(PNode(BinaryNode(a, "v", b)), "^", c)

    def test_upper(self):
        self.node.delete_parents()

if __name__ == '__main__':
    unittest.main()
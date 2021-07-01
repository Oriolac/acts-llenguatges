from typing import Optional

class Node:

    def __init__(self, label: Optional[str]=None, left=None, right=None):
        self.label = label
        self.left = left
        self.right = right
    
    def print(self):
        if self.left != None:
            self.left.print()
        if self.label != None:
            print(self.label)
        if self.right != None:
            self.right.print()

    def __str__(self):
        return f"({self.label}) : [{self.left}, {self.right}]"
    
from __future__ import annotations
from abc import ABC

class Condition(ABC):
    def __init__(self, a: Condition, b: Condition):
        self.A: Condition = a


class NOTCondition(Condition):
    def __init__(self, a: Condition):
        super().__init__(a)

class BinaryCondition(Condition):
    def __init__(self, a: Condition, b: Condition):
        super().__init__(a)
        self.b: Condition = b

class ANDCond(BinaryCondition):

    def __init__(self, a: Condition, b: Condition):
        super().__init__(a, b)


class ORCond(BinaryCondition):

    def __init__(self, a: Condition, b: Condition):
        super().__init__(a, b)
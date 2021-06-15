from __future__ import annotations
from abc import ABC
from computils.expr import Boolean
from typing import Union

class Condition(ABC):
    def __init__(self, a: Union[Condition, Boolean]):
        self.A: Condition = a


class NOTCond(Condition):
    def __init__(self, a: Union[Condition, Boolean]):
        super().__init__(a)

    def __str__(self) -> str:
        return f"NOTCond({self.A})"

class BinaryCondition(Condition):
    def __init__(self, a: Union[Condition, Boolean], b: Union[Condition, Boolean]):
        super().__init__(a)
        self.B: Condition = b

class ANDCond(BinaryCondition):

    def __init__(self, a: Union[Condition, Boolean], b: Union[Condition, Boolean]):
        super().__init__(a, b)

    def __str__(self) -> str:
        return f"ANDCond({self.A}, {self.B})"


class ORCond(BinaryCondition):

    def __init__(self, a: Union[Condition, Boolean], b: Union[Condition, Boolean]):
        super().__init__(a, b)
    

    def __str__(self) -> str:
        return f"ORCond({self.A}, {self.B})"
from __future__ import annotations
from computils.exceptions import CompileException
from computils.node import Node

from dataclasses import dataclass
from typing import Any, Optional
from abc import ABC, abstractmethod
from functools import reduce

class Expr:

    def __init__(self, tipus: Type, value: Any, node: Node):
        self.tipus: Type = tipus
        self.value: Any = value
        self.node = node

    def __str__(self) -> str:
        return f"{self.tipus}, {self.value}, {self.node}"

@dataclass
class Type(ABC):
    
    def isInstance(self, obj):
        return isinstance(obj, self.__class__)


@dataclass
class Boolean(Type):

    def getSize(self):
        return 1

@dataclass
class Num(Type):

    def isInstance(self, obj):
        return isinstance(obj, Num)

@dataclass
class Integer(Num):

    def getSize(self):
        return 4


@dataclass
class Float(Num):

    def getSize(self):
        return 4


@dataclass
class Char(Type):

    def getSize(self):
        return 2


class List(Type):

    def __init__(self, exprs: List[Expr] = []):
        self.exprs: dict = dict()
        acc = 0
        for expressio in exprs:
            self.exprs[acc] = expressio
            acc += expressio.tipus.getSize()
        if exprs == []:
            self.elementsType = []
            self.tipus: Type = None
        else:
            self.elementsType = list(map(lambda x: x.tipus, exprs))
            for i, elem  in enumerate(self.elementsType):
                if not self.elementsType[i-1].isInstance(self.elementsType[i]):
                    raise CompileException("Not correct types")
            self.tipus = Num() if isinstance(self.elementsType[0], (Float, Integer)) else self.elementsType[0]
        self.numElements: int = len(exprs)

    def getSize(self):
        return sum(map(lambda x: x.getSize(), self.elementsType))

    def getIndividualSize(self):
        print(self.elementsType)
    
    def isInstance(self, obj):
        if not isinstance(obj, List):
            return False
        if isinstance(self.tipus, List):
            return obj.tipus.isInstance(self.tipus)
        return self.tipus.isInstance(obj.tipus)

    def __str__(self):
        return f"List of {self.tipus} [numElements={self.numElements}, elementsType={self.elementsType}]"

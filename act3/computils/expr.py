from __future__ import annotations
from computils.exceptions import CompileException

from dataclasses import dataclass
from typing import Any, Optional
from abc import ABC, abstractmethod
from functools import reduce


@dataclass
class Expr:
    tipus: Type
    value: Any


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
        if exprs == []:
            self.elementsType = []
            self.type = None
        else:
            print(exprs)
            self.elementsType = list(map(lambda x: x.tipus, exprs))
            for i, elem  in enumerate(self.elementsType):
                if not self.elementsType[i-1].isInstance(self.elementsType[i]):
                    raise CompileException("Not correct types")
            self.type = Num() if isinstance(self.elementsType[0], (Float, Integer)) else self.elementsType[0]
        self.numElements: int = len(exprs)

    def getSize(self):
        return sum(map(lambda x: x.getSize(), self.elementsType))
    
    def isInstance(self, obj):
        if not isinstance(obj, List):
            return False
        if isinstance(self.elementType, List):
            return obj.elementType.isInstance(self.elementType)
        return self.elementType.isInstance(obj.elementType)

    def __str__(self):
        return f"List{self.type})[{self.numElements}]{self.elementsType}"

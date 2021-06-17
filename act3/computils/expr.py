from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional
from abc import ABC, abstractmethod


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

    def __init__(self, elementType: Optional[Type] = None):
        self.elementType: Optional[Type] = elementType

    def getSize(self, list):
        return lambda x: x.size()
    
    def isInstance(self, obj):
        if not isinstance(obj, List):
            return False
        if isinstance(self.elementType, List):
            return obj.elementType.isInstance(self.elementType)
        return self.elementType.isInstance(obj.elementType)


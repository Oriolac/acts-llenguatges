from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from abc import ABC, abstractmethod

@dataclass
class Expr:
    tipus: Type
    value: Any

@dataclass
class Type(ABC):
    pass

@dataclass
class Boolean(Type):
    
    def getSize(self):
        return 1

@dataclass
class Integer(Type):
    
    def getSize(self):
        return 4

@dataclass
class Float(Type):
    
    def getSize(self):
        return 4

@dataclass
class Char(Type):
    
    def getSize(self):
        return 2

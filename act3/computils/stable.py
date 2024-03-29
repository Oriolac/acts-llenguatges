from __future__ import annotations

from typing import Dict, Optional
from .expr import Type

from abc import ABC, abstractmethod

class Symbol(ABC):
    def __init__(self, name, tipus):
        self.name = name
        self.type: Type = tipus

    @abstractmethod
    def getSize(self):
        pass

class VariableSymbol(Symbol):
    
    def getSize(self):
        return self.type.getSize()

class FunctionSymbol(Symbol):
    def __init__(self, name, tipus, arguments):
        self.name = name
        self.type = tipus
        self.arguments = arguments

    def getSize(self):
        return None

class SymbolTable:

    def __init__(self, parent: SymbolTable, name: Optional[str] = None):
        self.symbols: Dict[Symbol] = {}
        self.name: str = name
        self.parent: SymbolTable = parent
        self.level = parent.level + 1 if parent and name else 0


    def put(self, symbol: Symbol):
        if self.symbols.__contains__(symbol.name) and not isinstance(symbol.type, self.symbols[symbol.name].__class__):
            return False
        else:
            self.symbols[symbol.name]= symbol
            return True

    def get(self, name: str) -> Symbol:
        if self.symbols.__contains__(name):
            return self.symbols[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            return None

    def has(self, name:str):
        return self.symbols.__contains__(name) or (self.parent and self.parent.has(name))

    def getParentScope(self):
        return self.parent

    def length(self):
        return len(self.symbols)

    def tabulation(self) -> str:
        return ''.join(['\t'] * self.level)
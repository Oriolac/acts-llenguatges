from __future__ import annotations
from .expr import Type

from abc import ABC

class Symbol(ABC):
    def __init__(self, name, tipus):
        self.name = name
        self.type: Type = tipus

class VariableSymbol(Symbol):
    pass

class FunctionSymbol(Symbol):
    def __init__(self, name, tipus, arguments):
        self.name = name
        self.type = tipus
        self.arguments = arguments

class SymbolTable:

    def __init__(self, parent: SymbolTable, name: str):
        self.symbols: set[Symbol] = {}
        self.name: str = name
        self.parent: SymbolTable = parent

    def put(self, symbol: Symbol):
        if self.symbols.__contains__(symbol.name):
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

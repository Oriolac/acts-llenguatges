from __future__ import annotations

from dataclasses import dataclass
from typing import Any




@dataclass
class Expr:
    tipus: Type
    value: Any

@dataclass
class Type:
    pass

@dataclass
class Boolean(Type):
    pass

@dataclass
class Integer(Type):
    pass

@dataclass
class Float(Type):
    pass

@dataclass
class Char(Type):
    pass
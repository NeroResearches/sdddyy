from .dop.dop.token import TokenDop

from dataclasses import dataclass
from typing import Literal as L


@dataclass(frozen=True)
class OperatorDop(TokenDop):
    op: L['+'] | L['-'] | L['*'] | L['^'] | L['/']


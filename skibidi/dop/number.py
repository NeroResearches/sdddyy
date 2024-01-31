from .dop.dop.token import TokenDop

from dataclasses import dataclass

@dataclass(frozen=True)
class NumberDop(TokenDop):
    value: int


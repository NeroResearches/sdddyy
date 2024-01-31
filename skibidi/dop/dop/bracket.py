from .dop.token import TokenDop

from dataclasses import dataclass

@dataclass(frozen=True)
class BracketDop(TokenDop):
    open: bool


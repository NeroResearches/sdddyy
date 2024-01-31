from ..token import TokenDop
from ..expr import (
    ExprDop,
    BinOpDop,
    UnaryOpDop,
    NumberExprDop
)

from skibidi.dop.operator import OperatorDop
from skibidi.dop.number import NumberDop
from skibidi.dop.dop.bracket import BracketDop

from typing import Callable
from itertools import takewhile

OPERATORS = {'+', '-', '*', '/', '^'}

class Eof(Exception): ...

def span(text: str, predicate: Callable[[str], bool]) -> tuple[str, str]:
    matched = ''.join(list(takewhile(predicate, text)))
    return (matched, text[len(matched):])

def tokenize(text: str) -> list[TokenDop]:
    text = text.strip()  # get rid of leading/trailing whitespaces
    if not text:
        return []

    head, tail = text[0], text[1:]
    if head.isdigit():
        (rest, tail) = span(tail, str.isdigit)
        number = int(head + rest)

        return [NumberDop(number)] + tokenize(tail)
    elif head.isspace():
        return tokenize(tail)
    elif head in OPERATORS:
        return [OperatorDop(head)] + tokenize(tail)
    elif head in '()':
        return [BracketDop(head == '(')] + tokenize(tail)
    else:
        raise ValueError(f"Unknown token {head!r}")

def factor(tokens: list[TokenDop]) -> tuple[ExprDop, list[TokenDop]]:
    if not tokens:
        raise Eof()

    head, tail = tokens[0], tokens[1:]
    if isinstance(head, BracketDop):
        if head.open:
            expr, left = parse_tailed(tail)
            if isinstance(left[0], BracketDop) and not left[0].open:
                return expr, left[1:]
            raise SyntaxError("Unmatched closing bracket")
    elif isinstance(head, NumberDop):
        return NumberExprDop(head), tail
    elif isinstance(head, OperatorDop):
        unary_operand, left = factor(tail)
        return UnaryOpDop(head, unary_operand), left

    raise SyntaxError(f"Unexpected token {head!r}")

def expect_operator(tokens: list[TokenDop], one_of: tuple[str, ...]) -> tuple[OperatorDop, list[TokenDop]] | None:
    if not tokens:
        return None
    head, tail = tokens[0], tokens[1:]
    if isinstance(head, OperatorDop) and head.op in one_of:
        return (head, tail)
    return None

def left_associative(
    tokens: list[TokenDop],
    ops: tuple[str, ...],
    down: Callable[[list[TokenDop]], tuple[ExprDop, list[TokenDop]]],
) -> tuple[ExprDop, list[TokenDop]]:
    lhs, t = down(tokens)
    o = expect_operator(t, one_of=ops)
    if o is None:
        return lhs, t
    operator, t = o

    rhs, t = down(t)
    expr = BinOpDop(lhs, operator, rhs)

    # Left associativity
    while True:
        o = expect_operator(t, one_of=ops)
        if o is None:
            break
        operator, t = o
        rhs, t = down(t)

        expr = BinOpDop(expr, operator, rhs)
    return expr, t

def parse_tailed(tokens: list[TokenDop]) -> tuple[ExprDop, list[TokenDop]]:
    return left_associative(
        tokens,
        ('+', '-'),
        lambda tks: left_associative(
            tks,
            ('*', '/'),
            factor,
        )
    )
    


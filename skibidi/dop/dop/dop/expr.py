from dataclasses import dataclass
from abc import ABCMeta, abstractmethod

from skibidi.dop.operator import OperatorDop
from skibidi.dop.number import NumberDop

class ExprDop(metaclass=ABCMeta):
    @abstractmethod
    def eval(self) -> int:
        raise NotImplemented


@dataclass(frozen=True)
class BinOpDop(ExprDop):
    lhs: ExprDop
    op: OperatorDop
    rhs: ExprDop

    def eval(self) -> int:
        lhs = self.lhs.eval()
        rhs = self.rhs.eval()

        match self.op.op:
            case '+':
                return lhs + rhs
            case '-':
                return lhs - rhs
            case '*':
                return lhs * rhs
            case '/':
                return lhs // rhs

            case o:
                raise TypeError(f"Unknown binary operator: {o}")


@dataclass(frozen=True)
class NumberExprDop(ExprDop):
    value: NumberDop

    def eval(self) -> int:
        return self.value.value


@dataclass(frozen=True)
class UnaryOpDop(ExprDop):
    op: OperatorDop
    rhs: ExprDop

    def eval(self) -> int:
        rhs = self.rhs.eval()
        match self.op.op:
            case '-':
                return -rhs
            case un:
                raise TypeError(f"Unknown unary operator: {un}")



import sys
import pprint

from skibidi.dop.dop.dop.yes.yes import tokenize, parse_tailed

tks = tokenize("(2 + 2 + 3 + 4) * 2")
expr, tail = parse_tailed(tks)

if tail:
    print(f"[-] Parse error, left tokens: {tail}")
    sys.exit(1)

print("Expr:")
pprint.pprint(expr)
print("Result:")
print(expr.eval())


#!/usr/bin/env python3

import logging
import sys
from argparse import ArgumentParser

cli = ArgumentParser(description=(
    "REPL that compute logical, bitwise and arithmetic expressions."))
cli.add_argument("-v", "--verbose", dest="loglevel", action="store_const",
        default=logging.INFO, const=logging.DEBUG,
        help="Verbose debug mode.")
cli.add_argument("-c", dest="expr", action="store",
        help="Evaluate the expression and exit.")
options = cli.parse_args()
logging.basicConfig(level=options.loglevel)
logger = logging.getLogger()

from lark.exceptions import LarkError
import visitor
from parser import parser


def repl():
    print("Use exit() or Ctrl-D (i.e. EOF) to exit")
    while True:
        try:
            expr = input("? ")
        except EOFError:
            break
        if not expr:
            continue
        if expr.rstrip("()") in ["quit", "exit"]:
            break
        try:
            print(eval(expr))
        except (ArithmeticError, TypeError) as exc:
            print("error:", exc, file=sys.stderr)
        except LarkError as exc:
            print("syntax error:", expr)
            print(" " * (12 + exc.column), "^", file=sys.stderr)


def eval(expr):
    tree = parser.parse(expr)
    visitor.eval_numbers(tree)
    visitor.eval_booleans(tree)
    visitor.type_checker(tree)
    visitor.compute(tree)
    return tree.meta.value


if options.expr:
    print(eval(options.expr))
else:
    repl()

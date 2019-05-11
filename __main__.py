#!/usr/bin/env python3

import logging
from argparse import ArgumentParser

cli = ArgumentParser()
cli.add_argument("-v", "--verbose", dest="loglevel", action="store_const",
        default=logging.INFO, const=logging.DEBUG,
        help="Verbose debug mode.")
cli.add_argument("-c", "--expr", dest="expr", action="store",
        help="Evaluate the expression and exit.")
options = cli.parse_args()
logging.basicConfig(level=options.loglevel)
logger = logging.getLogger()

import sys
from parser import parser
from visitor import eval_numbers, eval_booleans, type_checker
from compute import compute


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
        except TypeError as exc:
            print(exc, file=sys.stderr)


def eval(expr):
    tree = parser.parse(expr)
    eval_numbers(tree)
    eval_booleans(tree)
    type_checker(tree)
    compute(tree)
    return tree.meta.value


if options.expr:
    print(eval(options.expr))
else:
    repl()


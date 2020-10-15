#!/usr/bin/env python3

import argparse
import logging
import sys
from lark.exceptions import LarkError
import expr

# cli options
parser = argparse.ArgumentParser(description=(
    "REPL that compute logical, bitwise and arithmetic expressions."))
parser.add_argument("-v", "--verbose", action="count", default=0,
        help="increase verbosity")
parser.add_argument("-s", "--silent", action="count", default=0,
        help="decrease verbosity")
parser.add_argument("-c", dest="exprstr", action="store",
        help="evaluate this expression and exit")
options = parser.parse_args()
verbosity = 10 * max(0, min(3 - options.verbose + options.silent, 5))

# logging configuration
stdout = logging.StreamHandler()
stdout.formatter = logging.Formatter("[{levelname}] <{name}> {message}", style="{")
logging.root.handlers.clear()
logging.root.addHandler(stdout)
logging.root.setLevel(verbosity)
logger = logging.getLogger('expr')


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
            if logger.isEnabledFor(logging.DEBUG):
                logger.error("Math error", exc_info=exc)
            else:
                print(exc, file=sys.stderr)
        except LarkError as exc:
            if logger.isEnabledFor(logging.DEBUG):
                logger.error("Syntax error", exc_info=exc)
            else:
                print(str(exc).partition('\n')[0], file=sys.stderr)


def eval(exprstr):
    tree = expr.parse(exprstr)
    expr.eval_numbers(tree)
    expr.eval_booleans(tree)
    expr.type_checker(tree)
    expr.compute(tree)
    return tree.meta.value


if options.exprstr:
    try:
        print(eval(options.exprstr))
    except (ArithmeticError, TypeError) as exc:
        if logger.isEnabledFor(logging.DEBUG):
            logger.error("Math error", exc_info=exc)
        sys.exit(exc)
    except LarkError as exc:
        if logger.isEnabledFor(logging.DEBUG):
            logger.error("Syntax error", exc_info=exc)
        sys.exit(str(exc).partition('\n')[0])
else:
    repl()

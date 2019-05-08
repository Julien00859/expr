#!/usr/bin/env python3

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

from parser import parser

print("Welcome to this very simple REPL.")
print("Evaluate an empty expression to quit.")
while True:
    expr = input("? ")
    if not expr:
        break
    tree = parser.parse(expr)
    print(tree.pretty())

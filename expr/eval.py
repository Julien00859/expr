from . import visitor
from .parser import parser


def eval(expr):
    tree = parser.parse(expr)
    visitor.eval_numbers(tree)
    visitor.eval_booleans(tree)
    visitor.type_checker(tree)
    visitor.compute(tree)
    return tree.meta.value

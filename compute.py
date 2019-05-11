import operator
from logging import getLogger
from lark.lexer import Token
from visitor import _get_token

logger = getLogger(__name__)


def logic_and(a, b):
    return a and b


def logic_or(a, b):
    return a or b


def get_op(op_name):
    if op_name == "and":
        return logic_and
    elif op_name == "or":
        return logic_or
    return getattr(operator, op_name)




def compute(tree):
    logger.debug("Computing...")
    for node in tree.iter_subtrees():
        if len(node.children) == 0:
            pass
        elif len(node.children) == 1:
            if not isinstance(node.children[0], Token):
                node.meta.value = node.children[0].meta.value
        elif len(node.children) == 2:
            op = get_op(_get_token(node.children[0]).type.lower())
            node.meta.value = op(node.children[1].meta.value)
        else:
            op = get_op(_get_token(node.children[1]).type.lower())
            node.meta.value = op(node.children[0].meta.value,
                                 node.children[2].meta.value)
    logger.debug("Done!")


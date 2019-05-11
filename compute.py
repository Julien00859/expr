import operator
from logging import getLogger
from lark.lexer import Token


logger = getLogger(__name__)

def get_token(node):
    while not isinstance(node, Token):
        node = node.children[0]
    return node

def compute(tree):
    logger.debug("Computing...")
    for node in tree.iter_subtrees():
        if len(node.children) == 0:
            pass
        elif len(node.children) == 1:
            if not isinstance(node.children[0], Token):
                node.meta.value = node.children[0].meta.value
        elif len(node.children) == 2:
            op = getattr(operator, get_token(node.children[0]).type.lower())
            node.meta.value = op(node.children[1].meta.value)
        else:
            op = getattr(operator, get_token(node.children[1]).type.lower())
            node.meta.value = op(node.children[0].meta.value,
                                 node.children[2].meta.value)
    logger.debug("Done!")


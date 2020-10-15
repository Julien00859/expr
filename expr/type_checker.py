from logging import getLogger
from lark.lexer import Token
from expr.utils import get_token

logger = getLogger(__name__)


class TypeError_(TypeError):
    msg1 = "unsupported operand type for {}: {}."
    msg2 = "unsupported operand types for {}: {} and {}."
    def __init__(self, op, child1, child2=None):
        type1 = TypeError_.type_to_str(child1.meta.type)
        if child2:
            type2 = TypeError_.type_to_str(child2.meta.type)
            msg = TypeError_.msg2.format(op, type1, type2)
        else:
            msg = TypeError_.msg1.format(op, type1)
        super().__init__(msg)

    @staticmethod
    def type_to_str(type_):
        if type_ is int:
            return 'int'
        if type_ is bool:
            return 'bool'
        return 'unknown'


def _require_type(children, type_):
    for child in children:
        if isinstance(child, Token):
            continue
        if not hasattr(child.meta, "type"):
            continue
        if child.meta.type == type_:
            continue

        if len(children) == 2:
            raise TypeError_(get_token(children[0]).value, children[1])
        elif len(children) == 3:
            raise TypeError_(get_token(children[1]).value, children[0], children[2])


def type_checker(tree):
    logger.debug("Checking types...")
    for node in tree.iter_subtrees():
        if len(node.children) == 1:
            if not isinstance(node.children[0], Token):
                node.meta.type = node.children[0].meta.type
        elif node.data.startswith("logical"):
            node.meta.type = bool
            _require_type(node.children, bool)
        elif node.data == "comparison":
            node.meta.type = bool
            _require_type(node.children, int)
        elif node.data.startswith("bitwise"):
            node.meta.type = int
            _require_type(node.children, int)
        elif node.data.startswith("arith"):
            node.meta.type = int
            _require_type(node.children, int)

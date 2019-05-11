from logging import getLogger
from lark.lexer import Token

logger = getLogger(__name__)

orders = {
    "hex_number": 16,
    "dec_number": 10,
    "oct_number": 8,
    "bin_number": 2,
}
values = {l: v for v, l in enumerate("0123456789abcdef")}


def eval_numbers(tree):
    logger.debug("Evaluating numbers...")
    for number in tree.find_data("number"):
        unit = orders[number.children[0].data]
        number.meta.type = int
        number.meta.value = 0
        for digit in number.children[0].children:
            number.meta.value *= unit
            number.meta.value += values[digit.value.lower()]
        number.children = []


def eval_booleans(tree):
    logger.debug("Evaluating booleans...")
    for boolean in tree.find_data("boolean"):
        boolean.meta.type = bool
        boolean.meta.value = boolean.children[0].value == "true"
        boolean.children = []


def _require_type(children, type_):
    for child in children:
        if isinstance(child, Token):
            continue
        if not hasattr(child.meta, "type"):
            continue
        if child.meta.type == type_:
            continue

        raise TypeError("Child {} is type {} but type {} is required.".format(
            child, child.meta.type, type_))


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

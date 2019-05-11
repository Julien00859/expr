from logging import getLogger

logger = getLogger(__name__)

values = {l: v for v, l in enumerate("0123456789abcdef")}
orders = {
    "hex_number": 16,
    "dec_number": 10,
    "oct_number": 8,
    "bin_number": 2,
}


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
        boolean.meta.value = boolean.children[0].type == "TRUE"
        boolean.children = []

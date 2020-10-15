from expr.eval_values import eval_numbers, eval_booleans
from expr.type_checker import type_checker
from expr.compute import compute
parse = __import__('expr.parser').parser.parser.parse

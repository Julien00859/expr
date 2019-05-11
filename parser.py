from logging import getLogger
from os.path import dirname, join as pathjoin
from lark import Lark

logger = getLogger(__name__)

logger.debug("Loading grammar...")
with open(pathjoin(dirname(__file__), "grammar.lark")) as fd:
    gram = fd.read()

parser = Lark(gram, parser="lalr", start="expression")
logger.debug("Loaded.")

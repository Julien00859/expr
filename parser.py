from logging import getLogger
from lark import Lark

logger = getLogger(__name__)

logger.info("Loading grammar...")
with open("grammar.lark") as fd:
    gram = fd.read()

parser = Lark(gram, parser="lalr", start="expression", debug=True)
logger.info("Loaded.")

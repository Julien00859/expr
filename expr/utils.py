from lark.lexer import Token

def get_token(node):
    while not isinstance(node, Token):
        node = node.children[0]
    return node

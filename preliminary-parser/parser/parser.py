from parser.parser_handlers import Node, parse_node

class ParserState:
    def __init__(self, tokens, grammar):
        self.tokens = tokens
        self.grammar = grammar
        self.index = 0

def parse_syntax(tokens, grammar):
    # initialize parser state
    parser = ParserState(tokens, grammar)

    # parse root as child of super root
    super_root = Node("super_root")
    parse_node(parser, "root", super_root)

    # return root
    return super_root.children[0]

from parser.grammar import Terminal, Optional, Alternative, Concatenation

class Node:
    def __init__(self, name=None, children=None):
        self.name = name
        self.children = children or []

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def remove_children(self):
        self.children = []

class ParserState:
    def __init__(self, tokens, grammar):
        self.tokens = tokens
        self.grammar = grammar
        self.index = 0

def parse_terminal(parser, terminal, parent_node, name):
    # raise error if a terminal was expected but eof reached
    if parser.index == len(parser.tokens):
        raise SyntaxError("Unexpected end of file")

    # resolve token
    token = parser.tokens[parser.index]

    # check if token matches terminal criteria
    if not terminal.matches_token(token):
        raise SyntaxError("Unexpected token")

    # if token is named, wrap in named node
    if name is None:
        parent_node.add_child(token)
    else:
        parent_node.add_child(Node(name, [token]))

    # consume token
    parser.index += 1

def parse_concatenation(parser, concatenation, parent_node, name):
    concatenation_node = Node(name or "unnamed concatenation")

    # parse each element in the concatenation
    for element in concatenation.elements:
        parse_node(parser, element, concatenation_node)

    parent_node.add_child(concatenation_node)

def parse_node(parser, production, parent_node, name=None):
    # resolve references to named productions
    while isinstance(production, str):
        name = name or production

        if name not in parser.grammar:
            raise ReferenceError("Unresolved reference \"{}\"".format(name))

        production = parser.grammar[name]

    handler_dict = {
        Terminal: parse_terminal,
        Optional: None,
        Alternative: None,
        Concatenation: parse_concatenation
    }

    handler_dict[type(production)](parser, production, parent_node, name)

def parse_syntax(tokens, grammar):
    # initialize parser state
    parser = ParserState(tokens, grammar)

    # parse root as child of super root
    super_root = Node("super_root")
    parse_node(parser, "root", super_root)

    # return root
    return super_root

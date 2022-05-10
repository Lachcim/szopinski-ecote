from parser.productions import Terminal, Concatenation, OptionalConcatenation, Optional, Alternative

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

def parse_node(parser, production, parent_node, name=None):
    # resolve references to named productions
    while isinstance(production, str):
        name = name or production

        if name not in parser.grammar:
            raise ReferenceError("Unresolved reference \"{}\"".format(name))

        production = parser.grammar[name]

    handler_dict = {
        Terminal: parse_terminal,
        Concatenation: parse_concatenation,
        Optional: parse_optional,
        OptionalConcatenation: parse_optional_concatenation,
        Alternative: parse_alternative
    }

    handler_dict[type(production)](parser, production, parent_node, name)

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

    # parse both elements in the concatenation
    for element in concatenation.elements:
        parse_node(parser, element, concatenation_node)

    parent_node.add_child(concatenation_node)

def parse_optional_concatenation(parser, optional_concat, parent_node, name):
    optional_concat_node = Node(name or "unnamed optional concatenation")
    initial_index = parser.index

    # try to concatenate both elements
    try:
        for element in optional_concat.elements:
            parse_node(parser, element, optional_concat_node)

        parent_node.add_child(optional_concat_node)
        return
    except SyntaxError:
        pass

    # restore index and try without the optional element
    optional_concat_node = Node(name or "unnamed optional concatenation")
    parser.index = initial_index

    parse_node(parser, optional_concat.elements[1], optional_concat_node)

    parent_node.add_child(optional_concat_node)

def parse_alternative(parser, alternative, parent_node, name):
    alternative_node = Node(name or "unnamed alternative")
    initial_index = parser.index

    # try to parse first option
    try:
        parse_node(parser, alternative.elements[0], alternative_node)

        parent_node.add_child(alternative_node)
        return
    except SyntaxError:
        pass

    # restore index and try to parse second option
    alternative_node = Node(name or "unnamed alternative")
    parser.index = initial_index

    parse_node(parser, alternative.elements[1], alternative_node)

    parent_node.add_child(alternative_node)

def parse_optional(parser, optional, parent_node, name):
    optional_node = Node(name or "unnamed optional")
    initial_index = parser.index

    # try to parse optional element, don't propagate failure
    try:
        parse_node(parser, optional.element, optional_node)

        parent_node.add_child(optional_node)
        return
    except SyntaxError:
        pass

    # upon failure, restore initial index
    parser.index = initial_index
    parent_node.add_child(optional_node)

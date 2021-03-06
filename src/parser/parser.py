from parser.productions import SuperRoot

class Node:
    def __init__(self):
        self.name = None
        self.production = None
        self.parent = None
        self.initial_index = None
        self.children = []

    def add_child(self, child, index=None):
        child.parent = self

        if index is None or index == len(self.children):
            self.children.append(child)
        else:
            self.children[index].parent = None
            self.children[index] = child

    def remove_children(self):
        for child in self.children:
            child.parent = None

        self.children = []

    def resolve_child(self, *indices):
        indices = list(indices)
        index = indices.pop(0)

        try:
            if len(indices) == 0:
                return self.children[index]

            return self.children[index].resolve_child(*indices)
        except IndexError:
            return None

class ParseError(Exception):
    def __init__(self, message, origin):
        super().__init__(message)
        self.origin = origin

class Parser:
    def __init__(self, tokens, grammar):
        # register token sequence and grammar for this parser
        self.tokens = tokens
        self.grammar = grammar
        self.active_node = None
        self.previous_node = None
        self.index = 0

        # create super root
        super_root = Node()
        super_root.name = "super root"
        super_root.production = SuperRoot("root")
        self.super_root = super_root
        self.active_node = super_root

        # initialize node history for backtracking
        self.branch_points = []
        self.backtracking = False

        # initialize error state
        self.error = None
        self.error_origin = None

    def create_node(self, production):
        # if the production argument is a string, let it become the name
        name = production if isinstance(production, str) else None

        # resolve production by name
        while isinstance(production, str):
            production = self.grammar[production]

        # return empty node
        node = Node()
        node.production = production
        node.name = name
        return node

    def advance(self):
        try:
            # delegate advancement logic to Production subclass
            previous_node = self.active_node
            self.active_node = self.active_node.production.advance(self.active_node, self)
            self.previous_node = previous_node
        except SyntaxError:
            # nowhere to backtrack to
            if len(self.branch_points) == 0:
                raise ParseError(self.error, self.error_origin)

            # backtrack on error
            self.active_node = self.branch_points[-1]
            self.backtracking = True

    def parse(self):
        # advance until exit from super root
        while self.active_node is not None:
            self.advance()

        # return root
        return self.super_root.children[0]

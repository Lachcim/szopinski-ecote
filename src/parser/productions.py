# interface for production subclasses
class Production:
    def __init__(self, *elements):
        self.elements = elements

    def advance(self):
        raise NotImplementedError

class Terminal(Production):
    def __init__(self, token_type, token_value=None):
        self.elements = None
        self.token_type = token_type
        self.token_value = token_value

    def matches_token(self, token):
        # compare token types
        if self.token_type is not None and self.token_type != token.type:
            return False

        # compare token values
        if self.token_value is not None and self.token_value != token.value:
            return False

        return True

    def advance(self, node, parser):
        # check for end of input
        if parser.index == len(parser.tokens):
            if parser.error is None:
                parser.error = "Unexpected end of input"
                parser.error_origin = parser.tokens[-1]

            # invoke backtrack
            raise SyntaxError

        # check if able to consume token
        token = parser.tokens[parser.index]
        if not self.matches_token(token):
            if parser.error is None:
                parser.error = "Unexpected token, expected {}".format(self.token_value or self.token_type)
                parser.error_origin = token

            # invoke backtrack
            raise SyntaxError

        # successful consumption resets error
        parser.error = None
        parser.error_origin = None

        # update parser and node state
        parser.index += 1
        node.add_child(token)

        # return to parent node
        return node.parent

class Concatenation(Production):
    def __init__(self, element1, element2):
        super().__init__(element1, element2)

    def advance(self, node, parser):
        # return to parent if returning from right child
        if len(node.children) == 2 and parser.previous_node is node.children[1]:
            return node.parent

        # create node for left or right child and queue for parsing
        child_index = 0 if parser.previous_node is node.parent else 1
        child_production = self.elements[child_index]
        child = parser.create_node(child_production)

        node.add_child(child, child_index)
        return child

class Optional(Production):
    def __init__(self, element):
        super().__init__(element)

    def advance(self, node, parser):
        if parser.backtracking:
            # if backtracking, restore initial state and unregister branch point
            node.remove_children()
            parser.index = node.initial_index
            parser.branch_points.remove(node)
            parser.backtracking = False

        if parser.previous_node is node.parent:
            # if entering for the first time, remember initial state and register branch point
            node.initial_index = parser.index
            parser.branch_points.append(node)

            # create node for child and queue for parsing
            child = parser.create_node(self.elements[0])
            node.add_child(child)
            return child

        # if returning from child, return to parent
        return node.parent

class Alternative(Production):
    def __init__(self, element1, element2):
        super().__init__(element1, element2)

    def advance(self, node, parser):
        if parser.backtracking:
            # if backtracking, restore initial state and unregister branch point
            node.remove_children()
            parser.index = node.initial_index
            parser.branch_points.remove(node)
            parser.backtracking = False

            # create node for path B and queue for parsing
            child_b = parser.create_node(self.elements[1])
            node.add_child(child_b)
            return child_b

        if parser.previous_node is node.parent:
            # if entering for the first time, remember initial state and register branch point
            node.initial_index = parser.index
            parser.branch_points.append(node)

            # create node for path A and queue for parsing
            child_a = parser.create_node(self.elements[0])
            node.add_child(child_a)
            return child_a

        # if returning from child, return to parent
        return node.parent

class SuperRoot(Production):
    def __init__(self, element):
        super().__init__(element)

    def advance(self, node, parser):
        # when entering for the first time, create root element
        if parser.previous_node is None:
            root_node = parser.create_node(self.elements[0])
            node.add_child(root_node)
            return root_node

        # if returning from root, check if all tokens have been parsed
        if parser.index < len(parser.tokens):
            parser.error = "Unparsed tokens"
            parser.error_origin = parser.tokens[parser.index]

            # invoke backtrack
            raise SyntaxError

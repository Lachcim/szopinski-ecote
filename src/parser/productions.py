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
        node.stage += 1

        # return to parent node
        parser.active_node = node.parent

class Concatenation(Production):
    def __init__(self, element1, element2):
        super().__init__(element1, element2)

    def advance(self, node, parser):
        # return to parent if returning from right child
        if node.stage == 2:
            parser.active_node = node.parent
            return

        # create node for left or right child, depending on stage
        child_production = self.elements[node.stage]
        child = parser.create_node(child_production)
        node.add_child(child)

        # queue child for parsing
        parser.active_node = child
        node.stage += 1

class Optional(Production):
    def __init__(self, element):
        super().__init__(element)

class Alternative(Production):
    def __init__(self, element1, element2):
        super().__init__(element1, element2)

class SuperRoot(Production):
    def __init__(self, element):
        super().__init__(element)

    def advance(self, node, parser):
        # in initial stage, create root element
        if node.stage == 0:
            root_node = parser.create_node(self.elements[0])
            node.add_child(root_node)

            # queue root for parsing
            parser.active_node = root_node
            node.stage += 1
            return

        # if returning from root, check if all tokens have been parsed
        if parser.index < len(parser.tokens):
            parser.error = "Unparsed tokens"
            parser.error_origin = parser.tokens[parser.index]

            # invoke backtrack
            raise SyntaxError

        # finish parsing
        parser.active_node = None

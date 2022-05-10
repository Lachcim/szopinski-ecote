class Terminal:
    def __init__(self, token_type, token_value=None):
        self.token_type = token_type
        self.token_value = token_value

    def matches_token(self, token):
        # compare token types
        if self.token_type != token.type:
            return False

        # compare token values, no token value = wildcard
        if self.token_value is not None and self.token_value != token.value:
            return False

        return True

class Concatenation:
    def __init__(self, element1, element2):
        self.elements = [element1, element2]

class Optional:
    def __init__(self, element):
        self.element = element

class OptionalConcatenation:
    def __init__(self, optional, mandatory):
        self.elements = [optional, mandatory]

class Alternative:
    def __init__(self, *elements):
        self.elements = elements

# define grammar for the grammar definition file
meta_grammar = {
    "root": Concatenation(
        Terminal("identifier", "alpha"),
        OptionalConcatenation(
            OptionalConcatenation(
                Terminal("identifier", "beta"),
                Optional(Terminal("identifier", "gamma"))
            ),
            Terminal("identifier", "delta")
        )
    )
}

# generate grammar from the syntax tree of a grammar definition file
def generate_grammar(syntax_tree):
    pass

class Terminal:
    def __init__(self, token_type, token_value=None):
        self.token_type = token_type
        self.token_value = token_value

class Optional:
    def __init__(self, value):
        self.value = value

class Alternative:
    def __init__(self, *values):
        self.values = values

class Concatenation:
    def __init__(self, *values):
        self.values = values

# define grammar for the grammar definition file
meta_grammar = {
    "root": Optional("definitions"),
    "definitions": Concatenation("definition", Optional("definitions")),
    "definition": Concatenation(
        Terminal("identifier"),
        Terminal("auxillary", "="),
        "expression",
        Terminal("auxillary", ";")
    ),
    "expression": Concatenation(
        Alternative(
            Terminal("identifier"),
            Terminal("string_literal"),
            Terminal("identifier", "identifier"),
            Terminal("identifier", "string_literal"),
            Terminal("identifier", "number_literal"),
            "operator"
        ),
        Optional("expression")
    ),
    "operator": Alternative("optional_operator", "alternative_operator"),
    "optional_operator": Concatenation(
        Terminal("identifier", "optional"),
        Terminal("auxillary", "("),
        "expression",
        Terminal("auxillary", ")"),
    ),
    "alternative_operator": Concatenation(
        Terminal("identifier", "alternative"),
        Terminal("auxillary", "("),
        "argument_list",
        Terminal("auxillary", ")"),
    ),
    "argument_list": Concatenation(
        "expression",
        Optional(
            Concatenation(
                Terminal("auxillary", ","),
                "argument_list"
            )
        )
    )
}

# generate grammar from the syntax tree of a grammar definition file
def generate_grammar(syntax_tree):
    pass

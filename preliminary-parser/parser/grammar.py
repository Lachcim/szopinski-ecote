from parser.productions import Terminal, Concatenation, OptionalConcatenation, Optional, Alternative

# define grammar for the grammar definition file
meta_grammar = {
    "root": Concatenation(
        Terminal("identifier", "alpha"),
        Alternative(
            Terminal("identifier", "sralfa"),
            Terminal("identifier", "dupalfa")
        )
    )
}

# generate grammar from the syntax tree of a grammar definition file
def generate_grammar(syntax_tree):
    pass

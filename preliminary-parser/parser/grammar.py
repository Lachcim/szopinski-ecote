from parser.productions import Terminal, Concatenation, OptionalConcatenation, Optional, Alternative

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

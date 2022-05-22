from parser.productions import Terminal, Concatenation, Optional, Alternative

# define grammar for the grammar definition file
meta_grammar = {
    "root": Concatenation(
        Optional(
            Terminal("identifier", "alpha")
        ),
        Concatenation(
            Terminal("identifier", "alpha"),
            Terminal("identifier", "beta")
        )
    )
}

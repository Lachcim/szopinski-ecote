from parser.productions import Terminal, Concatenation, Alternative

# define grammar for the grammar definition file
meta_grammar = {
    "root": Concatenation(
        Terminal("identifier", "dupa"),
        Terminal("identifier", "trupa")
    )
}

from parser.productions import Terminal, Concatenation, OptionalConcatenation, Alternative

# define grammar for the grammar definition file
meta_grammar = {
    "root": Alternative(
        "definitions",
        Terminal("end_of_file")
    ),
    "definitions": Concatenation(
        "definition",
        Alternative(
            "definitions",
            Terminal("end_of_file")
        )
    ),
    "definition": Concatenation(
        Terminal("identifier"),
        Concatenation(
            Terminal("auxillary", "="),
            Concatenation(
                "expression",
                Terminal("auxillary", ";")
            )
        )
    ),
    "expression": Alternative(
        "concat_expression",
        Alternative(
            "opt_concat_expression",
            Alternative(
                "alt_expression",
                Alternative(
                    Terminal("identifier"),
                    Alternative(
                        Terminal("string_literal"),
                        Alternative(
                            Terminal("identifier", "identifier"),
                            Alternative(
                                Terminal("identifier", "string_literal"),
                                Alternative(
                                    Terminal("identifier", "number_literal"),
                                    Terminal("identifier", "end_of_file")
                                )
                            )
                        )
                    )
                )
            )
        )
    ),
    "concat_expression": Concatenation(
        Terminal("identifier", "concat"),
        "argument"
    ),
    "opt_concat_expression": Concatenation(
        Terminal("identifier", "opt_concat"),
        "argument"
    ),
    "opt_concat_expression": Concatenation(
        Terminal("identifier", "opt_concat"),
        "argument"
    ),
    "alt_expression": Concatenation(
        Terminal("identifier", "alt"),
        "argument"
    ),
    "argument": Concatenation(
        Terminal("auxillary", "("),
        Concatenation(
            "expression",
            Concatenation(
                Terminal("auxillary", ","),
                Concatenation(
                    "expression",
                    Terminal("auxillary", ")")
                )
            )
        )
    )
}

# generate grammar from the syntax tree of a grammar definition file
def generate_grammar(syntax_tree):
    pass

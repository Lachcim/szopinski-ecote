from parser.productions import Terminal, Concatenation, Alternative

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
        "definition_key",
        Concatenation(
            Terminal("auxillary", "="),
            Concatenation(
                "definition_expression",
                Terminal("auxillary", ";")
            )
        )
    ),
    "definition_key": Terminal("identifier"),
    "definition_expression": "expression",
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
    "alt_expression": Concatenation(
        Terminal("identifier", "alt"),
        "argument"
    ),
    "argument": Concatenation(
        Terminal("auxillary", "("),
        Concatenation(
            "arg1",
            Concatenation(
                Terminal("auxillary", ","),
                Concatenation(
                    "arg2",
                    Terminal("auxillary", ")")
                )
            )
        )
    ),
    "arg1": "expression",
    "arg2": "expression"
}

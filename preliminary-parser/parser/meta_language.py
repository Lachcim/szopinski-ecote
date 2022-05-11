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
                    "expr_identifier",
                    "expr_string_literal"
                )
            )
        )
    ),
    "expr_identifier": Terminal("identifier"),
    "expr_string_literal": Terminal("string_literal"),
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
            "expr_arg1",
            Concatenation(
                Terminal("auxillary", ","),
                Concatenation(
                    "expr_arg2",
                    Terminal("auxillary", ")")
                )
            )
        )
    ),
    "expr_arg1": "expression",
    "expr_arg2": "expression"
}

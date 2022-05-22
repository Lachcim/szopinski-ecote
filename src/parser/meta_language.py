from parser.productions import Terminal, Concatenation, Optional, Alternative

# define grammar for the grammar definition file
meta_grammar = {
    "root": Optional("definitions"),
    "definitions": Concatenation(
        "definition",
        Optional("definitions")
    ),
    "definition": Concatenation(
        "definition_key",
        Concatenation(
            Terminal("operator", "="),
            Concatenation(
                "definition_value",
                Terminal("separator", ";")
            )
        )
    ),
    "definition_key": Terminal("identifier"),
    "definition_value": "expression",
    "expression": Alternative(
        Alternative(
            Terminal("identifier"),
            Alternative(
                Terminal("string_literal"),
                Terminal("identifier", "identifier")
            )
        ),
        Alternative(
            Terminal("identifier", "string_literal"),
            Alternative(
                Terminal("identifier", "number_literal"),
                "operator"
            )
        )
    ),
    "operator": Alternative(
        "opt_operator",
        Alternative(
            "concat_operator",
            "alt_operator"
        )
    ),
    "opt_operator": Concatenation(
        Terminal("identifier", "opt"),
        "single_arg"
    ),
    "concat_operator": Concatenation(
        Terminal("identifier", "concat"),
        "double_arg"
    ),
    "alt_operator": Concatenation(
        Terminal("identifier", "alt"),
        "double_arg"
    ),
    "single_arg": Concatenation(
        Terminal("separator", "("),
        Concatenation(
            "arg1",
            Terminal("separator", ")"),
        )
    ),
    "double_arg": Concatenation(
        Terminal("separator", "("),
        Concatenation(
            "arg1",
            Concatenation(
                Terminal("separator", ","),
                Concatenation(
                    "arg2",
                    Terminal("separator", ")")
                )
            )
        )
    ),
    "arg1": "expression",
    "arg2": "expression"
}

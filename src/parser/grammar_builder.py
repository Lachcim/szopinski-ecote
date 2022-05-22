from parser.diagnostic import print_tree
from parser.lexer_handlers import Token
from parser.productions import Terminal, Concatenation, Optional, Alternative

reserved_identifiers = set([
    "identifier",
    "string_literal",
    "number_literal",
    "opt",
    "concat",
    "alt"
])

def parse_expression(node, used_identifiers):
    # resolve base expression type
    while not isinstance(node, Token) and not node.name == "operator":
        node = node.children[0]

    if isinstance(node, Token):
        # string literals evaluate to tokens of the given value
        if node.type == "string_literal":
            return Terminal(None, node.value[1:-1])

        # reserved identifiers evaluate to tokens of the given type
        if node.value in ["identifier", "string_literal", "number_literal"]:
            return Terminal(node.value, None)

        # other identifiers are references to other productions
        used_identifiers.add(node.value)
        return node.value

    # single-argument operator
    if node.children[0].name == "opt_operator":
        arg = parse_expression(node.resolve_child(0, 1, 1, 0), used_identifiers)
        return Optional(arg)

    # double-argument operator
    arg1 = parse_expression(node.resolve_child(0, 0, 1, 1, 0), used_identifiers)
    arg2 = parse_expression(node.resolve_child(0, 0, 1, 1, 1, 1, 0), used_identifiers)

    prod_name = node.resolve_child(0, 0).name
    if prod_name == "concat_operator":
        return Concatenation(arg1, arg2)
    else:
        return Alternative(arg1, arg2)

# generate grammar from the syntax tree of a grammar definition file
def build_grammar(definitions):
    output = {}
    defined_identifiers = set()
    used_identifiers = set()

    # find and parse all definitions in parsed grammar file
    while definitions is not None:
        definition_key = definitions.resolve_child(0, 0, 0).value
        definition_value = definitions.resolve_child(0, 1, 1, 0)

        output[definition_key] = parse_expression(definition_value, used_identifiers)
        defined_identifiers.add(definition_key)

        # move to next definitions node, break if there are none
        definitions = definitions.resolve_child(1, 0)

    # require root definition
    if "root" not in defined_identifiers:
        raise NameError("Root element definition missing")

    # disallow overwriting reserved identifiers
    overwritten_reserved = used_identifiers.intersection(reserved_identifiers)
    for identifier in overwritten_reserved:
        raise NameError("Illegal production name {}".format(identifier))

    # disallow undefined references
    undefined_references = used_identifiers.difference(defined_identifiers)
    for identifier in undefined_references:
        raise NameError("Reference to {} is undefined".format(identifier))

    # disallow unused definitions
    defined_identifiers.remove("root")
    unused_definitions = defined_identifiers.difference(used_identifiers)
    for identifier in unused_definitions:
        raise NameError("Production {} is defined but never used".format(identifier))

    return output

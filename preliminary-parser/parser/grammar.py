from parser.parser_handlers import Node
from parser.meta_language import meta_grammar
from parser.productions import Terminal, Concatenation, OptionalConcatenation, Alternative

argumented_productions = [
    "concat_expression",
    "opt_concat_expression",
    "alt_expression"
]
terminal_productions = [
    "expr_identifier",
    "expr_string_literal"
]
all_productions = argumented_productions + terminal_productions

reserved_identifiers = [
    "identifier",
    "string_literal",
    "number_literal",
    "end_of_file"
    "concat",
    "opt_concat",
    "alt"
]

def find_all_nodes(node, name):
    output = []

    # if node matches name, add it to the output
    if node.name == name:
        output.append(node)

    # recurse over children
    for child in node.children:
        if isinstance(child, Node):
            output += find_all_nodes(child, name)

    return output

def find_first_node(node, *names):
    # if node matches name list, return it
    if node.name in names:
        return node

    # recurse over children
    for child in node.children:
        if isinstance(child, Node):
            result = find_first_node(child, *names)
            if result is not None:
                return result

    return None

def parse_production(node):
    # find base production in definition
    base_prod_node = find_first_node(node, *all_productions)
    base_prod_name = base_prod_node.name

    # resolve terminal productions
    if base_prod_name in terminal_productions:
        # string literals evaluate to tokens with the given value
        if base_prod_name == "expr_string_literal":
            return Terminal(None, base_prod_node.children[0].value)

        # reserved identifiers evaluate to tokens of the given type
        identifier = base_prod_node.children[0].value
        if identifier in reserved_identifiers:
            return Terminal(identifier)

        # arbitrary identifiers evaluate to references
        return base_prod_node.children[0].value

    # resolve production class
    argumented_prod_classes = {
        "concat_expression": Concatenation,
        "opt_concat_expression": OptionalConcatenation,
        "alt_expression": Alternative
    }
    base_production = argumented_prod_classes[base_prod_name]

    # resolve arguments
    arg1 = parse_production(find_first_node(base_prod_node, "expr_arg1"))
    arg2 = parse_production(find_first_node(base_prod_node, "expr_arg2"))

    return base_production(arg1, arg2)

# generate grammar from the syntax tree of a grammar definition file
def generate_grammar(syntax_tree):
    output = {}

    # find all definitions in parsed grammar file
    definition_nodes = find_all_nodes(syntax_tree, "definition")

    # parse definition nodes into productions
    for definition_node in definition_nodes:
        production_name = find_first_node(definition_node, "definition_key").children[0].value
        production_expression = find_first_node(definition_node, "definition_expression").children[0]

        # protect reserved identifiers
        if production_name in reserved_identifiers:
            raise ValueError("Must not override reserved identifier \"{}\"".format(production_name))

        # translate syntax tree into production
        output[production_name] = parse_production(production_expression)

    # require root definition
    if "root" not in output:
        raise ValueError("Must define root element")

    return output

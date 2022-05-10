from parser.parser_handlers import Node
from parser.diagnostic import print_tree

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

def find_first_node(node, name):
    # if node matches name, return it
    if node.name == name:
        return node

    # recurse over children
    for child in node.children:
        if isinstance(child, Node):
            result = find_first_node(child, name)
            if result is not None:
                return result

    return None

# generate grammar from the syntax tree of a grammar definition file
def generate_grammar(syntax_tree):
    output = {}

    # find all definitions in parsed grammar file
    definition_nodes = find_all_nodes(syntax_tree, "definition")

    # parse definition nodes into productions
    for definition_node in definition_nodes:
        production_name = find_first_node(definition_node, "definition_key").children[0].value
        production_expression = find_first_node(definition_node, "definition_expression").children[0]

        print(production_name)
        print_tree(production_expression)

    return output

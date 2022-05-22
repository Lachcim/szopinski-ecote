import os
import sys

from parser.parser import Node

def has_lexer_errors(tokens):
    # check if tokenized input contains invalid tokens
    for token in tokens:
        if token.type == "invalid":
            return True

    return False

def print_lexer_errors(tokens, input, file_path):
    for token in tokens:
        if token.type == "invalid":
            print_diagnostic(
                input,
                file_path,
                token.position,
                token.length,
                "Invalid token"
            )

def print_diagnostic(input, file_path, index, length, error):
    line_start = input.rfind("\n", 0, index) + 1
    line_end = input.find("\n", line_start)
    line_end = line_end if line_end != -1 else len(input)
    error_start = index - line_start
    file_name = os.path.basename(file_path)
    line_no = input.count("\n", 0, index) + 1

    print("Error in {}, line {}:".format(file_name, line_no), file=sys.stderr)
    print(input[line_start:line_end], file=sys.stderr)
    print("{}{}".format(error_start * " ", length * "^"), file=sys.stderr)
    print("{}{}".format(error_start * " ", error), file=sys.stderr)

def print_tree(node, indent=0):
    spaces = "    " * indent
    production_name = type(node.production).__name__

    if node.name is not None:
        print("{}{} ({}):".format(spaces, node.name, production_name))
    else:
        print("{}Unnamed {}:".format(spaces, production_name))

    for item in node.children:
        if isinstance(item, Node):
            print_tree(item, indent + 1)
        else:
            print("{}Terminal token: {} {}".format("    " * (indent + 1), item.type, item.value))

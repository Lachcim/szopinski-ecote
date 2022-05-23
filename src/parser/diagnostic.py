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
    # print diagnostic for each invalid token
    for token in tokens:
        if token.type == "invalid":
            print_diagnostic(
                input,
                file_path,
                token.position,
                token.length,
                "Invalid token"
            )

def print_parser_error(error, input, file_path):
    # print diagnostic for parser error
    print_diagnostic(
        input,
        file_path,
        error.origin.position if error.origin is not None else 0,
        error.origin.length if error.origin is not None else 1,
        error
    )

def print_semantic_error(error, file_path):
    file_name = os.path.basename(file_path)

    print("Error in {}:".format(file_name), file=sys.stderr)
    print(error, file=sys.stderr)

def print_diagnostic(input, file_path, index, length, error):
    # print line containing error together with error message
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

def print_tree(node, active_node, indent=0, flatten=False, interactive=False):
    spaces = "    " * indent
    production_name = type(node.production).__name__
    active_indicator = " <---" if node is active_node else ""

    if indent == 0:
        if flatten and active_node.name is None:
            return
        if interactive:
            os.system("cls" if os.name == "nt" else "clear")

    if node.name is not None:
        print("{}{} ({}):{}".format(spaces, node.name, production_name, active_indicator))
    else:
        if not flatten:
            print("{}Unnamed {}:{}".format(spaces, production_name, active_indicator))
        else:
            indent -= 1

    for item in node.children:
        if isinstance(item, Node):
            print_tree(item, active_node, indent + 1, flatten=flatten)
        else:
            print("{}Token: {} {}".format("    " * (indent + 1), item.type, item.value))

    # pause execution in interactive mode, otherwise print newline after tree
    if indent == 0:
        if interactive:
            input()
        else:
            print()

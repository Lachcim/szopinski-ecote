import os
import sys

from parser.lexer_handlers import Token
from parser.productions import Terminal

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

def print_tree(node, parser, indent=0, collapse=False, interactive=False):
    # top-level entry checks
    if indent == 0:
        # in collapse mode, don't print if the active node is not going to be displayed
        if collapse and parser.active_node and parser.active_node.name is None:
            return

        # in interactive mode, clear the screen before printing
        if interactive:
            os.system("cls" if os.name == "nt" else "clear")

    indent_spaces = "    " * indent
    active_indicator = " <---" if node is parser.active_node else ""

    # for tokens, print their type and value
    if isinstance(node, Token):
        token_value = "\"{}\"".format(node.value) if node.type != "string_literal" else node.value
        print("{}token {} ({})".format(indent_spaces, token_value, node.type))
        return

    # in collapse mode, skip this node if unnamed
    if collapse and node.name is None:
        for child in node.children:
            print_tree(child, parser, indent, collapse)
        return

    # obtain a string describing the production
    production_desc = type(node.production).__name__

    # for terminal productions, specify consumption requirements
    if isinstance(node.production, Terminal):
        token_type = node.production.token_type
        token_value = node.production.token_value

        if token_type is not None and token_value is not None:
            production_desc += " of type {} and value \"{}\"".format(token_type, token_value)
        elif token_type is not None:
            production_desc += " of type {}".format(token_type)
        elif token_value is not None:
            production_desc += " of value \"{}\"".format(token_value)
        else:
            production_desc += " of any type and value"

    # obtain a string describing the node
    if node.name is None:
        node_desc = "unnamed {}".format(production_desc)
    else:
        node_desc = "{} ({})".format(node.name, production_desc)

    # print node description
    print("{}{}:{}".format(indent_spaces, node_desc, active_indicator))

    # print children
    for child in node.children:
        print_tree(child, parser, indent + 1, collapse)

    # exit check: in interactive mode, prompt for input before continuing
    if indent == 0 and interactive:
        input()

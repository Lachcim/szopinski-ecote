import argparse

from parser.lexer import scan_and_evaluate
from parser.diagnostic import has_lexer_errors, print_lexer_errors, print_tree
from parser.diagnostic import print_parser_error, print_semantic_error
from parser.parser import Parser, ParseError
from parser.meta_language import meta_grammar
from parser.grammar_builder import build_grammar

# parse input arguments
arg_parser = argparse.ArgumentParser(description="Parse a file using the given grammar.")
arg_parser.add_argument("grammar_file", help="path to the file containing the grammar definition")
arg_parser.add_argument("input_file", help="path to the file to be parsed")
arg_parser.add_argument("-c", "--collapse",
    help="collapse unnamed nodes",
    action="store_true"
)
arg_parser.add_argument("-i", "--interactive",
    help="clear screen and step through the tree manually",
    action="store_true"
)
arg_parser.add_argument("-f", "--final",
    help="only print the final state of the tree",
    action="store_true"
)
args = arg_parser.parse_args()

# utility functions
def read_file_contents(path):
    with open(path, "r") as f:
        file_contents = f.read()
        file_contents = file_contents.replace("\t", "    ")
        return file_contents

def print_tree_step(parser, final_step=False):
    if args.final and not final_step:
        return
    print_tree(parser.super_root, parser, collapse=args.collapse, interactive=args.interactive)
    if not args.interactive and not final_step:
        print()

# read files
grammar_file_raw = read_file_contents(args.grammar_file)
input_file_raw = read_file_contents(args.input_file)

# tokenize grammar file
grammar_tokens = scan_and_evaluate(grammar_file_raw)
if has_lexer_errors(grammar_tokens):
    print_lexer_errors(grammar_tokens, grammar_file_raw, args.grammar_file)
    exit(1)

try:
    # parse grammar file using grammar definition metalanguage
    grammar_parser = Parser(grammar_tokens, meta_grammar)
    grammar_syntax_tree = grammar_parser.parse()
except ParseError as error:
    print_parser_error(error, grammar_file_raw, args.grammar_file)
    exit(2)

try:
    # build grammar description object from the grammar file's syntax tree
    grammar = build_grammar(grammar_syntax_tree)
except NameError as error:
    print_semantic_error(error, args.grammar_file)
    exit(3)

# tokenize input file
input_tokens = scan_and_evaluate(input_file_raw)
if has_lexer_errors(input_tokens):
    print_lexer_errors(input_tokens, input_file_raw, args.input_file)
    exit(4)

# create parser using input tokens and the obtained grammar
parser = Parser(input_tokens, grammar)
print_tree_step(parser)

# step until parser exits from super root
while parser.active_node is not None:
    try:
        parser.advance()
        print_tree_step(parser, final_step=parser.active_node is None)
    except ParseError as error:
        print_parser_error(error, input_file_raw, args.input_file)
        exit(5)

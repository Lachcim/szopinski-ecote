import sys
from parser.lexer import scan_and_evaluate
from parser.diagnostic import has_lexer_errors, print_lexer_errors
from parser.diagnostic import print_parser_error, print_semantic_error
from parser.parser import Parser, ParseError
from parser.meta_language import meta_grammar
from parser.grammar_builder import build_grammar

def read_file_contents(path):
    with open(path, "r") as f:
        file_contents = f.read()
        file_contents = file_contents.replace("\t", "    ")
        return file_contents

# print usage information
if len(sys.argv) < 3:
    print("Usage: python preliminary_parser.py [grammar file] [input file]")
    exit()

# read files
grammar_file_path = sys.argv[1]
grammar_file_raw = read_file_contents(grammar_file_path)
input_file_path = sys.argv[2]
input_file_raw = read_file_contents(input_file_path)

# tokenize grammar file
grammar_tokens = scan_and_evaluate(grammar_file_raw)
if has_lexer_errors(grammar_tokens):
    print_lexer_errors(grammar_tokens, grammar_file_raw, grammar_file_path)
    exit(1)

try:
    # parse grammar file using grammar definition metalanguage
    grammar_parser = Parser(grammar_tokens, meta_grammar)
    grammar_syntax_tree = grammar_parser.parse()
except ParseError as error:
    print_parser_error(error, grammar_file_raw, grammar_file_path)
    exit(2)

try:
    # build grammar description object from the grammar file's syntax tree
    grammar = build_grammar(grammar_syntax_tree)
except NameError as error:
    print_semantic_error(error, grammar_file_path)
    exit(3)

print(grammar["root"])
print(grammar["root"].elements[0].token_value)
print(grammar["root"].elements[1].token_value)

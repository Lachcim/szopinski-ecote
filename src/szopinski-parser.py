import sys
from parser.lexer import scan_and_evaluate
from parser.diagnostic import has_lexer_errors, print_lexer_errors
from parser.diagnostic import print_parser_error, print_tree
from parser.parser import Parser, ParseError
from parser.meta_language import meta_grammar

# print usage information
if len(sys.argv) < 3:
    print("Usage: python preliminary_parser.py [grammar file] [input file]")
    exit()

# read files
grammar_file_path = sys.argv[1]
input_file_path = sys.argv[2]

with open(grammar_file_path, "r") as f:
    grammar_file_raw = f.read()
    grammar_file_raw = grammar_file_raw.replace("\t", "    ")
with open(input_file_path, "r") as f:
    input_file_raw = f.read().replace("\t", "    ")
    input_file_raw = input_file_raw.replace("\t", "    ")

# tokenize grammar file
grammar_tokens = scan_and_evaluate(grammar_file_raw)

if has_lexer_errors(grammar_tokens):
    print_lexer_errors(grammar_tokens, grammar_file_raw, grammar_file_path)
    exit(1)

try:
    # parse grammar file using grammar definition metalanguage
    grammar_parser = Parser(grammar_tokens, meta_grammar)
    grammar_parser.parse()
except ParseError as e:
    print_parser_error(e, grammar_file_raw, grammar_file_path)
    exit(1)

print_tree(grammar_parser.super_root)

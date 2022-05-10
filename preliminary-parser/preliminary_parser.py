import sys
from parser.lexer import scan_and_evaluate
from parser.diagnostic import diagnose_lexer_errors
from parser.grammar import meta_grammar, generate_grammar

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
if diagnose_lexer_errors(grammar_tokens, grammar_file_raw, grammar_file_path):
    exit(1)

# szopinski-ecote

My implementation of the ECOTE project for Ms Derezińska, PhD. It is a state-of-the-art top-down parser with backtracking. Accepts a grammar description file and validates the specified input file against it. Prints diagnostic messages and shows the evolution of the syntax tree.

```
usage: szopinski-parser.py [-h] [-f] [-i] grammar_file input_file

Parse a file using the given grammar.

positional arguments:
  grammar_file       path to the file containing the grammar definition
  input_file         path to the file to be parsed

optional arguments:
  -h, --help         show this help message and exit
  -f, --flatten      don't print unnamed nodes
  -i, --interactive  clear screen and step through the tree manually
```

Check <a href="/src/parser/meta_language.py">meta_language.py</a> for the grammar of the grammar definition file.

from parser.lexer import scan_and_evaluate

input = """
"jezus" & "maria" & 123.
"""

output = scan_and_evaluate(input)

print("Found {} tokens:".format(len(output)))

for token in output:
    print("{}: `{}`".format(token.type, token.value))

from parser.lexer import scan_and_evaluate

input = """
+++ 5.5"jezus" && "5"
"""

output = scan_and_evaluate(input)

print("Found {} tokens:".format(len(output)))

for token in output:
    print("{}: `{}`".format(token.type, token.value))

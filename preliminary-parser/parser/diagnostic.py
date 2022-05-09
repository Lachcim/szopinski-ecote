import os
import sys

def diagnose_lexer_errors(tokens, input, file_path):
    output = False

    # check if tokenized input contains invalid tokens
    for token in tokens:
        if token.type == "invalid":
            print_diagnostic(
                input,
                file_path,
                token.position,
                token.length,
                "Invalid token"
            )
            output = True

    return output

def print_diagnostic(input, file_path, index, length, error):
    line_start = input.rfind("\n", 0, index) + 1
    line_end = input.find("\n", line_start)
    line_end = line_end if line_end != -1 else len(input)
    error_start = index - line_start
    file_name = os.path.basename(file_path)

    print("Error in {}, line {}:".format(file_name), file=sys.stderr)
    print(input[line_start:line_end], file=sys.stderr)
    print("{}{}".format(error_start * " ", length * "^"), file=sys.stderr)
    print("{}{}".format(error_start * " ", error), file=sys.stderr)

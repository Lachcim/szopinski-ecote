import string

class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position
        self.length = len(value)

identifier_start = string.ascii_letters + "_"
identifier_cont = identifier_start + string.digits
separator_chars = "(),;[]{}"
operator_chars = "!#$%&*+-./:<=>?@\\^`|~"
string_delimiters = "\"'"

def get_char(input, i):
    return input[i] if i >= 0 and i < len(input) else None

def handle_new_token(machine_state, i, input, output):
    char = get_char(input, i)

    # EOF reached
    if char is None:
        return

    # whitespace separates tokens
    if char in string.whitespace:
        machine_state.token_type = None
        return

    # mark token start
    machine_state.token_start = i

    # identify token type
    if char in string_delimiters:
        machine_state.token_type = "string_literal"
    elif char in string.digits:
        machine_state.token_type = "number_literal"
    elif char in identifier_start:
        machine_state.token_type = "identifier"
    elif char in separator_chars:
        machine_state.token_type = "separator"
    elif char in operator_chars:
        machine_state.token_type = "operator"

def handle_string_literal(machine_state, i, input, output):
    char = get_char(input, i)

    # string must end before EOF or EOL
    if char in [None, "\r", "\n"]:
        lexeme = input[machine_state.token_start:i]
        output.append(Token("invalid", lexeme, machine_state.token_start))

        machine_state.token_type = None
        machine_state.string_escape = False

    # backslash enables escape for the next character
    if char == "\\" and not machine_state.string_escape:
        machine_state.string_escape = True
        return

    # can't terminate if character is escaped
    if machine_state.string_escape:
        machine_state.string_escape = False
        return

    # string terminates on the same quote that it started on
    if char == input[machine_state.token_start]:
        lexeme = input[machine_state.token_start:(i + 1)]
        output.append(Token("string_literal", lexeme, machine_state.token_start))
        machine_state.token_type = None
        return

def handle_number_literal(machine_state, i, input, output):
    char = get_char(input, i)

    if char is not None:
        # digits always allowed
        if char in string.digits:
            return

        # allow single decimal point
        if char == ".":
            if not machine_state.decimal_point_consumed:
                machine_state.decimal_point_consumed = True
            else:
                # dot belongs to operator and marks the end of this literal
                lexeme = input[machine_state.token_start:i]
                output.append(Token("number_literal", lexeme, machine_state.token_start))

                machine_state.token_start = i
                machine_state.token_type = "operator"

            return

        # must be separated from succeeding identifier
        if char in identifier_cont:
            machine_state.decimal_point_consumed = False
            machine_state.token_type = "invalid"
            return

    # non-digit, non-dot, non-identifier terminates the literal
    lexeme = input[machine_state.token_start:i]
    output.append(Token("number_literal", lexeme, machine_state.token_start))

    machine_state.decimal_point_consumed = False
    machine_state.token_type = None
    machine_state.rescan = True

def handle_identifier(machine_state, i, input, output):
    char = get_char(input, i)

    # non-alphanumeric, non-underscore terminates the identifier
    if char is None or char not in identifier_cont:
        lexeme = input[machine_state.token_start:i]
        output.append(Token("identifier", lexeme, machine_state.token_start))

        machine_state.token_type = None
        machine_state.rescan = True

def handle_separator(machine_state, i, input, output):
    # separators only take a single character
    lexeme = input[machine_state.token_start:i]
    output.append(Token("separator", lexeme, machine_state.token_start))

    machine_state.token_type = None
    machine_state.rescan = True

def handle_operator(machine_state, i, input, output):
    char = get_char(input, i)

    # non-alphanumeric, non-underscore terminates the identifier
    if char is None or char not in operator_chars:
        lexeme = input[machine_state.token_start:i]
        output.append(Token("operator", lexeme, machine_state.token_start))

        machine_state.token_type = None
        machine_state.rescan = True

def handle_invalid(machine_state, i, input, output):
    char = get_char(input, i)

    # invalid tokens terminate on whitespace or EOF
    if char is None or char in string.whitespace:
        lexeme = input[machine_state.token_start:i]
        output.append(Token("invalid", lexeme, machine_state.token_start))
        machine_state.token_type = None

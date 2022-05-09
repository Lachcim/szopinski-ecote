class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position

def get_char(input, i):
    return input[i] if i < len(input) else None

def handle_auxillary(machine_state, i, input, output):
    char = get_char(input, i)

    # all auxillary tokens are single-character
    output.append(Token("auxillary", char, machine_state.token_start))
    machine_state.token_type = None

def handle_new_token(machine_state, i, input, output):
    char = get_char(input, i)

    # EOF reached
    if char is None:
        return

    # whitespace separates tokens
    if char in " \t\r\n\v\f":
        machine_state.token_type = None
        return

    # mark token start
    machine_state.token_start = i

    # identify token type
    if char in "\"'":
        machine_state.token_type = "string-literal"
    elif char in "0123456789":
        machine_state.token_type = "number-literal"
    elif char == "+-.":
        machine_state.token_type = "aux-or-number"
    elif char == "/":
        machine_state.token_type = "aux-or-comment"
    elif (char.lower() >= "a" and char.lower() <= "z") or char == "_":
        machine_state.token_type = "identifier"
    else:
        # failed to match against multi-character token types, must be auxillary token
        handle_auxillary(machine_state, i, input, output)

def handle_string_literal(machine_state, i, input, output):
    char = get_char(input, i)

    # string must end before EOF or EOL
    if char in [None, "\r", "\n"]:
        literal = input[machine_state.token_start:i]
        output.append(Token("invalid", literal, machine_state.token_start))

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
        literal = input[machine_state.token_start:(i + 1)]
        output.append(Token("string-literal", literal, machine_state.token_start))
        machine_state.token_type = None
        return

def handle_number_literal(machine_state, i, input, output):
    char = get_char(input, i)

    # digits always allowed
    if char in "0123456789":
        return

    # allow single decimal point
    if char == ".":
        if not machine_state.decimal_point_consumed:
            machine_state.decimal_point_consumed = True
        else:
            # dot belongs to auxillary token and marks the end of this literal
            literal = input[machine_state.token_start:i]
            output.append(Token("number-literal", literal, machine_state.token_start))

            machine_state.token_start = i
            machine_state.decimal_point_consumed = False

            # add auxillary token to output and reset token type
            handle_auxillary(machine_state, i, input, output)

        return

    # must be separated from succeeding identifier
    if (char.lower() >= "a" and char.lower() <= "z") or char == "_":
        machine_state.token_type = "invalid"
        return

    # non-digit, non-dot terminates the literal
    literal = input[machine_state.token_start:i]
    output.append(Token("number-literal", literal, machine_state.token_start))
    machine_state.decimal_point_consumed = False
    machine_state.token_type = None

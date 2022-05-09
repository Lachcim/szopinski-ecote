class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position

def get_char(input, i):
    return input[i] if i < len(input) else None

def get_prev_char(input, i):
    input[i - 1] if i > 0 else None

def get_initial_token_type(machine_state, i, input, output):
    char = get_char(input, i)

    # EOF reached
    if char is None:
        return

    # whitespace separates tokens
    if char in " \t\r\n\v\f":
        machine_state.token_type = None
        return

    # identify token type
    if char in "\"'":
        machine_state.token_type = "string-literal"
    elif char in "0123456789":
        machine_state.token_type = "number-literal"
    elif char in "+-":
        machine_state.token_type = "aux-or-number"
    elif char == "/":
        machine_state.token_type = "aux-or-comment"
    elif (char.lower() >= "a" and char.lower() <= "z") or char == "_":
        machine_state.token_type = "identifier"
    else:
        machine_state.token_type = "auxillary"

    # mark token start
    machine_state.token_start = i

def handle_string_literal(machine_state, i, input, output):
    char = get_char(input, i)

    # backslash enables escape for the next character
    if char == "\\" and not machine_state.string_escape:
        machine_state.string_escape = True
        return

    # escaped character is included in the string at all times
    if machine_state.string_escape:
        machine_state.string_escape = False
        return

    # string ends on the same quote that it started on
    if char == input[machine_state.token_start]:
        literal = input[machine_state.token_start:(i + 1)]
        output.append(Token("string-literal", literal, machine_state.token_start))
        machine_state.token_type = None
        return

    # string must end before EOF or EOL
    if char is None or char in "\r\n":
        literal = input[machine_state.token_start:i]
        output.append(Token("invalid", literal, machine_state.token_start))
        machine_state.token_type = None

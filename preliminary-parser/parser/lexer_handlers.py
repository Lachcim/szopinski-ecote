class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position
        self.length = len(value)

def get_char(input, i):
    return input[i] if i >= 0 and i < len(input) else None

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
        machine_state.token_type = "string_literal"
    elif char in "0123456789":
        machine_state.token_type = "number_literal"
    elif (char.lower() >= "a" and char.lower() <= "z") or char == "_":
        machine_state.token_type = "identifier"
    else:
        machine_state.token_type = "auxillary"

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

    # digits always allowed
    if char in "0123456789":
        return

    # allow single decimal point
    if char == ".":
        if not machine_state.decimal_point_consumed:
            machine_state.decimal_point_consumed = True
        else:
            # dot belongs to auxillary token and marks the end of this literal
            lexeme = input[machine_state.token_start:i]
            output.append(Token("number_literal", lexeme, machine_state.token_start))

            machine_state.token_start = i
            machine_state.token_type = "auxillary"

        return

    # must be separated from succeeding identifier
    if (char.lower() >= "a" and char.lower() <= "z") or char == "_":
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
    pass

def handle_auxillary(machine_state, i, input, output):
    char = get_char(input, i)

    # transition into number literal
    if char in "0123456789" and get_char(input, i - 1) in ["+", "-", "."]:
        # output true auxillary part
        if i - machine_state.token_start > 1:
            lexeme = input[machine_state.token_start:(i - 1)]
            output.append(Token("auxillary", lexeme, machine_state.token_start))

        machine_state.token_start = i - 1
        machine_state.token_type = "number_literal"
        return

    # terminate on identifier, number, string or whitespace
    if (char.lower() >= "a" and char.lower() <= "z") or char in "_0123456789\"' \t\r\n\v\f":
        lexeme = input[machine_state.token_start:i]
        output.append(Token("auxillary", lexeme, machine_state.token_start))

        machine_state.token_type = None
        machine_state.rescan = char not in " \t\r\n\v\f"

def handle_invalid(machine_state, i, input, output):
    char = get_char(input, i)

    # invalid tokens terminate on whitespace or EOF
    if char is None or char in " \t\r\n\v\f":
        lexeme = input[machine_state.token_start:i]
        output.append(Token("invalid", lexeme, machine_state.token_start))
        machine_state.token_type = None

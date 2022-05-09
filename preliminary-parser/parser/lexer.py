from parser.lexer_handlers import handle_new_token
from parser.lexer_handlers import handle_string_literal
from parser.lexer_handlers import handle_number_literal

class MachineState:
    token_start = None
    token_type = None
    string_escape = False
    decimal_point_consumed = False

def scan_and_evaluate(input):
    # initialize output array and finite state machine
    output = []
    machine_state = MachineState()

    # dictionary of handlers for various token types
    handlers = {
        None: handle_new_token,
        "string-literal": handle_string_literal,
        "number-literal": handle_number_literal
    }

    # iterate over input string
    for i in range(len(input) + 1):
        # call handler for the current token type
        handlers[machine_state.token_type](
            machine_state,
            i,
            input,
            output
        )

    return output

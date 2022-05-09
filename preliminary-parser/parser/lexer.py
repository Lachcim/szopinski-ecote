from parser.lexer_handlers import get_initial_token_type
from parser.lexer_handlers import handle_string_literal

class MachineState:
    token_start = None
    token_type = None
    string_escape = False

def scan_and_evaluate(input):
    # initialize output array and finite state machine
    output = []
    machine_state = MachineState()

    # dictionary of handlers for various token types
    handlers = {
        None: get_initial_token_type,
        "string-literal": handle_string_literal
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

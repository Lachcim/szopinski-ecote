from parser.token import Token
from parser.lexer_handlers import handle_new_token
from parser.lexer_handlers import handle_string_literal
from parser.lexer_handlers import handle_number_literal
from parser.lexer_handlers import handle_identifier
from parser.lexer_handlers import handle_auxillary
from parser.lexer_handlers import handle_invalid

class MachineState:
    token_start = None
    token_type = None
    rescan = False
    string_escape = False
    decimal_point_consumed = False

def scan_and_evaluate(input):
    # initialize output array and finite state machine
    output = []
    machine_state = MachineState()

    # dictionary of handlers for various token types
    handlers = {
        None: handle_new_token,
        "string_literal": handle_string_literal,
        "number_literal": handle_number_literal,
        "identifier": handle_identifier,
        "auxillary": handle_auxillary,
        "invalid": handle_invalid
    }

    # iterate over input string
    for i in range(len(input) + 1):
        while True:
            # call handler for the current token type
            handlers[machine_state.token_type](
                machine_state,
                i,
                input,
                output
            )

            # rescan if requested
            if not machine_state.rescan:
                break
            machine_state.rescan = False

    # add end of file token
    output.append(Token("end_of_file", "", len(input)))

    return output

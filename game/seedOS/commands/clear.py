"""
Clear the screen.
"""
from game.seedOS import create_command
from game.seedOS.console import send_messages
from game.terminal.screen import clear_screen, get_screen_size


def get_clear_command():
    """
    Get the dictionary data for the clear command.

    :postcondition: get the data for the clear command
    :return: a dictionary representing the data for the clear command
    """
    return create_command(
        name="clear",
        run=run_clear,
        privilege_required=0)


def run_clear(seed_system, tokens):
    """
    Run the clear command.

    Clears the screen and moves up message_history

    :param seed_system: a dictionary representing the currently active seedOS system
    :param tokens: a list of strings representing the arguments passed in to the command
    :precondition: seed_system must be a well-formed seed_system dictionary
    :precondition: tokens must be a list of strings
    :postcondition: clear the terminal and console screens
    :return: a tuple of 2 strings representing the success status and a status message
    """
    status = "success"
    if tokens:
        status = "argument_error"
        status_message = f"|'clear' expects no arguments|\n{len(tokens)} > 0"
    else:
        clear_screen()
        send_messages(seed_system, ["" for _ in range(get_screen_size()[1])], 0)
        status_message = "|Cleared the screen|"
    return (status, status_message)

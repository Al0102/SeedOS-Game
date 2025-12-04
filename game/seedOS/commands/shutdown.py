"""
Turn off the game.
"""
from game.seedOS import create_command


def get_shutdown_command():
    """
    Get the dictionary data for the shutdown command.

    :postcondition: get the data for the shutdown command
    :return: a dictionary representing the data for the shutdown command
    """
    return create_command(
        name="shutdown",
        run=run_shutdown,
        privilege_required=0)


def run_shutdown(seed_system, tokens):
    """
    Run the shutdown command.

    :param seed_system: a dictionary representing the currently active seedOS system
    :param tokens: a list of strings representing the arguments passed in to the command
    :precondition: seed_system must be a well-formed seed_system dictionary
    :precondition: tokens must be a list of strings
    :postcondition: change the active program of <seed_system> to "seedos_shutdown"
    :return: a tuple of 2 strings representing the success status and a status message
    """
    status = "success"
    if tokens:
        status = "argument_error"
        status_message = f"|'shutdown' expects no arguments|\n{len(tokens)} > 0"
    else:
        seed_system["active_program"] = "seedos_shutdown"
        status_message = "|Shutting down system|"
    return (status, status_message)

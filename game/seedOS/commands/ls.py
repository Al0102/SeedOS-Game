"""
Clear the screen.
"""
from game.ansi_actions.style import style
from game.seedOS import create_command
from game.seedOS.console import send_messages, send_message
from game.seedOS.files import get_folder_contents


def get_ls_command():
    """
    Get the dictionary data for the ls command.

    :postcondition: get the data for the ls command
    :return: a dictionary representing the data for the ls command
    """
    return create_command(
        name="ls",
        run=run_ls,
        privilege_required=0)


def run_ls(seed_system, tokens):
    """
    Run the ls command.

    Display contents of current working directory.

    :param seed_system: a dictionary representing the currently active seedOS system
    :param tokens: a list of strings representing the arguments passed in to the command
    :precondition: seed_system must be a well-formed seed_system dictionary
    :precondition: tokens must be a list of strings
    :postcondition: display contents of current working directory.
    :return: a tuple of 2 strings representing the success status and a status message
    """
    status = "success"
    if tokens:
        status = "argument_error"
        status_message = f"|'ls' expects no arguments|\n{len(tokens)} > 0"
    else:
        send_message(
            seed_system,
            style(f"{seed_system['aphid']['current_folder']}/", 'underline', 'yellow'))
        send_messages(
            seed_system,
            get_folder_contents(seed_system, seed_system["aphid"]["current_folder"]))
        status_message = f"|Displayed directory contents|\n{seed_system['aphid']['current_folder']}"
    return (status, status_message)

"""
Shows the contents of the current working folder.
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

    Display the contents of current working folder.

    :param seed_system: a dictionary representing the currently active seedOS system
    :param tokens: a list of strings representing the arguments passed in to the command
    :precondition: seed_system must be a well-formed seed_system dictionary
    :precondition: tokens must be a list of strings
    :postcondition: display the contents of current working folder
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
        contents = get_folder_contents(seed_system, seed_system["aphid"]["current_folder"], full_path=True)
        formatted = tuple(map(lambda file_path: format_ls_item(seed_system, file_path), contents))
        send_messages(
            seed_system, formatted)
        status_message = "|Displayed folder contents|"
    return (status, status_message)

def format_ls_item(seed_system, full_path):
    """
    Return a path formatted to be displayed with ls.

    :param seed_system: a dictionary representing the currently active seedOS system
    :param full_path: an absolute path string representing a path
    :precondition: seed_system must be a well-formed seed_system dictionary
    :precondition: file_path must be a path-like string with tokens separated by "/"
    :postcondition: format the information about <full_path> for displaying it with ls
    :return: a string representing the formatted file information
    """
    content = seed_system["file_tree"][full_path]
    name = content["name"]
    if content["type"] == "file":
        name = f"{name}.{content["extension"]}"
    return f"{style(name, 'bold')} - {content['type']}"

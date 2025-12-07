"""
Change current working folder.
"""
from game.ansi_actions.style import style
from game.seedOS import create_command
from game.seedOS.files import convert_relative_path_to_absolute


def get_cd_command():
    """
    Get the dictionary data for the cd command.

    :postcondition: get the data for the cd command
    :return: a dictionary representing the data for the cd command
    """
    return create_command(
        name="cd",
        run=run_cd,
        privilege_required=0)


def run_cd(seed_system, tokens):
    """
    Run the cd command.

    Change the current working folder.

    :param seed_system: a dictionary representing the currently active seedOS system
    :param tokens: a list of strings representing the arguments passed in to the command
    :precondition: seed_system must be a well-formed seed_system dictionary
    :precondition: tokens must be a list of strings
    :postcondition: change the current working folder
    :return: a tuple of 2 strings representing the success status and a status message
    """
    status = "success"
    if len(tokens) > 1:
        status = "argument_error"
        status_message = f"|'cd' expects at most 1 argument: [path]|\n{len(tokens)} > 1"
    elif len(tokens) == 1:
        new_path = convert_relative_path_to_absolute(seed_system["aphid"]["current_folder"], tokens[0])
        if not new_path in seed_system["file_tree"].keys():
            status = "argument_error"
            status_message = f"|Invalid path|\n{style(new_path, 'underline')}"
        elif seed_system["file_tree"][new_path]["type"] != "folder":
            status = "argument_error"
            status_message = f"|Path must be a folder|\n{style(new_path, 'underline')}"
        elif seed_system["file_tree"][new_path]["privilege_required"] > seed_system["aphid"]["privilege"]:
            status = "privilege_error"
            status_message = (
                "|Privilege too low|\n"
                f"{seed_system['aphid']['privilege']} < {seed_system['file_tree'][new_path]['privilege_required']}")
        else:
            seed_system["aphid"]["current_folder"] = new_path
            status_message = f"|Changed folder to path|\n{style(new_path, 'underline')}"
    else:
        seed_system["aphid"]["current_folder"] = "seed"
        status_message = f"|Changed folder to root|\n{style('seed', 'underline')}"
    return (status, status_message)



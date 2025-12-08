"""
Look at the content of a text file.
"""
from game.ansi_actions.style import style
from game.seedOS import create_command
from game.seedOS.files import convert_relative_path_to_absolute


def get_do_command():
    """
    Get the dictionary data for the do command.

    :postcondition: get the data for the do command
    :return: a dictionary representing the data for the do command
    """
    return create_command(
        name="do",
        run=run_do,
        privilege_required=2)


def run_do(seed_system, tokens):
    """
    Run the do command.

    Look through the content of a text file.

    :param seed_system: a dictionary representing the currently active seedOS system
    :param tokens: a list of strings representing the arguments passed in to the command
    :precondition: seed_system must be a well-formed seed_system dictionary
    :precondition: tokens must be a list of strings
    :postcondition: do through the content of a text file
    :return: a tuple of 2 strings representing the success status and a status message
    """
    status = "success"
    if len(tokens) != 1:
        status = "argument_error"
        status_message = f"|'do' expects exactly 1 argument: [path]|\n{len(tokens)} != 1"
    else:
        new_path = convert_relative_path_to_absolute(seed_system["aphid"]["current_folder"], tokens[0])
        try:
            path_data = seed_system["file_tree"][new_path]
        except KeyError:
            status = "argument_error"
            status_message = f"|Invalid path|\n{style(new_path, 'underline')}"
        else:
            if path_data["type"] != "file" or path_data["extension"] != "sprout":
                status = "argument_error"
                status_message = f"|Can't run this file|\n{style(new_path, 'underline')}"
            elif path_data["privilege_required"] > seed_system["aphid"]["privilege"]:
                status = "privilege_error"
                status_message = (
                    "|Privilege too low|\n"
                    f"{seed_system['aphid']['privilege']} < {path_data['privilege_required']}")
            else:
                seed_system["active_program"] = "seedos_burrow" if "board_src" in path_data["data"] else "seedos_unlock"
                seed_system["active_file"] = path_data
                status_message = f"|Ran the file|\n{style(new_path, 'underline')}"
    return (status, status_message)



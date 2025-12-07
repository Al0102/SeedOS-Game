"""
Terminal simulator.
"""
from game.seedOS.command import create_command
from game.seedOS.commands.command_root import create_command_root
from game.seedOS.files import create_file_tree


def init_seed_system():
    """
    Return a seedOS data dictionary.

    The seedOS dictionary has the form:
    {
        "aphid": <dictionary of aphid data or None>,
        "command_root": <dictionary of command data>,
        "file_tree": <dictionary of file tree data>,
        "message_history": <list of string outputs to seedOS console>,
        "active_program": <string program (scene) name or None for seedos_console>
    }

    :postcondition: get a new seedOS data dictionary
    :return: a dictionary representing new seedOS data
    """
    return {
        "aphid": None,
        "command_root": create_command_root(),
        "file_tree": create_file_tree(),
        "message_history": [],
        "active_program": None}


def init_aphid(name):
    """
    Return a new APHID data dictionary.

    The APHID dictionary has the form:
    {
        "name": <string>,
        "privilege": <integer of aphid security clearance>,
        "current_folder": <string path of current folder>,
        "stability": <float from [0, 1] representing APHID health>}
    }

    :param name: a string representing the name of the APHID
    :precondition: aphid_name must be a string
    :postcondition: get a new APHID data dictionary
    :return: a dictionary representing new seedOS data
    """
    return {
        "name": name,
        "privilege": 0,
        "current_folder": "seed",
        "stability": 1}

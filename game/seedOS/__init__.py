"""
Terminal simulator.
"""
from game.seedOS.command import create_command
from game.seedOS.commands.command_root import create_command_root


def init_seed_system(aphid_name):
    """
    Return a seedOS data dictionary.

    The seedOS dictionary has the form:
    {
        "aphid": <dictionary of aphid data>,
        "command_root": <dictionary of command data>,
        "file_tree": <dictionary of file tree data>
    }

    :param aphid_name: a string representing the name of the system's APHID
    :precondition: aphid_name must be a string
    :postcondition: get a new seedOS data dictionary
    :return: a dictionary representing new seedOS data
    """
    return {
        "aphid": init_aphid(aphid_name),
        "command_root": create_command_root(),
        "file_tree": {}}


def init_aphid(name):
    """
    Return a new APHID data dictionary.

    The APHID dictionary has the form:
    {
        "name": <string>,
        "privilege": <integer of aphid security clearance>,
        "current_directory": <string path of current directory>,
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
        "current_directory": "seed",
        "stability": 1}

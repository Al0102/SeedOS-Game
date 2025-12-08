"""
Shows the APHID's current status
"""
from game.ansi_actions.style import style
from game.seedOS import create_command
from game.seedOS.console import send_messages, send_message
from game.seedOS.files import get_folder_contents


def get_aphid_command():
    """
    Get the dictionary data for the aphid command.

    :postcondition: get the data for the aphid command
    :return: a dictionary representing the data for the aphid command
    """
    return create_command(
        name="aphid",
        run=None,
        privilege_required=0,
        subcommands={
            "status": create_command(
                name="status",
                run=run_aphid_status,
                privilege_required=0), })
    # "upgrade": create_command(
    #     name="status",
    #     run=run_aphid_upgrade,
    #     privilege_required=2)})


def run_aphid_status(seed_system, tokens):
    """
    Run the aphid status command.

    Show the APHID's information.

    :param seed_system: a dictionary representing the currently active seedOS system
    :param tokens: a list of strings representing the arguments passed in to the command
    :precondition: seed_system must be a well-formed seed_system dictionary
    :precondition: tokens must be a list of strings
    :postcondition: display the APHID's status information
    :return: a tuple of 2 strings representing the success status and a status message
    """
    status = "success"
    if tokens:
        status = "argument_error"
        status_message = f"|'aphid status' expects no arguments|\n{len(tokens)} > 0"
    else:
        aphid_stability = seed_system['aphid']['stability']
        send_messages(seed_system, [
            f"Aphid: {style(seed_system['aphid']['name'], 'green')}",
            f"Privilege: {style(str(seed_system['aphid']['privilege']), 'yellow')}",
            f"Memory: {style(str(seed_system['aphid']['memory']), 'yellow')}kB",
            f"Stability: {style(str(aphid_stability * 100), 'green' if aphid_stability > 0.5 else 'red')}%",
            "Drivers:",
            *map(lambda driver: style(f"    {driver.upper()}", "blue"), seed_system["aphid"]["drivers"])])
        status_message = "|Showed APHID information|"
    return (status, status_message)

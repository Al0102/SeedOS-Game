"""
User interaction with SeedOS.
"""
from game.ansi_actions import style
from game.seedOS import get_built_in_commands


def get_commands(seed_system):
    return get_built_in_commands() | seed_system["packages"]["commands"]


def status_report(code, message):
    """
    Create a status report dictionary.

    :param code: a string representing the status code of a process
    :param message: a string representing the user readable status response to a process
    :precondition: code must be a string with a valid error code
    :precondition: message must be a string
    :postcondition: create a dictionary holding the status report of a process
    :postcondition: the dictionary will have a "code" and a "message" key
    :return: a dictionary representing the status report of a process

    >>> status_report("success","The process succeeded") == {
    ... "code": "success",
    ... "message": "The process succeeded"
    ... }
    True
    >>> status_report("invalid_syntax","The option, 'cach', does not exist") == {
    ... "code": "invalid_syntax",
    ... "message": "The option, 'cach', does not exist"
    ... }
    True
    """
    return {"code": code, "message": message}


def validate_command(seed_system, command_tokens):
    name = command_tokens[0]
    available_commands = get_commands(seed_system)
    if name not in available_commands.keys():
        return status_report("does_not_exist", style.style("Command does not exist!", "red"))
    command = available_commands[name]
    if seed_system["aphid"]["privilege"] < command["privilege_required"]:
        return status_report("privilege_too_low", style.style("Privileges are insufficient!", "red"))
    elif (syntax_status := command["validate_options"](seed_system, command_tokens[1:]))["code"] != "success":
        return status_report("invalid_syntax", style.style(syntax_status["message"], "red"))
    return status_report("success", style.style("Command succeeded!", "green"))


def send_command(seed_system, command):
    tokens = command.strip().split()
    status = validate_command(seed_system, tokens)
    if status["code"] != "success":
        output = [status["message"]]
        seed_system["message_history"] += output
        return output
    output = get_commands(seed_system)[tokens[0]]["call"](seed_system, tokens)
    seed_system["message_history"] += output
    return output
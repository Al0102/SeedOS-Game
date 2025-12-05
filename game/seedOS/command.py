"""
User interaction with SeedOS.
"""
from game.ansi_actions import style
from game.seedOS.console import send_messages, send_message


def get_status_styles():
    """
    Get a dictionary of statuses and their styles.

    :return: get a dictionary statuses and their styles
    :return: a dictionary representing statuses and their styles

    >>> get_status_styles() == {
    ...     "success": ("green", "dim"),
    ...     "system_error": ("background_red", "black", "rapid_blink"),
    ...     "syntax_error": ("red", "bold"),
    ...     "argument_error": ("red", "bold"),
    ...     "privilege_error": ("yellow", "bold")}
    True
    """
    return {
        "success": ("green", "dim"),
        "system_error": ("background_red", "black", "rapid_blink"),
        "syntax_error": ("red", "bold"),
        "argument_error": ("red", "bold"),
        "privilege_error": ("yellow", "bold")}


def run_command(seed_system, command_data, tokens):
    if seed_system["aphid"]["privilege"] < command_data["privilege_required"]:
        status = "privilege_error"
        status_message = ("|Privilege too low|\n" +
                          f"{seed_system['aphid']['privilege']} < {command_data['privilege_required']}")
    elif command_data["subcommands"]:
        try:
            next_command = command_data["subcommands"][tokens[0]]
        except IndexError:
            status = "argument_error"
            status_message = "|Expected a command|\nReceived nothing"
        except KeyError:
            status = "syntax_error"
            status_message = "|Could not find command|\n" + tokens[0]
        else:
            status, status_message = run_command(seed_system, next_command, tokens[1:])
    else:
        status, status_message = command_data["run"](seed_system, tokens)
    return (status, command_data["name"] + " -> " + status_message)


def send_command(seed_system, command_string):
    send_message(seed_system, f"> command_string")
    tokens = command_string.strip().split()
    status = status_report(
        *run_command(seed_system, seed_system["command_root"], tokens))
    send_messages(seed_system, status["message"].split("\n"))
    send_message(seed_system, "")
    return status

def create_command(name, run, privilege_required, subcommands=None):
    """
    Return the data for a new command.

    Command data has the form,
        "name": <str>
        "run": <callback>,
        "privilege_required": <int>,
        "subcommands": None or <dictionary of commands>

    :param name: a string representing the name of the command and how it is called
    :param run: a callback function representing the process to run for this command
    :param privilege_required: an integer representing the minimum clearance level needed to run the command
    :param subcommands: (default None) a dictionary representing potential subcommands for the command,
    :precondition: name must be a string
    :precondition: if the command is a subcommand, <name> should be the same as its index
    :precondition: run must be a callback function that returns a status and status message of its success
    :precondition: privilege_required must be an integer
    :precondition: subcomands must be a non-empty dictionary with key-value pairs of form,
                        <subcommand name>: <command dictionary>
                    or None if the command has no subcommands
    :postcondition: create a new command dictionary
    :return: a dictionary representing the data for a new command

    >>> run_function = lambda seed: ("success", "This create_command has been run!")
    >>> create_command("foo", run_function, 0) == {
    ...     "name": "foo",
    ...     "run": run_function,
    ...     "privilege_required": 0,
    ...     "subcommands": None}
    True
    >>> run_function = lambda seed: {"success": "This is fizzy!"}
    >>> create_command(
    ...     "fizz", run_function, 1, {
    ...         "foo": create_command("foo", run_function, 0),
    ...         "bar": create_command("bar", run_function, 5)}
    ... ) == {
    ...     "name": "fizz",
    ...     "run": run_function,
    ...     "privilege_required": 1,
    ...     "subcommands": {
    ...         "foo": create_command("foo", run_function, 0),
    ...         "bar": create_command("bar", run_function, 5)}}
    True
    """
    return {
        "name": name,
        "run": run,
        "subcommands": subcommands,
        "privilege_required": privilege_required,
    }


def status_report(code, message):
    """
    Create a status report dictionary with styled status message.

    :param code: a string representing the status code of a process
    :param message: a string representing the user readable status response to a process
    :precondition: code must be a string with a valid error code
    :precondition: message must be a string
    :postcondition: create a dictionary holding the status report of a process
    :postcondition: the dictionary will have a "code" and a "message" key
    :return: a dictionary representing the status report of a process
    >>> status_report("success", "The process succeeded") == {
    ... "code": "success",
    ... "message": "\\x1b[32m\\x1b[2mThe process succeeded\\x1b[0m"
    ... }
    True
    >>> status_report("syntax_error", "The option, 'cach', does not exist") == {
    ... "code": "syntax_error",
    ... "message": "\\x1b[31m\\033[1mThe option, 'cach', does not exist\\x1b[0m"
    ... }
    True
    """
    message = style.style(message, *get_status_styles()[code])
    return {"code": code, "message": message}


def main():
    mock_seed = {
        "aphid": {"name": "Clippy", "privilege": 0},
        "message_history": [],
        "command_root": create_command(
            name="command_root",
            run=lambda seed_system, tokens: print(f"{seed_system["aphid"]["name"]} reporting for duty.\n" +
                                                  f"Picked up: {tokens}"),
            privilege_required=0,
            subcommands={
                "say": create_command(
                    name="say",
                    run=lambda seed_system, tokens: print(seed_system["aphid"]["name"], *tokens),
                    privilege_required=1)})}
    print(
        mock_seed["command_root"]["run"](mock_seed, ["coin", "paperclip", "windowpane"]))
    print(send_command(mock_seed, "say hi"))


if __name__ == '__main__':
    main()
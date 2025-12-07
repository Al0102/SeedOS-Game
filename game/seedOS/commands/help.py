"""
Get documentation for SeedOS and installed package commands.
"""
import json

from game import relative_path
from game.ansi_actions.style import style
from game.seedOS.command import create_command
from game.seedOS.console import display_message_history, send_messages, send_message


def get_help_command():
    """
    Get the dictionary data for the help command.

    :postcondition: get the data for the help command
    :return: a dictionary representing the data for the help command
    """
    return create_command(
        name="help",
        run=run_help,
        privilege_required=0)


def run_help(seed_system, tokens):
    """
    Run the help command.

    :param seed_system: a dictionary representing the currently active seedOS system
    :param tokens: a list of strings representing the arguments passed in to the command
    :precondition: seed_system must be a well-formed seed_system dictionary
    :precondition: tokens must be a list of strings
    :postcondition: display help documentation
    :return: a tuple of 2 strings representing the success status and a status message
    """
    status = "success"
    try:
        with open(relative_path("seedOS/commands/help.json"), "r") as help_docs_file:
            try:
                help_json = json.load(help_docs_file)
            except json.JSONDecodeError as error:
                return ("system_error", f"|File corrupted|\nhelp.json decode error: {error}")
    except FileNotFoundError:
        return ("system_error", "|File corrupted|\nhelp.json not found")
    command_documents = {
        data["name"]: data for data in help_json if data["name"] in seed_system["command_root"]["subcommands"].keys()}
    if len(tokens) > 1:
        status = "argument_error"
        status_message = f"|'help' expects at most, 1 argument|\n{len(tokens)} > 1"
    elif len(tokens) == 1:
        try:
            command_help = command_documents[tokens[0]]
        except KeyError:
            status = "syntax_error"
            status_message = "|Could not find help document|\n" + tokens[0]
        else:
            send_messages(seed_system, format_long_description(command_help).split("\n"))
            status_message = f"|Showed help documentation|\n{tokens[0]}"
    else:
        for command_help in command_documents.values():
            send_message(seed_system, format_short_description(command_help))
        status_message = "|Listed available commands|"
    display_message_history(seed_system)
    return (status, status_message)


def format_short_description(command_help):
    """
    Return the formatted short form description of a command

    :param command_help: a dictionary representing the command's help documentation
    :precondition: command_data must be a dictionary with the following key-value-pairs,
                   "name": <str>
                   "options": <list of strings>
                   "short_description": <oneline string>
    :postcondition: get a string representing the formatted short form description of a command
    :return: a string representing the formatted short form description of a command

    >>> command = {
    ...     "name": "help", "options": ["[command]"],
    ...     "short_description": "List the built-in commands or get the documentation for a command"}
    >>> format_short_description(command)
    '\\x1b[1mhelp\\x1b[0m [command] - List the built-in commands or get the documentation for a command'
    """
    return (f"{style(command_help['name'], 'bold')} {' '.join(command_help['options'])} - "
            f"{command_help['short_description']}")


def format_long_description(command_help):
    """
    Return the formatted long form description of a command

    :param command_help: a dictionary representing the command's help documentation
    :precondition: command_data must be a dictionary with the following key-value-pairs,
                   "name": <str>
                   "options": <list of strings>
                   "short_description": <oneline string>
                   "long_description": <list of strings, each represent one line>
    :postcondition: get a string representing the formatted long form description of a command
    :return: a string representing the formatted long form description of a command

    >>> command = {
    ...     "name": "help", "options": ["[command]"],
    ...     "short_description": "List available commands or get the documentation for a command",
    ...     "long_description": [
    ...         "Syntax:",
    ...         "  help",
    ...         "  - list all available commands",
    ...         "  help [command]",
    ...         "  - get the help documentation for [command]"]}
    >>> format_long_description(command) == (
    ...    "\\x1b[4m\\x1b[1mhelp\\x1b[0m [command]\x1b[0m\\n"
    ...    "List available commands or get the documentation for a command\\n"
    ...    "Syntax:\\n"
    ...    "  help\\n  - list all available commands\\n"
    ...    "  help [command]\\n  - get the help documentation for [command]")
    True
    """
    title = style(
        f"{style(command_help['name'], 'bold')} {' '.join(command_help['options'])}",
        "underline")
    return f"{title}\n{command_help['short_description']}\n{'\n'.join(command_help['long_description'])}"


def main():
    """
    Drive the program.
    """
    mock_seed_system = {
        "message_history": [],
        "command_root": {
            "name": "command_root", "subcommands": {"help": get_help_command()}
        }
    }
    print(run_help(mock_seed_system, ["help"]))
    print(*mock_seed_system["message_history"], sep="\n")


if __name__ == "__main__":
    main()
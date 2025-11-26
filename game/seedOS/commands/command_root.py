"""
Base command of SeedOS, holds all available commands.
"""
from game.seedOS.command import create_command
from game.seedOS.commands.help import get_help_command


def create_command_root():
    return create_command(
        name="command_root",
        run=lambda seed_system, tokens: ("system_error", "|User running of command_root.sprout is prohibited|"),
        privilege_required=0,
        subcommands={
            "help": get_help_command(),
        }
    )
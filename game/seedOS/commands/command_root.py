"""
Base command of SeedOS, holds all available commands.
"""
from game.seedOS.command import create_command
from game.seedOS.commands.help import get_help_command
from game.seedOS.commands.shutdown import get_shutdown_command


def create_command_root():
    return create_command(
        name="command_root",
        run=None,
        privilege_required=0,
        subcommands={
            "help": get_help_command(),
            "shutdown": get_shutdown_command(),
        }
    )
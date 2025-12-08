"""
Base command of SeedOS, holds all available commands.
"""
from game.seedOS.command import create_command
from game.seedOS.commands.cd import get_cd_command
from game.seedOS.commands.clear import get_clear_command
from game.seedOS.commands.do import get_do_command
from game.seedOS.commands.help import get_help_command
from game.seedOS.commands.look import get_look_command
from game.seedOS.commands.ls import get_ls_command
from game.seedOS.commands.shutdown import get_shutdown_command


def create_command_root():
    return create_command(
        name="command_root",
        run=None,
        privilege_required=0,
        subcommands={
            "help": get_help_command(),
            "shutdown": get_shutdown_command(),
            "clear": get_clear_command(),
            "ls": get_ls_command(),
            "cd": get_cd_command(),
            "look": get_look_command(),
            "do": get_do_command()
        }
    )
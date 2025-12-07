"""
Primary game loop for file navigation.
"""
from time import sleep

from game.ansi_actions.style import style
from game.sound.effects import get_effects
from game.terminal.input import poll_key_press
from game.terminal.screen import clear_screen
from game.seedOS.command import send_command
from game.seedOS.console import display_message_history, start_prompt_user, send_message, send_messages, \
    do_validated_prompt


def get_seedos_console_scene():
    """
    Return the data dictionary for the seedOS console scene.

    Scene data dictionaries have the form:
    {
        "name": <string>,
        "open": <function or None>,
        "update": <function or None>,
        "exit": <function or None>
    }

    :postcondition: get data for the seedOS console scene
    :return: a dictionary representing the data for the seedOS console scene
    """

    def open_seedos_console(game_data):
        """
        Reset the menu.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: open the seedOS console
        """
        clear_screen()
        handle_progress(game_data)
        game_data["seed_system"]["active_program"] = None
        game_data["seed_system"]["active_file"] = None
        display_message_history(game_data["seed_system"])

    def update_seedos_console(game_data):
        """
        Return the next scene to run after the seedOS console.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: run the seedOS console scene
        :postcondition: return the next scene to run, or None for game exit
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        while True:
            inputted_prompt = do_validated_prompt(game_data, None)
            if inputted_prompt is None:
                continue
            result = send_command(game_data["seed_system"], inputted_prompt)
            if result["code"] == "success" and game_data["seed_system"]["active_program"]:
                send_message(
                    game_data["seed_system"],
                    f"Running... {game_data["seed_system"]["active_program"]}")
                return game_data["seed_system"]["active_program"]
            display_message_history(game_data["seed_system"])

    return {
        "name": "seedos_console",
        "open": open_seedos_console,
        "update": update_seedos_console,
        "exit": None}


def handle_progress(game_data):
    progress = game_data["progress"]
    if progress["just_loaded"]:
        progress["just_loaded"] = False
        game_data["seed_system"]["message_history"].clear()
        send_message(
            game_data["seed_system"],
            f"Welcome, {style(game_data['seed_system']['aphid']['name'], 'green')}")
    if progress["new_user"]:
        send_messages(game_data["seed_system"], (
            f"Hello {style('beta tester!', 'bold', 'yellow')}",
            "Welcome to SeedOS.",
            "To get setup with your new operating system,",
            f"enter '{style('help', 'bold', 'magenta')}' for information about commands.",
            f"When you're ready, take a '{style('look', 'bold', 'yellow')}' inside README.txt",
            "for important information."))

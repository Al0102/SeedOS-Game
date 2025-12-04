"""
Save and shutdown seedOS, then return to main main menu.
"""
from time import sleep

from game.save import save_data_to_file
from game.sound.effects import get_effects
from game.terminal.input import poll_key_press
from game.terminal.screen import clear_screen
from game.seedOS.console import display_message_history, start_prompt_user, draw_user_prompt


def get_seedos_shutdown_scene():
    """
    Return the data dictionary for the seedOS shutdown scene.

    Scene data dictionaries have the form:
    {
        "name": <string>,
        "open": <function or None>,
        "update": <function or None>,
        "exit": <function or None>
    }

    :postcondition: get data for the seedOS shutdown scene
    :return: a dictionary representing the data for the seedOS shutdown scene
    """
    prompt_user = start_prompt_user()

    def open_seedos_shutdown(_):
        """
        Reset the menu.

        :postcondition: open the seedOS shutdown
        """
        nonlocal prompt_user
        clear_screen()
        draw_user_prompt()
        prompt_user = start_prompt_user()
        get_effects()["mouse_click"].play(loop=True)
        get_effects()["mouse_click"].pause()

    def exit_seedos_shutdown(game_data):
        """
        Cleans the scene before it is switched.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: run the seedOS shutdown scene
        :postcondition: return the next scene to run, or None for game exit
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        game_data["seed_system"]["active_program"] = None

    def update_seedos_shutdown(game_data):
        """
        Return the next scene to run after the seedOS shutdown.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        nonlocal prompt_user
        while True:
            display_message_history(game_data["seed_system"])
            get_effects()["mouse_click"].pause()
            inputted = poll_key_press(game_data["key_input"])
            get_effects()["mouse_click"].resume()
            sleep(0.01)
            inputted_prompt = prompt_user(inputted)
            if inputted_prompt is None:
                continue
            inputted_prompt = inputted_prompt.strip().lower()
            if inputted_prompt == "yes":
                save_data_to_file(game_data)
                return "main_menu"
            if inputted_prompt == "no":
                return "seedos_console"
            prompt_user = start_prompt_user()

    return {
        "name": "seedos_shutdown",
        "open": open_seedos_shutdown,
        "update": update_seedos_shutdown,
        "exit": exit_seedos_shutdown}


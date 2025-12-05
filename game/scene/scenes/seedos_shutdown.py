"""
Save and shutdown seedOS, then return to main main menu.
"""
from time import sleep

from game.ansi_actions.style import style
from game.save import save_data_to_file
from game.sound.effects import get_effects
from game.terminal.input import poll_key_press, pull_input
from game.seedOS.console import display_message_history, start_prompt_user, draw_user_prompt, send_message, \
    send_messages


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
    shutdown_sequence = iter([])

    def open_seedos_shutdown(game_data):
        """
        Reset the menu.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: open the seedOS shutdown scene
        """
        nonlocal shutdown_sequence
        draw_user_prompt()
        shutdown_sequence = start_shutdown_sequence(game_data)
        next(shutdown_sequence)
        display_message_history(game_data["seed_system"])
        get_effects()["mouse_click"].play(loop=True)
        get_effects()["mouse_click"].pause()

    def exit_seedos_shutdown(game_data):
        """
        Cleans the scene before it is switched.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: exit the seedOS shutdown scene
        """
        get_effects()["mouse_click"].stop()

    def update_seedos_shutdown(game_data):
        """
        Return the next scene to run after the seedOS shutdown.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        while True:
            get_effects()["mouse_click"].pause()
            poll_key_press(game_data["key_input"])
            get_effects()["mouse_click"].resume()
            sleep(0.05)
            try:
                result = next(shutdown_sequence)
            except StopIteration:
                return "main_menu"
            else:
                if result:
                    return result
                display_message_history(game_data["seed_system"])

    return {
        "name": "seedos_shutdown",
        "open": open_seedos_shutdown,
        "update": update_seedos_shutdown,
        "exit": exit_seedos_shutdown}


def start_shutdown_sequence(game_data):
    """
    Return iterator for shutting down the seed system.

    :param game_data: a dictionary representing the data needed to run the game
    :precondition game_data: must be a well-formed dictionary of game data
    :postcondition: get an iterator for running the shutdown sequence
    :postcondition: yields a string representing the scene to switch to or None to continue
    :return: an iterator representing the shutdown sequence
    """
    send_messages(game_data["seed_system"], (
        "Getting ready to shutdown system...",
        style("Save game to file? (yes/no)", "red")))
    prompt_user = start_prompt_user()
    while True:
        confirm_save = prompt_user(pull_input(game_data["key_input"], flush=True)[0])
        if confirm_save is None:
            yield
            continue
        confirm_save = confirm_save.strip().lower()
        if confirm_save == "yes":
            send_message(game_data["seed_system"], save_data_to_file(game_data))
            break
        if confirm_save == "no":
            send_message(game_data["seed_system"], "did not save data.")
            break
        prompt_user = start_prompt_user()
        yield
    send_messages(game_data["seed_system"], (
        "Choice confirmed.",
        style("Are you sure you want to shut down SeedOS? (yes/no)", "red")))
    prompt_user = start_prompt_user()
    yield
    while True:
        confirm_shutdown = prompt_user(pull_input(game_data["key_input"], flush=True)[0])
        if confirm_shutdown is None:
            yield
            continue
        confirm_shutdown = confirm_shutdown.strip().lower()
        if confirm_shutdown == "yes":
            break
        if confirm_shutdown == "no":
            send_messages(game_data["seed_system"],(
                "Canceling shutdown...",
                "Done!"))
            yield "seedos_console"
        prompt_user = start_prompt_user()
        yield


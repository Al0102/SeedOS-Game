"""
Create new seed system and APHID scene.
"""
from time import sleep

from game.ansi_actions.style import style
from game.menu import create_menu
from game.seedOS import init_seed_system, init_aphid
from game.seedOS.console import display_message_history, draw_user_prompt, send_message, start_prompt_user, \
    send_messages, get_console_dimensions
from game.sound.effects import chance_sound, get_effects
from game.terminal.input import poll_key_press, pull_input
from game.terminal.screen import clear_screen


def get_seedos_signup_scene():
    """
    Return the data dictionary for the seedOS signup scene.

    Scene data dictionaries have the form:
    {
        "name": <string>,
        "open": <function or None>,
        "update": <function or None>,
        "exit": <function or None>
    }

    :postcondition: get data for the seedOS signup scene
    :return: a dictionary representing the data for the seedOS signup scene
    """
    signup_sequence = iter([])

    def open_seedos_signup(game_data):
        """
        Start the signup sequence.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: start the signup sequence
        """
        nonlocal signup_sequence
        game_data["seed_system"] = init_seed_system()
        game_data["progress"] = []
        signup_sequence = start_signup_sequence(game_data)
        clear_screen()
        draw_user_prompt()
        display_message_history(game_data["seed_system"])
        get_effects()["mouse_click"].play(loop=True)
        get_effects()["mouse_click"].pause()
        next(signup_sequence)

    def update_seedos_signup(game_data):
        """
        Return the next scene to run after the seedOS signup.

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
                result = next(signup_sequence)
            except StopIteration:
                game_data["seed_system"]["message_history"].clear()
                return "seedos_console"
            else:
                if result:
                    send_message(game_data["seed_system"], result)
                    display_message_history(game_data["seed_system"])

    return {
        "name": "seedos_signup",
        "open": open_seedos_signup,
        "update": update_seedos_signup,
        "exit": None}


def start_signup_sequence(game_data):
    send_messages(game_data["seed_system"], (
        "Installing seedOS...",
        "Hatching APHID...",
        style("Done!", "green"),
        "Enter your name:"))
    prompt_user = start_prompt_user()
    while True:
        name = prompt_user(pull_input(game_data["key_input"], flush=True)[0])
        if name is None:
            yield
            continue
        name = name.strip()
        if len(name) == 0 or "\033" in name:
            yield f"Name is invalid: {name}"
        else:
            game_data["seed_system"]["aphid"] = init_aphid(name)
            break
    options = ("Yes", "No need, I'm beating this in one go!")
    confirm_menu = create_menu(
        4, get_console_dimensions()["output"][1] - 1,
        *options)
    send_messages(game_data["seed_system"], (
        style(f"Successfully registered APHID: {name}", "green"),
        "Save game data to file?"))
    send_messages(game_data["seed_system"], ["" for _ in range(4)], 0)
    confirm_menu["draw_menu"]()
    yield
    while True:
        confirm_menu["draw_menu"]()
        result = confirm_menu["update_menu"](pull_input(game_data["key_input"], flush=True)[0])
        if result is None:
            yield
            continue
        if result == "Yes":
            yield save_data_to_file(game_data)
        break
    send_messages(game_data["seed_system"], (
        "Initializing seedOS ecosystem, this may take a while...",
        "Polishing tools... ",
        "Plucking weeds...",
        "Digging holes...",
        "Planting the seed drive...",
        "Feeding the APHID...",
        "Refilling nectar...",
        "Spinning webs...",
        "Letting in sun...",
        "Watching grass grow...",
        "Building ShellSpace...",
        "Done!"
    ), 1)
    yield style("Press any key to continue", "bold", "rapid_blink", "black", "background_yellow")


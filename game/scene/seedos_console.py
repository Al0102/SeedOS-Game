"""
Primary game loop for file navigation.
"""
from game.sound.effects import get_effects, chance_sound
from game.terminal.input import pull_input, start_text_input, poll_key_press
from game.terminal.screen import clear_screen
from game.seedOS.command import send_command, run_command
from game.seedOS.console import get_console_dimensions, display_message_history, start_prompt_user, draw_user_prompt


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
    prompt_user = start_prompt_user()

    def open_seedos_console(_):
        """
        Reset the menu.

        :postcondition: open the seedOS console
        """
        nonlocal prompt_user
        clear_screen()
        draw_user_prompt()
        prompt_user = start_prompt_user()

    def update_seedos_console(game_data):
        """
        Return the next scene to run after the seedOS console.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        nonlocal prompt_user
        while True:
            inputted = poll_key_press(game_data["key_input"])
            inputted_prompt = prompt_user(inputted)
            chance_sound("mouse_click", 0.5)
            if inputted_prompt is None:
                continue
            result = send_command(game_data["seed"], inputted_prompt)
            if result[0] == "success":
                return
            prompt_user = start_prompt_user()

    return {
        "name": "seedos_console",
        "open": open_seedos_console,
        "update": update_seedos_console,
        "exit": None}


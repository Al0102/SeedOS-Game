"""
Primary game loop for file navigation.
"""
from game.terminal.input import pull_input, start_text_input
from game.terminal.screen import clear_screen
from game.seedOS.command import send_command
from game.seedOS.console import get_console_dimensions, display_message_history, start_prompt_user, draw_user_prompt


def get_seedOS_console_scene():
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

    def open_seedOS_console(_):
        """
        Reset the menu.

        :postcondition: open the seedOS console
        """
        clear_screen()
        draw_user_prompt()

    def update_seedOS_console(game_data):
        """
        Return the next scene to run after the seedOS console.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        while True:
            poll_key_press(game_data["key_input"])
            inputted = pull_input(game_data["key_input"], flush=True)[0]
            selection = menu["update_menu"](inputted)
            if selection == "Start":
                return "seedOS_console" # TODO change to seedOS_login
            if selection == "Quit":
                return "quit"

    return {
        "name": "seedOS_console",
        "open": open_seedOS_console,
        "update": update_seedOS_console,
        "exit": None}


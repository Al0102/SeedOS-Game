"""
Main menu: Start or Quit.
"""
from game.menu import create_menu, centered_menu_position
from game.sound.effects import chance_sound
from game.terminal.input import pull_input, poll_key_press
from game.terminal.screen import get_screen_size, clear_screen


def get_main_menu_scene():
    """
    Return the data dictionary for the main menu scene.

    Scene data dictionaries have the form:
    {
        "name": <string>,
        "open": <function or None>,
        "update": <function or None>,
        "exit": <function or None>
    }

    :postcondition: get data for the main menu scene
    :return: a dictionary representing the data for the main menu scene
    """
    options = ("Start", "Quit")
    menu_column, menu_row = centered_menu_position(options)
    menu = {}

    def open_main_menu(_):
        """
        Reset the menu.

        :postcondition: reset the main menu by creating a new menu
        """
        nonlocal menu
        menu = create_menu(
            menu_column, menu_row,
            *options)
        clear_screen()
        menu["draw_menu"]()

    def update_main_menu(game_data):
        """
        Return the next scene to run after the main menu.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: run the game main menu scene
        :postcondition: return the next scene to run, or None for game exit
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        while True:
            poll_key_press(game_data["key_input"])
            inputted = pull_input(game_data["key_input"], flush=True)[0]
            selection = menu["update_menu"](inputted)
            if selection == "Start":
                return "seedos_login"
            if selection == "Quit":
                return "quit"

    return {
        "name": "main_menu",
        "open": open_main_menu,
        "update": update_main_menu,
        "exit": None}


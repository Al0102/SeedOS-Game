"""
Main menu: Start or Quit.
"""
from game.menu import create_menu
from game.terminal.input import pull_input
from game.terminal.screen import get_screen_size, clear_screen
from game.utilities import longest_string


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
    menu_position = get_screen_size()
    menu_width = (menu_position[0] - longest_string(options)[1]) // 2
    menu_height = (menu_position[1] - len(options)) // 2
    menu = {}

    def open_main_menu(_):
        """
        Reset the menu.

        :postcondition: reset the main menu by creating a new menu
        """
        nonlocal menu
        menu = create_menu(
            menu_width, menu_height,
            *options)
        clear_screen()
        menu["draw_menu"]()

    def update_main_menu(game_data):
        """
        Return the next scene to run after the main menu.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        while True:
            game_data["key_input"]["key_get"](game_data["key_input"])
            inputted = pull_input(game_data["key_input"], flush=True)[0]
            selection = menu["update_menu"](inputted)
            if selection == "Start":
                return "seedOS_console" # TODO change to seedOS_login
            if selection == "Quit":
                return "quit"

    return {
        "name": "main_menu",
        "open": open_main_menu,
        "update": update_main_menu,
        "exit": None}


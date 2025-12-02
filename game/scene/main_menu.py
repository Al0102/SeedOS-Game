"""
Main menu: Start or Quit.
"""
from game.menu import create_menu
from game.terminal.input import pull_input
from game.terminal.screen import get_screen_size
from game.utilities import longest_string


def get_main_menu_scene():
    options = ("Start", "Quit")
    menu_position = get_screen_size()
    menu_position[0] = (menu_position[0] - longest_string(options)[1]) // 2
    menu_position[1] = (menu_position[1] - len(options)) // 2
    menu = {}

    def open_main_menu(_):
        """
        Reset the menu.

        :postcondition: reset the main menu by creating a new menu
        """
        nonlocal menu
        menu = create_menu(
            menu_position[0], menu_position[1],
            *options)
        menu["draw_menu"]()

    def update_main_menu(game_data):
        """
        Return the next scene to run after the main menu.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :return: a dictionary representing the data for the next scene to run,
                 or None to signify game exit
        """
        while True:
            game_data["key_input"]["key_get"]()
            inputted = pull_input(game_data["key_input"], flush=True)
            menu["update_menu"](inputted)

    return {
        "name": "main_menu",
        "open": open_main_menu,
        "update": update_main_menu,
        "exit": None}


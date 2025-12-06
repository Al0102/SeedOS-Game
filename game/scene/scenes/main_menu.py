"""
Main menu: Start or Quit.
"""
from game.seedOS.console import do_menu_prompt
from game.terminal.screen import clear_screen


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
        clear_screen()
        selection = do_menu_prompt(game_data, *options, style_name="centered")
        if selection == "Start":
            return "seedos_login"
        else:
            return "quit"

    return {
        "name": "main_menu",
        "open": None,
        "update": update_main_menu,
        "exit": None}

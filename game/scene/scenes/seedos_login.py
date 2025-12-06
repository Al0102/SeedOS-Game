"""
Load save data from file based on username.
"""
from game.ansi_actions.cursor import cursor_set
from game.ansi_actions.style import style
from game.save import load_saves_file_paths, load_save_from_file
from game.menu import get_centered_menu_position
from game.seedOS.console import do_menu_prompt
from game.terminal.screen import clear_screen


def get_seedos_login_scene():
    """
    Return the data dictionary for the seedOS login scene.

    Scene data dictionaries have the form:
    {
        "name": <string>,
        "open": <function or None>,
        "update": <function or None>,
        "exit": <function or None>
    }

    :postcondition: get data for the seedOS login scene
    :return: a dictionary representing the data for the seedOS login scene
    """
    save_files = []
    corrupted_files_names = set()
    options = []

    def open_seedos_login(game_data):
        """
        Reset the menu.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: reset the main menu by creating a new menu
        """
        nonlocal save_files, options
        save_files = load_saves_file_paths(game_data)
        options = list(set(map(lambda file: file.stem, save_files)) - corrupted_files_names)
        if len(options) <= 5:
            options.insert(0, style("NEW", "bold", "yellow"))
        options.insert(0, style("Back to main menu", "bold", "red"))
        menu_column, menu_row = get_centered_menu_position(*options)
        clear_screen()
        cursor_set(menu_column, menu_row - 1)
        print("Choose a save:", end="", flush=False)

    def exit_seedos_login(game_data):
        """
        Cleans the scene before it is switched.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: exit the seedOS login scene
        """
        if game_data["seed_system"]:
            game_data["progress"]["just_loaded"] = True
        clear_screen()

    def update_seedos_login(game_data):
        """
        Return the next scene to run after the seedOS login.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: run the seedOS login scene
        :postcondition: return the next scene to run, or None for game exit
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        nonlocal corrupted_files_names

        selection = do_menu_prompt(game_data, *options, style_name="centered")
        if selection == style("Back to main menu", "bold", "red"):
            return "main_menu"
        elif selection == style("NEW", "bold", "yellow"):
            return "seedos_signup"
        else:
            data = load_save_from_file(
                list(filter(lambda file: file.stem == selection, save_files))[0])
            if data:
                game_data.update(data)
                return "seedos_console"
            else:
                corrupted_files_names.add(selection)
                # Reload scene without corrupted options
                return "seedos_login"

    return {
        "name": "seedos_login",
        "open": open_seedos_login,
        "update": update_seedos_login,
        "exit": exit_seedos_login}


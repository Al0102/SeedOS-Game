"""
Load save data from file based on username.
"""
from game.ansi_actions.cursor import cursor_set
from game.ansi_actions.style import style
from game.save import load_saves_file_paths, load_save_from_file
from game.menu import create_menu, centered_menu_position
from game.terminal.input import poll_key_press
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
    menu = {}
    menu_column, menu_row = 1, 1

    def open_seedos_login(game_data):
        """
        Reset the menu.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: reset the main menu by creating a new menu
        """
        nonlocal save_files, menu, menu_column, menu_row
        save_files = load_saves_file_paths(game_data)
        options = list(set(map(lambda file: file.stem, save_files)) - corrupted_files_names)
        if len(options) <= 5:
            options.insert(0, style("NEW", "bold"))
        options.insert(0, style("Back to main menu", "bold"))
        menu_column, menu_row = centered_menu_position(options)
        menu = create_menu(
            menu_column, menu_row,
            *options)
        clear_screen()
        cursor_set(menu_column, menu_row - 1)
        print("Choose a save:", end="", flush=False)
        menu["draw_menu"]()

    def update_seedos_login(game_data):
        """
        Return the next scene to run after the seedOS login.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        nonlocal corrupted_files_names
        while True:
            inputted = poll_key_press(game_data["key_input"])
            selection = menu["update_menu"](inputted)
            if selection is None:
                continue
            if selection == style("Back to main menu", "bold"):
                return "main_menu"
            if selection == style("NEW", "bold"):
                return "seedos_signup"
            data = load_save_from_file(
                list(filter(lambda file: file.stem == selection, save_files))[0])
            if data:
                game_data.update(data)
                return "seedos_console"
            else:
                corrupted_files_names.add(selection)
                open_seedos_login(game_data)

    return {
        "name": "seedos_login",
        "open": open_seedos_login,
        "update": update_seedos_login,
        "exit": None}


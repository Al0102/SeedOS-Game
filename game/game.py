"""
The entry point for the game.
"""
import pathlib, json

from game import relative_path
from game.ansi_actions.cursor import cursor_set
from game.ansi_actions.style import style
from game.scene.scene import get_scenes
from game.terminal import input as terminal_input
from game.terminal.screen import get_screen_size


def setup_game():
    """
    Get the data for running an instance of the game.

    The data is in a dictionary of form:
    {
        "key_input": <terminal input data dictionary>,
        "saves": <save data dictionary>,
        "previous_scene": None or <scene data dictionary>,
        "active_scene": <scene data dictionary>
    }

    :postcondition: get the data needed for the game to run
    :postcondition: create a local user data folder if it does not already exist
    :return: a dictionary representing the data needed for the game to run
    """
    game_data = {
        "key_input": terminal_input.init_key_input(),
        "saves_path": get_user_data_folder(),
        "previous_scene": None,
        "active_scene": get_scenes()["startup"],
        "seed_system": None}
    return game_data


def game_loop(game_data):
    """
    Drive the main game loop.

    :param game_data: a dictionary representing the data needed to run the game
    :precondition game_data: must be a well-formed dictionary of game data
    :postcondition: run the game
    """
    while True:
        if not game_data["active_scene"]["open"] is None:
            game_data["active_scene"]["open"](game_data)
        next_scene = game_data["active_scene"]["update"](game_data)
        if not game_data["active_scene"]["exit"] is None:
            game_data["active_scene"]["exit"](game_data)
        if next_scene is None:
            return
        game_data["previous_scene"] = game_data["active_scene"]
        try:
            game_data["active_scene"] = get_scenes()[next_scene]
        except KeyError:
            print(style(f"Scene is not defined: {next_scene}", "red"))
            return


def get_user_data_folder():
    """
    Get the path to the local data folder.

    Attempt to create one if no folder exists.

    :postcondition: get the path to the local data folder
    :postcondition: attempt to create a local data folder if it does not already exist
    :return: a path-like string representing the path to the local data folder,
             or None if no folder exists/can be created
    """
    save_folder = pathlib.Path(relative_path("local_data"))
    status = "Nothing loaded."
    try:
        save_folder.mkdir()
    except FileExistsError:
        status = "Local data folder found, loading saves."
    except PermissionError:
        status = "Unable to create local data folder, using temporary save data."
        save_folder = None
    else:
        status = f"Local data folder created at: {save_folder}"
    finally:
        cursor_set(get_screen_size()[0] - len(status), get_screen_size()[1])
        print(status, end="")
        return save_folder


def load_saves_file_paths(game_data):
    files = []
    status = "success"
    try:
        files = game_data["saves_path"].glob("**/*")
    except ValueError:
        status = "local data folder does not exist"
    else:
        files = [save_file for save_file in files if save_file.is_file() and save_file.suffix == ".json"]
    finally:
        cursor_set(get_screen_size()[0] - len(status), get_screen_size()[1])
        print(status, end="")
        return files


def load_save_from_file(file_path):
    status = "success"
    save_data = None
    try:
        with open(file_path, "r") as save_file:
            save_data = json.load(save_file)
    except FileNotFoundError:
        status = f"file does not exist: {file_path}"
    except json.JSONDecodeError:
        status = f"file data corrupted: {file_path}"
    finally:
        cursor_set(get_screen_size()[0] - len(status), get_screen_size()[1])
        print(status, end="")
        return save_data


def main():
    """
    Drive the program.
    """
    game_data = setup_game()
    game_loop(game_data)


if __name__ == "__main__":
    main()


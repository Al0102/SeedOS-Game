"""
The entry point for the game.
"""
import pathlib

from game import relative_path
from game.scene import scenes
from game.terminal import input as terminal_input


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
        "active_scene": scenes.bootup.get_scene()}
    return game_data


def game_loop(game_data):
    """
    Drive the main game loop.

    :param game_data: a dictionary representing the data needed to run the game
    :precondition game_data: must be a well-formed dictionary of game data
    :postcondition: run the game
    """
    game_data["active_scene"]["open"](game_data)
    while True:
        next_scene = game_data["active_scene"]["update"](game_data)
        if not game_data["active_scene"]["exit"] is None:
            game_data["active_scene"]["exit"](game_data)
        if next_scene is None:
            return
        game_data["previous_scene"] = game_data["active_scene"]
        game_data["active_scene"] = next_scene
        if not game_data["active_scene"]["open"] is None:
            game_data["active_scene"]["open"](game_data)


def get_user_data_folder():
    save_folder = pathlib.Path(relative_path("local_data"))
    try:
        save_folder.mkdir()
    except FileExistsError:
        print("Local data folder found, loading saves.")
    except PermissionError:
        print("Unable to create local data folder, using temporary save data.")
        save_folder = None
    else:
        print(f"Local data folder created at: {save_folder}")
    finally:
        return save_folder


def load_game_save():
    pass





def main():
    """
    Drive the program.
    """
    pass


if __name__ == "__main__":
    main()


"""
Save files.
"""
import pathlib
import dill as pickle

from game import relative_path
from game.ansi_actions.cursor import cursor_set
from game.terminal.screen import get_screen_size


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
        files = [save_file for save_file in files if save_file.is_file() and save_file.suffix == ".pkl"]
    finally:
        cursor_set(get_screen_size()[0] - len(status), get_screen_size()[1])
        print(status, end="")
        return files


def load_save_from_file(file_path):
    status = "success"
    save_data = None
    try:
        with open(file_path, "rb") as save_file:
            save_data = pickle.load(save_file)
    except FileNotFoundError:
        status = f"file does not exist: {file_path}"
    except pickle.UnpicklingError:
        status = f"file data corrupted: {file_path}"
    finally:
        cursor_set(get_screen_size()[0] - len(status), get_screen_size()[1])
        print(status, end="")
        return save_data


def save_data_to_file(game_data):
    """
    Save the <game_data> to a pkl file.

    Only the game_data's "progress" and "seed_system" are saved

    :param game_data: a dictionary representing the data needed to run the game
    :precondition game_data: must be a well-formed dictionary of game data
    :postcondition: attempt to save "progress" and "seed_system" from <game_data> to a pkl file
    :return: a string representing the success status of the file save
    """
    file_path = game_data["saves_path"] / f"{game_data["seed_system"]["aphid"]["name"].replace(" ", "_")}.pkl"
    status = "success"
    data = {"seed_system": game_data["seed_system"], "progress": game_data["progress"]}
    try:
        with open(file_path, "wb") as save_file:
            pickle.dump(data, save_file)
    except FileNotFoundError:
        status = f"local_data folder does not exist, cannot write"
    except PermissionError:
        status = f"not allowed to write to: {file_path}"
    finally:
        cursor_set(get_screen_size()[0] - len(status), get_screen_size()[1])
        print(status, end="")
        return status


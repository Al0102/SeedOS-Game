"""
Save files.
"""
import pathlib
import dill as pickle
from sys import stderr

from game import relative_path
from game.ansi_actions.cursor import cursor_set
from game.terminal.screen import get_screen_size


def get_user_data_folder(print_status=False):
    """
    Get the path to the local data folder.

    Attempt to create one if no folder exists.

    :param print_status: (default False) a boolean representing whether to print the operation status
    :precondition: print_status must be a boolean
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
        if print_status:
            cursor_set(get_screen_size()[0] - len(status), get_screen_size()[1])
            print(status, end="")
        return save_folder


def load_saves_file_paths(game_data, print_status=False):
    """
    Get the paths of save files in the local data folder.

    :param game_data: a dictionary representing the data needed to run the game
    :param print_status: (default False) a boolean representing whether to print the operation status
    :precondition game_data: must be a well-formed dictionary of game data
    :precondition: print_status must be a boolean
    :postcondition: get a list of save files within the local data folder
    :return: a list of Paths representing the paths of found save files in the local data folder
    """
    files = []
    status = "success"
    try:
        files = game_data["saves_path"].glob("**/*")
    except ValueError:
        status = "local data folder does not exist"
    else:
        files = [save_file for save_file in files if save_file.is_file() and save_file.suffix == ".pkl"]
    finally:
        if print_status:
            cursor_set(get_screen_size()[0] - len(status), get_screen_size()[1])
            print(status, end="")
        return files


def load_save_from_file(file_path, print_status=False):
    """
    Get the save data from the file at <file_path>.

    :param file_path: a path-like string or Path object representing the file load data from
    :param print_status: (default False) a boolean representing whether to print the operation status
    :precondition: file_path must be a path-like string or Path object
    :precondition: file_path must be for a .pkl file
    :precondition: print_status must be a boolean
    :postcondition: load the data from <file_path>
    :return: an object representing th data loaded from <file_path>,
             or None if no data could be loaded
    """
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
        if print_status:
            cursor_set(get_screen_size()[0] - len(status), get_screen_size()[1])
            print(status, end="", file=stderr)
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
        return status


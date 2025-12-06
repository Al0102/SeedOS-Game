"""
Manage the seedOS file system.
"""
from game import relative_path


def create_file_tree():
    return {
        "seed": {
            "name": "seed",
            "type": "folder",
        },
        "seed/Welcome.txt": {
            "name": "Welcome",
            "type": "file",
            "extension": "txt",
            "data": {
                "text": relative_path("assets/files/Welcome.txt")
            }
        },
        "seed/seedOS": {},
        "seed/documents": {},
        "seed/applications": {
            "name": "seed",
            "type": "folder",
        }
    }


def to_path(path_tokens):
    return "/".join(path_tokens)



def get_parent_directory_path(file_path):
    return to_path(tokenize_path(file_path)[:-1])


def get_current_folder_contents(seed_system, folder_path):
    """
    Get the contents (dictionaries) at the folder path in <seed_system>.

    :param seed_system: a dictionary representing the currently active seedOS system
    :param folder_path: a string representing path of the directory to get the contents of
    :precondition: seed_system must be a well-formed seed_system dictionary
    :precondition: folder_path must be a valid path-like string
    :raises FileNotFoundError: if folder_path does not exist
    :return: a tuple of strings representing the children file paths of <folder_path>
    """
    return tuple(filter(
        lambda file_path: get_parent_directory_path(file_path) == folder_path,
        seed_system["file_tree"].keys()))


def tokenize_path(file_path):
    """
    Return the path tokens of file_path.

    A path token is a single string without slashes representing something in the filetree.

    :param file_path: a path-like string representing a path
    :precondition: file_path must be a path-like string representing a path
    :postcondition: get the tokens in <file_path>
    :return: a list of strings representing the path tokens in <file_path>

    >>> tokenize_path("seed")
    ['seed']
    >>> tokenize_path("seed/")
    ['seed']
    >>> tokenize_path("seed/Applications/Tutorial Level")
    ['seed', 'Applications', 'Tutorial Level']
    """
    return file_path.strip("/ ").split("/")

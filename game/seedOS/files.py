"""
Manage the seedOS file system.
"""
from game import relative_path
from game.ansi_actions.style import style


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


def to_path(path_tokens: list | tuple) -> str:
    """
    Return <path_tokens> joined by "/".

    :param path_tokens: a list or tuple of strings representing the ordered path names to join
    :precondition: path_tokens must be a list or tuple of strings
    :postcondition: get the path string of <path_tokens>
    :postcondition: the path string uses "/" to join tokens
    :return: a string representing the path string of <path_tokens> joined by "/"

    >>> to_path([])
    ''
    >>> to_path(["", "a"])
    '/a'
    >>> to_path(["school", "Grade K", "abc123.txt"])
    'school/Grade K/abc123.txt'
    """
    return "/".join(path_tokens)


def get_parent_directory_path(file_path: str) -> str:
    """
    Get the parent directory path string of <file_path>.

    Return an empty string if no parent directory was found.

    :param file_path: a string representing the full path to a file/folder
    :precondition: file_path must be a path-like string with tokens separated by "/"
    :precondition: file_path cannot be an empty string, nor only "/", nor only spaces
    :postcondition: get the parent directory path string of <file_path>,
                    or an empty string if <file_path> has no parent directory
    :return: a string representing the parent directory path string of <file_path>,
                    or an empty string if <file_path> has no parent directory

    >>> get_parent_directory_path("root")
    ''
    >>> get_parent_directory_path("root/abc")
    'root'
    >>> get_parent_directory_path("root/abc/123/next/")
    'root/abc/123'
    """
    return to_path(tokenize_path(file_path)[:-1])


def get_folder_contents(seed_system: dict, folder_path, full_path=False) -> tuple:
    """
    Get the contents (dictionaries) at the folder path in <seed_system>.

    :param seed_system: a dictionary representing the currently active seedOS system
    :param folder_path: a string representing path of the directory to get the contents of
    :param full_path: a boolean representing whether to return paths as absolute or only the child name
    :precondition: seed_system must be a well-formed seed_system dictionary with key-value pair:
                       "file_tree": <dictionary>
    :precondition: folder_path must be a valid path-like string
    :raises FileNotFoundError: if folder_path does not exist
    :return: a tuple of strings representing the children file paths of <folder_path>
    """
    if not folder_path in seed_system["file_tree"]:
        raise FileNotFoundError(style(f"{folder_path} does not exist", "red"))
    children = filter(
        lambda file_path: get_parent_directory_path(file_path) == folder_path,
        seed_system["file_tree"].keys())
    if not full_path:
        children = map(lambda path: path.split("/")[-1], children)
    return tuple(children)


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

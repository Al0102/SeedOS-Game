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
            "privilege_required": 0},
        "seed/Welcome.txt": {
            "name": "Welcome",
            "type": "file",
            "privilege_required": 0,
            "extension": "txt",
            "data": {
                "text_src": relative_path("assets/files/Welcome.txt")}},
        "seed/seedOS": {
            "name": "seedOS",
            "privilege_required": 3,
            "type": "folder"},
        "seed/documents": {
            "name": "documents",
            "type": "folder",
            "privilege_required": 1},
        "seed/documents/logs": {
            "name": "logs",
            "type": "folder",
            "privilege_required": 1},
        "seed/documents/logs/patch.txt": {
            "name": "patch",
            "type": "file",
            "extension": "txt",
            "privilege_required": 1,
            "data": {
                "text_src": relative_path("assets/files/logs_patch.txt")}},
        "seed/documents/logs/potty_joke.txt": {
            "name": "potty_joke",
            "type": "file",
            "extension": "txt",
            "privilege_required": 1,
            "data": {
                "text_src": relative_path("assets/files/log_joke.txt")}},
        "seed/applications": {
            "name": "applications",
            "type": "folder",
            "privilege_required": 1}}

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

def get_parent_folder_path(file_path: str) -> str:
    """
    Get the parent folder path string of <file_path>.

    Return an empty string if no parent folder was found.

    :param file_path: a string representing the full path to a file/folder
    :precondition: file_path must be a path-like string with tokens separated by "/"
    :precondition: file_path cannot be an empty string, nor only "/", nor only spaces
    :postcondition: get the parent folder path string of <file_path>,
                    or an empty string if <file_path> has no parent folder
    :return: a string representing the parent folder path string of <file_path>,
                    or an empty string if <file_path> has no parent folder

    >>> get_parent_folder_path("root")
    ''
    >>> get_parent_folder_path("root/abc")
    'root'
    >>> get_parent_folder_path("root/abc/123/next/")
    'root/abc/123'
    """
    return to_path(tokenize_path(file_path)[:-1])

def get_folder_contents(seed_system: dict, folder_path, full_path=False) -> tuple:
    """
    Get the contents (dictionaries) at the folder path in <seed_system>.

    :param seed_system: a dictionary representing the currently active seedOS system
    :param folder_path: a string representing path of the folder to get the contents of
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
        lambda file_path: get_parent_folder_path(file_path) == folder_path,
        seed_system["file_tree"].keys())
    if not full_path:
        children = map(lambda path: path.split("/")[-1], children)
    return tuple(children)

def convert_relative_path_to_absolute(current_path: str, new_relative_path: str) -> str:
    """
    Get an absolute path from a relative (path with ".." or ".") path.

    "." - current folder
    ".." - parent folder

    :param current_path: a string representing the absolute path of the current working folder
    :param new_relative_path: a string representing the relative path from <current_path>
    :preconditon: current_path must be a path-string with tokens separated by "/"
    :preconditon: new_relative_path must be a string with tokens separated by "/"
    :postcondition: find the absolute path from <current_path> and <new_relative_path>
    :return: a path-like string representing the absolute path based on <current_path> and <new_relative_path>

    >>> convert_relative_path_to_absolute("seed", ".")
    'seed'
    >>> convert_relative_path_to_absolute("seed/school/", "../../../work/files/12_0_2025")
    'seed/work/files/12_0_2025'
    >>> convert_relative_path_to_absolute("seed/school/", "../../../../text.txt")
    'seed/text.txt'
    """
    relative_tokens = tokenize_path(new_relative_path)
    if not (".." in relative_tokens or "." in relative_tokens) or len(new_relative_path) == 0:
        return f"{current_path}/{new_relative_path}".strip("/ ")
    first_token = relative_tokens.pop(0)
    if first_token == "..":
        new_current_path = get_parent_folder_path(current_path)
        if new_current_path == "":
            new_current_path = current_path
    elif first_token == ".":
        new_current_path = current_path
    else:
        new_current_path = f"{current_path}/{first_token}",
    return convert_relative_path_to_absolute(new_current_path, to_path(relative_tokens))

def tokenize_path(file_path):
    """
    Return the path tokens of file_path.

    A path token is a single string without slashes representing something in the filetree.

    :param file_path: a path-like string representing a path
    :precondition: file_path must be a path-like string with tokens separated by "/"
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

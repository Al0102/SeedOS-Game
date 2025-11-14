"""
A file system roaming, virus busting game that runs in the terminal!

"""
from pathlib import Path
from os import path


def get_root_path():
    """
    Return the absolute path of this (game) module directory.

    :postcondition: get the absolute path of this (game) module's directory
    :return: a string representing the absolute path of this (game) module's directory

    >>> get_root_path() == str(Path(__file__).resolve().parent)
    True
    """
    return str(Path(__file__).resolve().parent)


def relative_path(project_relative_path):
    """
    Return the correctly formatted absolute path from a path relative to the project root (game).

    The relative path takes the form <subdir name>/<etc>,
        where <subdir name> is an immediate subdirectory of the project root.

    :param project_relative_path: a string representing the relative path from the project root
    :precondition: project_relative_path must be a string
    :precondition: project_relative_path must be a valid path string separated using forward slashes
    :postcondition: get the operating system formatted absolute path from <project_relative_path>
    :postcondition: if <project_relative_path> is an empty string, it does not append an extra slash to the path string
    :return: a string representing the operating system formatted absolute path from <project_relative_path>

    >>> rel_path = ""
    >>> relative_path(rel_path) == path.join(str(Path(__file__).resolve().parent))
    True
    >>> rel_path = "example"
    >>> relative_path(rel_path) == path.join(str(Path(__file__).resolve().parent), "example")
    True
    >>> rel_path = "example/example.txt"
    >>> relative_path(rel_path) == path.join(str(Path(__file__).resolve().parent), "example", "example.txt")
    True
    """
    if project_relative_path:
        path_items = project_relative_path.strip("/").split("/")
        return path.join(get_root_path(), *path_items)
    return get_root_path()


def main():
    print(get_root_path())
    print(relative_path(""))


if __name__ == "__main__":
    main()
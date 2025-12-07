"""
Miscellaneous tools.
"""
import re
from typing import Any


def get_escape_codes_indices(text: str) -> list:
    """
    Get all ANSI escape codes and their indices from the string.

    Return in form:
    [ (<index>, <code>) ]

    :param text: a string representing the text to remove escape codes from
    :precondition: text must be a string
    :postcondition: search for all ANSI escape codes from <text>
    :postcondition: return in form [ (<index>, <code>) ]
    :return: a list of tuples representing the escape codes and their indices found in <text>

    >>> get_escape_codes_indices("No codes")
    []
    >>> get_escape_codes_indices("\033[1mYes codes")
    [(0, '\\x1b[1m')]
    >>> get_escape_codes_indices("\033[1mMany\033[5;3H codes\033[0m")
    [(0, '\\x1b[1m'), (4, '\\x1b[5;3H'), (10, '\\x1b[0m')]
    """
    ansi_escape = re.compile(r'\033(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    codes = []
    while not (matched := ansi_escape.search(text)) is None:
        codes.append((matched.start(), matched.group(0)))
        text = text[:matched.start()] + text[matched.end():]
    return codes


def remove_escape_codes(text: str) -> str:
    """
    Remove all ANSI escape codes from the string.

    :param text: a string representing the text to remove escape codes from
    :precondition: text must be a string
    :postcondition: remove all ANSI escape codes from <text>
    :return: a string representing <text> with all ANSI escape codes removed

    >>> remove_escape_codes("No codes")
    'No codes'
    >>> remove_escape_codes("\033[1mYes codes")
    'Yes codes'
    >>> remove_escape_codes("\033[1mMany\033[5;3H codes\033[0m")
    'Many codes'
    """
    ansi_escape = re.compile(r'\033(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def longest_string(string_list: list | tuple) -> tuple[str, int] | None:
    """
    Find the longest string and its length in <iterable>.

    Return None if <string_list> is empty.

    :param string_list: a list representing the strings to search
    :precondition: string_list must be a list of strings
    :postcondition: find the longest string in <string_list> and its length
    :postcondition: return the first occurrence for ties
    :return: a tuple of a string representing the longest string in <string_list> and its length,
             or None if <string_list> is empty

    >>> longest_string([])

    >>> longest_string(("A", "B", "C"))
    ('A', 1)
    >>> longest_string(("AB", "ABC123", "C"))
    ('ABC123', 6)
    """
    if len(string_list) == 0:
        return None
    lengths = list(map(lambda item: len(item), string_list))
    longest_length = max(lengths)
    return (string_list[lengths.index(longest_length)], longest_length)


def sum_vectors(*vectors: tuple | list) -> tuple:
    """
    Return the sum of <vectors>.

    :param vectors: a tuple of lists/tuples of floats representing the vectors to add
    :precondition: vectors must be a tuple of lists/tuples of floats
    :precondition: vectors must have at least 2 vectors
    :precondition: all vectors in <vectors> must be of equal length
    :postcondition: calculate the scalar sum of <vectors>
    :return: a tuple of floats representing the scalar sum of <vectors>

    >>> sum_vectors((0, 0), (0, 0))
    (0, 0)
    >>> sum_vectors((0, 1), (5, -10), (4, 8))
    (9, -1)
    >>> sum_vectors((0, 1, 2), (3, 4, 5), (6, 7, 8))
    (9, 12, 15)
    """
    return tuple(map(sum, zip(*vectors)))


def targets_have_key(key_name: Any, *targets: dict) -> tuple:
    """
    Get a tuple of mapped booleans for whether the key exists in the target.

    :param key_name: a dictionary key representing the key to test for
    :param targets: a tuple of dictionaries representing the targets to search for <key_name>
    :precondition: key_name must be a valid dictionary key
    :precondition: targets must be a tuple of dictionaries
    :postcondition: get a tuple of mapped booleans for whether each dictionary in <targets> has the key <key_name>
    :postcondition: return an empty tuple if there are no results
    :return: a tuple of mapped of booleans representing whether each dictionary in <targets> has the key <key_name>,
             or an empty tuple if no targets are found

    >>> targets_have_key(0)
    ()
    >>> targets_have_key(0, {0: None}, {})
    (True, False)
    >>> targets_have_key("key", {0: None, 5: "key"}, {1: 0, "key": "value"}, {"key": None})
    (False, True, True)
    """
    return tuple(map(lambda target: key_name in target.keys(), targets))


def targets_with_key(key_name: Any, *targets: dict) -> tuple:
    """
    Get a tuple of dictionaries that have the key <key_name>.

    :param key_name: a dictionary key representing the key to test for
    :param targets: a tuple of dictionaries representing the targets to search for <key_name>
    :precondition: key_name must be a valid dictionary key
    :precondition: targets must be a tuple of dictionaries
    :postcondition: get a tuple of each dictionary in <targets> that has the key <key_name>
    :postcondition: return an empty tuple if there are no results
    :return: a tuple of dictionaries representing the targets that have key <key_name>m
             or an empty tuple if no results are found

    >>> targets_with_key(0) == ()
    True
    >>> targets_with_key(0, {0: None}, {}) == tuple([{0: None}])
    True
    >>> targets_with_key("key", {0: None, 5: "key"}, {1: 0, "key": "value"}, {"key": None}) == (
    ... {1: 0, "key": "value"}, {"key": None})
    True
    """
    return tuple(filter(lambda target: key_name in target.keys(), targets))


def get_direction_vectors() -> dict:
    """
    Return a dirctionary of directions names as vectors.

    A vector is of tuple of integers with the form (<x-value>, <y-value>).

    :postcondition: get a dictionary of directions and their corresponding vector tuples
    :return: a dictionary of two integers representing the corresponding vector of the move direction, <move>

    >>> get_direction_vectors() == {
    ...     "up": (0, -1),
    ...     "left": (-1, 0),
    ...     "right": (1, 0),
    ...     "down": (0, 1)}
    True
    """
    return {
        "up": (0, -1),
        "left": (-1, 0),
        "right": (1, 0),
        "down": (0, 1)}


def main():
    """
    Drive the program.
    """
    print(get_escape_codes_indices("\033[1mYes cod\033[0mes"))
    print(remove_escape_codes("\033[1mYes cod\033[0mes"))
    print(longest_string(("AB", "ABC123", "C")))


if __name__ == '__main__':
    main()

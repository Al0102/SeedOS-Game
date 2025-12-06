"""
Miscellaneous tools.
"""
import re


def get_escape_codes_indices(text):
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


def remove_escape_codes(text):
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


def longest_string(string_list):
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


def main():
    print(get_escape_codes_indices("\033[1mYes cod\033[0mes"))
    print(remove_escape_codes("\033[1mYes cod\033[0mes"))
    print(longest_string(("AB", "ABC123", "C")))


if __name__ == '__main__':
    main()

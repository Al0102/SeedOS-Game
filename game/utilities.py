"""
Miscellaneous tools.
"""


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
    return string_list[lengths.index(longest_length)], longest_length
"""
Helpers for cursor manipulation and movement.

TODO Consider implementing cursor pos save and auto pause on unfocus
"""


def get_move_options():
    """
    Return a dictionary of available movement options and their ANSI escape code letter.

    :postcondition: get a dictionary of available movement options and their ANSI escape code letter
    :postcondition: the key-value pairs have the form <name>: <sequence letter> and both are strings
    :return: a dictionary representing the available movement options and their ANSI escape code letter.

    >>> get_move_options() == {
    ...     "up": "A",
    ...     "down": "B",
    ...     "right": "C",
    ...     "left": "D",
    ...     "next_line": "E",
    ...     "previous_line": "F",
    ...     "column": "G",
    ...     "position": "H",
    ...     "scroll_up": "S",
    ...     "scroll_down": "T",
    ...     "save_position": "s",
    ...     "load_position": "u"}
    True
    """
    return {
        "up": "A",
        "down": "B",
        "right": "C",
        "left": "D",
        "next_line": "E",
        "previous_line": "F",
        "column": "G",
        "position": "H",
        "scroll_up": "S",
        "scroll_down": "T",
        "save_position": "s",
        "load_position": "u"
    }


def cursor_previous_line(amount=1):
    """
    Moves the cursor to the previous line in the terminal.

    This will cause the cursor to return to column 1.

    :param amount: an integer larger than or equal to 0 representing the number of lines to move up
    :precondition: amount must be an integer larger than or equal to 0
    :postcondition: move the cursor up <amount> lines
    :postcondition: the cursor will return to column 1
    :postcondition: a newline will not be printed

    >>> cursor_previous_line()
    \\x1b[1F
    >>> cursor_previous_line(0)
    \\x1b[0F
    >>> cursor_previous_line(5)
    \\x1b[5F
    """
    print(f"\033[{amount}{get_move_options()["previous_line"]}", end="", flush=True)


def cursor_next_line(amount=1):
    """
    Moves the cursor to the next line in the terminal.

    This will cause the cursor to return to column 1.

    :param amount: an integer larger than or equal to 0 representing the number of lines to move down
    :precondition: amount must be an integer larger than or equal to 0
    :postcondition: move the cursor down <amount> lines
    :postcondition: the cursor will return to column 1
    :postcondition: a newline will not be printed

    >>> cursor_next_line()
    \\x1b[1E
    >>> cursor_next_line(0)
    \\x1b[0E
    >>> cursor_next_line(5)
    \\x1b[5E
    """
    print(f"\033[{amount}{get_move_options()["next_line"]}", end="", flush=True)


def set_cursor_visibility(show):
    """
    Show or hide the terminal's cursor.

    :param show: a boolean representing whether to show or hide the cursor
    :precondition: show must be a boolean
    :postcondition: show or hide the terminal's cursor using an ANSI escape sequence
    :postcondition: a newline will not be printed

    >>> set_cursor_visibility(show=True)
    \\x1b[?25h
    >>> set_cursor_visibility(show=False)
    \\x1b[?25l
    """
    if show:
        print("\033[?25h", end="", flush=True)
    else:
        print("\033[?25l", end="", flush=True)


def cursor_set(column, row):
    """
    Set the cursor's position in the terminal.

    The position is 1-based; <column> units from the left and <row> units from the top.

    :param column: an integer representing the new column (horizontal) position of the cursor
    :param row: an integer representing the new row (vertical) position of the cursor
    :precondition: column must be a positive integer larger than 0
    :precondition: row must be a positive integer larger than 0
    :postcondition: set the cursor's position in the terminal:
                    <column> units from the left and <row> units from the top
    :postcondition: a newline will not be printed

    >>> cursor_set(1, 1)
    \\x1b[1;1H
    >>> cursor_set(8, 90)
    \\x1b[90;8H
    >>> cursor_set(15, 1)
    \\x1b[1;15H
    """
    print(f"\033[{row};{column}{get_move_options()["position"]}", end="", flush=True)


def cursor_shift(direction, amount=1):
    """
    Shift the cursor's position in the terminal by <amount> in <direction>.

    If no amount is specified, it shifts by one.

    :param direction: a string representing the direction to shift the cursor in
    :param amount: an integer representing the number of units to shift the cursor by
    :precondition: direction must be a string in ("up", "down", "left", "right")
    :precondition: amount must be a positive integer
    :postcondition: shift the cursor's position in the terminal by <amount> in <direction>
    :postcondition: a newline will not be printed

    >>> cursor_shift("down")
    \\x1b[1B
    >>> cursor_shift("right", 5)
    \\x1b[5C
    >>> cursor_shift("left", 20)
    \\x1b[20D
    """
    print(f"\033[{amount}{get_move_options()[direction]}", end="", flush=True)


def main():
    """
    Drive the program.
    """
    set_cursor_visibility(show=False)
    input("hidden cursor")
    set_cursor_visibility(show=True)
    input("visible cursor")
    cursor_set(17, 5)
    print("set pos", end="", flush=True)
    cursor_shift("down", 1)
    input("shift pos")
    cursor_next_line()
    input("next_line")
    cursor_set(1, 1)
    print("staircase")
    for _ in range(10):
        print("#", end="")
        cursor_shift("right")
        cursor_shift("down")
    input()
    cursor_shift("left", 10000)
    print("ladder")
    for _ in range(10):
        print("#", end="")
        cursor_shift("right")
        cursor_next_line()
    input()


if __name__ == '__main__':
    main()
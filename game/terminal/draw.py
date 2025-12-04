"""
Drawing and animating to the terminal.
"""
from game.ansi_actions import cursor
from game.terminal.screen import clear_screen
from game.utilities import remove_escape_codes, get_escape_codes_indices


def create_text_area(column, row, width, height, text=""):
    """
    Get a text area dictionary that can be used for draw_text_box.

    A text area dictionary has the form:
    {"column": <int>, "row": <int>, "width": <int>, "height": <int>, text: <str>}

    :param column: a positive integer greater than 0 representing the 1-based horizontal origin of the text area
    :param row: a positive integer greater than 0 representing the 1-based vertical origin of the text area
    :param width: a positive integer greater than 0 representing the columns of the text area
    :param height: a positive integer greater than 0 representing the rows of the text area
    :param text: (default empty string) a string representing the text to draw in the terminal
    :precondition: column must be a positive integer greater than 0 within the bounds of the terminal
    :precondition: row must be a positive integer greater than 0 within the bounds of the terminal
    :precondition: width must be a positive integer greater than 0,
                   and small enough to avoid causing the text area to exceed the bounds of the terminal
    :precondition: height must be a positive integer greater than 0,
                   and small enough to avoid causing the text area to exceed the bounds of the terminal
    :precondition: text must be a string with "\n" to indicate a new row
    :precondition: the number of newlines in <text> must be less than <height>
    :precondition: text_area must be a dictionary holding valid text area data
    :return: a dictionary representing a text box's data

    >>> create_text_area(1, 1, 1, 1, "") == {
    ...     "column": 1, "row": 1, "width": 1, "height": 1, "text": ""}
    True
    >>> create_text_area(4, 2, 10, 5, "Hello,\\nw\\no\\nr\\nld") == {
    ...     "column": 4, "row": 2, "width": 10, "height": 5, "text": "Hello,\\nw\\no\\nr\\nld"}
    True
    """
    return {"column": column, "row": row, "width": width, "height": height, "text": text}


def draw_text_box(
        column=None, row=None, width=None, height=None, text="",
        text_area=None, overwrite=False, flush_output=True):
    """
    Draw a text box to the terminal.

    A text area dictionary has the form:
    {"column": <int>, "row": <int>, "width": <int>, "height": <int>, text: <str>}

    :param column: (default None) a positive integer greater than 0,
                    representing the 1-based horizontal origin of the text area
    :param row: (default None) a positive integer greater than 0,
                representing the 1-based vertical origin of the text area
    :param width: (default None) a positive integer greater than 0 representing the columns of the text area
    :param height: (default None) a positive integer greater than 0 representing the rows of the text area
    :param text: (default None) a string representing the text to draw in the terminal
    :param text_area: (default None) a dictionary representing a text area's data
    :param overwrite: (default False) a boolean representing whether to replace all existing text within the text area
    :param flush_output: (default True) a boolean representing whether to flush the output to stdout
    :precondition: column must be a positive integer greater than 0 within the bounds of the terminal
    :precondition: row must be a positive integer greater than 0 within the bounds of the terminal
    :precondition: width must be a positive integer greater than 0,
                   and small enough to avoid causing the text area to exceed the bounds of the terminal
    :precondition: height must be a positive integer greater than 0,
                   and small enough to avoid causing the text area to exceed the bounds of the terminal
    :precondition: text must be a string with "\n" to indicate a new row
    :precondition: the number of newlines in <text> must be less than <height>
    :precondition: text_area must be a dictionary holding valid text area data
    :precondition: overwrite must be a boolean
    :precondition: flush_output must be a boolean
    :precondition: parameters, column, row, width, height, and text
                   or parameter, text_area must be given
    :postcondition: draw a text box to the terminal based on the <text_area> or the preceding parameters
    :postcondition: existing text within the bounds of the text area will be overwritten with a space
                    if <overwrite> is True

    >>> my_text_area = create_text_area(1, 1, 20, 1, "Hello, World")
    >>> draw_text_box(text_area=my_text_area)
    \\x1b[1;1HHello, World
    >>> # Do same but without predefined text area
    >>> draw_text_box(1, 1, 20, 1, "Hello, World")
    \\x1b[1;1HHello, World
    >>> draw_text_box(1, 2, 20, 2, "Hello, World", overwrite=True)
    \\x1b[2;1HHello, World        \\x1b[3;1
    """
    if not text_area:
        text_area = create_text_area(column, row, width, height, text)
    text_rows = text_area["text"].split("\n")
    clip_row_text = lambda row_text: remove_escape_codes(row_text)[:min(len(row_text), text_area["width"])]
    text_ansi = tuple(map(get_escape_codes_indices, text_rows))
    text_rows = tuple(map(clip_row_text, text_rows))
    for row_index in range(text_area["height"]):
        if row_index == len(text_rows) and not overwrite:
            break
        to_draw = ""
        cursor.cursor_set(text_area["column"], text_area["row"] + row_index)
        if row_index < len(text_rows):
            ansi_insert = text_rows[row_index]
            # print(text_ansi, end="")
            for ansi_code in reversed(text_ansi[row_index]):
                if ansi_code[0] <= len(text_rows[row_index]):
                    ansi_insert = ansi_insert[:ansi_code[0]] + ansi_code[1] + ansi_insert[ansi_code[0]:]
            to_draw = ansi_insert
        if overwrite:
            to_draw = to_draw.ljust(text_area["width"])
        print(to_draw, end="")
    print("", end="", flush=flush_output)
    return text_area


def draw_rectangle(
        column=None, row=None, width=None, height=None,
        text_area=None, flush_output=True):
    """
    :param column: a positive integer greater than 0,
                   representing the 1-based horizontal origin of the text area
    :param row: a positive integer greater than 0,
                representing the 1-based vertical origin of the text area
    :param width: a positive integer greater than 1 representing the columns of the text area
    :param height: a positive integer greater than 1 representing the rows of the text area
    :param text_area: (default None) a dictionary representing a text area's data
    :param flush_output: (default True) a boolean representing whether to flush the output to stdout
    :precondition: column must be a positive integer greater than 0 within the bounds of the terminal
    :precondition: row must be a positive integer greater than 0 within the bounds of the terminal
    :precondition: width must be a positive integer greater than 0,
                   and small enough to avoid causing the text area to exceed the bounds of the terminal
    :precondition: height must be a positive integer greater than 0,
                   and small enough to avoid causing the text area to exceed the bounds of the terminal
    :precondition: text_area must be a dictionary holding valid text area data
    :precondition: flush_output must be a boolean
    :precondition: parameters, column, row, width, height, and text
                   or parameter, text_area must be given
    :postcondition: draw a text box to the terminal based on the <text_area> or the preceding parameters

    >>> draw_rectangle(1, 1, 2, 2)
    \\x1b[1;1H..\\x1b[2;1H..
    >>> draw_rectangle(1, 1, 3, 3)
    \\x1b[1;1H._.\\x1b[2;1H| |\\x1b[3;1H` ´
    """
    if not text_area:
        text_area = create_text_area(column, row, width, height)
    justify_width = text_area["width"] - 1
    middle_height = text_area["height"] - 2
    text_area["text"] = (
            ".".ljust(justify_width, "-") + ".\n" +
            ("|".ljust(justify_width, " ") + "|\n") * middle_height +
            "`".ljust(justify_width, "-") + "´")
    draw_text_box(text_area=text_area, flush_output=flush_output)


def play_animation(frames, frames_per_second, loop=False):
    pass


def main():
    """
    Drive the program.
    """
    clear_screen()
    draw_text_box(5, 5, 20, 5,
                  "Hello, World\n123456789012345678901234")
    input()
    draw_text_box(5, 5, 20, 5,
                  "Bye, World",
                  overwrite=True)


if __name__ == '__main__':
    main()

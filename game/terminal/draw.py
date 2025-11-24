"""
Drawing and animating to the terminal.
"""
from game.ansi_actions import cursor
from game.terminal.screen import clear_screen


def create_text_area(column, row, width, height, text):
    """
    Get a text area dictionary that can be used for draw_text_box.

    A text area dictionary has the form:
    {"column": <int>, "row": <int>, "width": <int>, "height": <int>, text: <str>}

    :param column: a positive integer greater than 0 representing the 1-based horizontal origin of the text area
    :param row: a positive integer greater than 0 representing the 1-based vertical origin of the text area
    :param width: a positive integer greater than 0 representing the columns of the text area
    :param height: a positive integer greater than 0 representing the rows of the text area
    :param text: a string representing the text to draw in the terminal
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
    ... "column": 1, "row": 1, "width": 1, "height": 1, "text": ""}
    True
    """
    return {"column": column, "row": row, "width": width, "height": height, "text": text}


def draw_text_box(column=None, row=None, width=None, height=None, text="", text_area=None, overwrite=False):
    """
    Draw a text box to the terminal.

    A text area dictionary has the form:
    {"column": <int>, "row": <int>, "width": <int>, "height": <int>, text: <str>}

    :param column: a positive integer greater than 0 representing the 1-based horizontal origin of the text area
    :param row: a positive integer greater than 0 representing the 1-based vertical origin of the text area
    :param width: a positive integer greater than 0 representing the columns of the text area
    :param height: a positive integer greater than 0 representing the rows of the text area
    :param text: a string representing the text to draw in the terminal
    :param text_area: a dictionary representing a text area's data
    :param overwrite: a boolean representing whether to replace existing text within the text area with a space
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
    :precondition: parameters, column, row, width, height, and text
                   or parameter, text_area must be given
    :postcondition: draw a text box to the terminal based on the <text_area> or the preceding parameters
    :postcondition: existing text within the bounds of the text area will be overwritten with a space
                    if <overwrite> is True

    >>> draw_text_box(1, 1, 20, 1, "Hello, World")
    \x1b[1;1HHello, World
    >>> draw_text_box(1, 2, 20, 2, "Hello, World", overwrite=True)
    \x1b[2;1HHello, World        \x1b[3;1
    """
    if not text_area:
        text_area = create_text_area(column, row, width, height, text)
    text_rows = text_area["text"].split("\n")
    clip_row_text = lambda row_text: row_text[:min(len(row_text), text_area["width"])]
    text_rows = tuple(map(clip_row_text, text_rows))
    for row_index in range(text_area["height"]):
        if row_index == len(text_rows) and not overwrite:
            break
        to_draw = ""
        cursor.cursor_set(text_area["column"], text_area["row"] + row_index)
        if row_index < len(text_rows):
            to_draw += text_rows[row_index]
        if overwrite:
            to_draw = to_draw.ljust(text_area["width"])
        print(to_draw, end="")
    print("", end="", flush=True)
    return text_area


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
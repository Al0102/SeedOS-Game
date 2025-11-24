"""
OS dependent inputs with getch and msvcrt.
"""
import os
from string import printable
from game.ansi_actions import cursor
from game.terminal.screen import get_screen_size, draw_text_box, clear_screen


def get_key_codes(system=os.name):
    """
    Get dictionary of key code names and their corresponding key code for the operating system.

    Supported systems are "nt" for Windows and "posix" for Unix based systems.

    :param system: a string representing the name of operating system to get the key codes for
    :precondition: system must be a string
    :postcondition: get a dictionary of key code names and their OS dependent key codes,
                    or None if <system> is unsupported or invalid
    :postcondition: print error message if <system> is invalid or unsupported
    :return: a dictionary of key code names and their OS dependent key codes,
             or None if <system> is unsupported or invalid
    """
    if system == "posix":
        return {
            "enter": "\n",
            "backspace": "\x7f",
            # Require 1-2 extra getch() calls to confirm
            "escape": "\x1b",
            # Notice that these are the same as the ANSI escape sequences
            "up": "A",
            "left": "D",
            "right": "C",
            "down": "B"
        }
    elif system == "nt":
        return {
            "enter": "\r",
            "backspace": "\x08",
            "escape": "\x1b",
            # Require 1 extra getch() call after yielding \xe0
            "extend": "\xe0",
            # H: \x48, K: \x4B, M: \x4D, P: \x50
            "up": "H",
            "left": "K",
            "right": "M",
            "down": "P"
        }
    else:
        print("Unsupported operating system")
        return None


def init():
    if os.name == "posix":
        try:
            from getch import getch
        except ImportError:
            print("'getch' module not found: do 'pip install'")
            return None
        key_codes = get_key_codes("posix")

        def key_get(input_info):
            code = getch()
            if code == input_info["key_codes"]["escape"]:
                code = getch()
                if code != input_info["key_codes"]["escape"]:
                    code = getch()
            for key_name, key_code in input_info["key_codes"].items():
                if code == key_code:
                    input_info["input_queue"].append(key_name)
                    return key_name
            # Normal characters and undefined actions
            input_info["input_queue"].append(code)
            return code

    elif os.name == "nt":
        from msvcrt import getwch
        key_codes = get_key_codes("nt")

        def key_get(input_info):
            code = getwch()
            if code == input_info["key_codes"]["extend"]:
                code = getwch()
            for key_name, key_code in input_info["key_codes"].items():
                if code == key_code:
                    input_info["input_queue"].append(key_name)
                    return key_name
            # Normal characters and undefined actions
            input_info["input_queue"].append(code)
            return code
    else:
        print("Unsupported operating system: use Windows or Unix system")
        return None

    return {
        "key_codes": key_codes,
        "key_get": key_get,
        "input_queue": []
    }


def pull_input(terminal_input, amount=1, flush=False):
    """
    Pop the next <amount> inputs in the queue.

    :param terminal_input: a dictionary representing the terminal input info created by init()
    :param amount: an integer greater than or equal to -1 representing whether the number of inputs to queue
    :param flush: a boolean representing whether to clear the queue after getting the input
    :precondition: terminal_input must be a dictionary of terminal input info with the key "input_queue"
    :precondition: amount must be an integer greater than or equal to -1
    :precondition: flush must be a boolean
    :postcondition: get a list of input names from the queue and pop them
    :postcondition: if <amount> is -1, get all the queued inputs
    :postcondition: if <amount> is greater than the length of the input queue, return None
    :postcondition: clear the input queue if <flush> is True
    :return: a list of string(s) representing the popped input names,
             or None if <amount> is out of range of the input queue

    >>> input_dictionary = {"input_queue": []}
    >>> pull_input(input_dictionary)
    None
    >>> input_dictionary = {"input_queue": [" ", "a", "escape"]}
    >>> pull_input(input_dictionary, amount=2, flush=True)
    [' ', 'a']
    >>> input_dictionary
    []
    """
    queue_length = len(terminal_input["input_queue"])
    if queue_length < amount or amount == 0:
        return None
    if amount == -1:
        amount = queue_length
    inputs = [terminal_input["input_queue"].pop(0) for _ in range(amount)]
    if flush:
        terminal_input["input_queue"].clear()
    return inputs


def text_input(terminal_input, column, row, max_width=None, hide=False):
    """
    Return text from the user similarly to the built-in input.

    If not hidden, typing will start at (<column>, <row>), and
    start hiding (clip) characters after <max_width> characters are inputted.

    :param terminal_input: a dictionary representing the terminal input info created by init()
    :param column: an integer representing the 1-based horizontal origin of the text input
    :param row: an integer representing the 1-based vertical origin of the text_input
    :param max_width: an integer representing the maximum width of the input area
    :param hide: a boolean representing whether to show the user input being typed
    :precondition: terminal_input must be a dictionary of terminal input info created by init()
    :precondition: column must be a positive integer greater than 0 and less than the width of the terminal
    :precondition: row must be a positive integer greater than 0 and less than the height of the terminal
    :precondition: max_width must be a positive integer larger than 0,
                   or None for no constraints on typing length
    :precondition: hide must be a boolean
    :postcondition: get the text input from the user
    :postcondition: the text input is taken from function call until "enter" is detected
    :return: a string representing the text input from the user,
             or None if KeyboardInterrupt occurred
    """
    if not max_width:
        max_width = get_screen_size()[0] - column - 1
    pull_input(terminal_input, amount=0, flush=True)
    string_input = []
    cursor_at = 0
    draw_index = 0
    while True:
        try:
            inputted = terminal_input["key_get"](terminal_input)
        except KeyboardInterrupt:
            return None
        if inputted == "enter":
            cursor.cursor_set(column, row + 1)
            return string_input
        elif inputted == "backspace" and len(string_input) > 0 and cursor_at > 0:
            string_input.pop(cursor_at - 1)
            cursor_at -= 1
        elif inputted == "right":
            cursor_at = min(len(string_input), cursor_at + 1)
            # if cursor_at > len(string_input):
            #     draw_index += 1
        elif inputted == "left":
            cursor_at = max(0, cursor_at - 1)
            # if cursor_at < draw_index:
            #     draw_index -= 1
        elif inputted in printable:
            string_input.insert(cursor_at, inputted)
            cursor_at = min(len(string_input), cursor_at + 1)
            # if len(string_input) - draw_index > max_width:
            #     draw_index += 1
        else:
            continue
        if hide:
            continue
        draw_index = min(max(0, len(string_input) - max_width), max(0, cursor_at - max_width + draw_index))
        draw_text_box(
            20, 20, 50, 1,
            str(draw_index), overwrite=True)
        draw_text_box(
            column, row, max_width, 1,
            "".join(string_input[draw_index:draw_index + min(len(string_input), max_width)]),
            overwrite=True)
        cursor.cursor_set(
            min(max_width + column, max(column, column + cursor_at - draw_index)),
            row)


def main():
    """
    Drive the program.
    """
    clear_screen()
    print("Press escape to go to text input")
    key_input = init()
    while True:
        inputted = key_input["key_get"](key_input)
        if not inputted:
            continue
        elif inputted == "escape":
            break
        elif inputted in ("left", "right", "up", "down"):
            cursor.cursor_shift(inputted)
        else:
            print(inputted, end="", flush=True)
    print(text_input(key_input, 10, 10, 25))


if __name__ == '__main__':
    main()
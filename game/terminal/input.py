"""
OS dependent inputs with getch and msvcrt.
"""
import os
from string import printable
from game.ansi_actions import cursor
from game.sound import effects
from game.terminal.screen import get_screen_size, clear_screen
from game.terminal.draw import draw_text_box, create_text_area


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

    >>> get_key_codes("posix") == {
    ...     "enter": "\\n",
    ...     "backspace": "\\x7f",
    ...     "tab": "\\t",
    ...     "escape": "\\x1b",
    ...     "up": "A",
    ...     "left": "D",
    ...     "right": "C",
    ...     "down": "B"}
    True
    >>> get_key_codes("nt") == {
    ...     "enter": "\\r",
    ...     "backspace": "\\x08",
    ...     "tab": "\\t",
    ...     "escape": "\\x1b",
    ...     "extend": "\\xe0",
    ...     "up": "H",
    ...     "left": "K",
    ...     "right": "M",
    ...     "down": "P"}
    True
    """
    if system == "posix":
        return {
            "enter": "\n",
            "backspace": "\x7f",
            "tab": "\t",
            # Require 1-2 extra getch() calls to confirm
            "escape": "\x1b",
            # Notice that these are the same as the ANSI escape sequences
            "up": "escapeA",
            "left": "escapeD",
            "right": "escapeC",
            "down": "escapeB"
        }
    elif system == "nt":
        return {
            "enter": "\r",
            "backspace": "\x08",
            "escape": "\x1b",
            "tab": "\t",
            # Require 1 extra getch() call after yielding \xe0
            "extend": "\xe0",
            # H: \x48, K: \x4B, M: \x4D, P: \x50
            "up": "extendH",
            "left": "extendK",
            "right": "extendM",
            "down": "extendP"
        }
    else:
        print("Unsupported operating system")
        return None


def init_key_input():
    """
    Return a dictionary representing the info needed for "keyboard" input in the terminal

    The key input dictionary has the following key-value pairs:
        "key_codes": <os dependent dictionary of key codes and their names>\n
        "key_get": <os dependent function for adding the next key press to "input_queue">\n
        "input_queue": <list backlog of inputs>

    :return: a dictionary representing the info needed for "keyboard" input in the terminal
    """
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
                    code = "escape" + getch()
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
                code = "extend" + getwch()
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

    :param terminal_input: a dictionary representing the terminal input info created by init_key_input()
    :param amount: an integer greater than or equal to -1 representing the number of inputs to pull
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

    >>> input_dictionary = {"input_queue": [" ", "a", "escape"]}
    >>> pull_input(input_dictionary, amount=2, flush=True)
    [' ', 'a']
    >>> input_dictionary["input_queue"]
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


def start_text_input(column, row, max_width=None, hide=False):
    """
    Return a function for getting text input from the user.

    If not hidden, typing will start at (<column>, <row>), and
    start hiding (clip) characters after <max_width> characters are inputted.

    :param column: an integer representing the 1-based horizontal origin of the text input
    :param row: an integer representing the 1-based vertical origin of the text_input
    :param max_width: an integer representing the maximum width of the input area
    :param hide: a boolean representing whether to show the user input being typed
    :precondition: terminal_input must be a dictionary of valid terminal input info
    :precondition: column must be a positive integer greater than 0 and less than the width of the terminal
    :precondition: row must be a positive integer greater than 0 and less than the height of the terminal
    :precondition: max_width must be a positive integer larger than 0,
                   or None for no constraints on typing length
    :precondition: hide must be a boolean
    :postcondition: get a function for getting text input from the user
    :postcondition: the text input is taken from function call until "enter" is detected
    :return: a function representing a text_input prompt for the user
    """
    if not max_width:
        max_width = get_screen_size()[0] - column - 1
    text_area = create_text_area(column=column, row=row, width=max_width, height=1)
    string_input = []
    cursor_at = 0
    draw_index = 0

    def update_text_input(key_press):
        """
        Get text input from the user.

        :param key_press: a string representing the key code of the pressed key input
        :precondition: key_press must be a valid key code string
        :postcondition: get text input from the user, or continue the prompt
        :postcondition: the prompt is completed when "enter" is passed
        :return: a string representing the text input from the user,
        """
        nonlocal string_input, cursor_at, draw_index, text_area
        if key_press == "enter":
            cursor.cursor_set(column, row + 1)
            return string_input
        elif key_press == "backspace" and len(string_input) > 0 and cursor_at > 0:
            string_input.pop(cursor_at - 1)
            cursor_at -= 1
        elif key_press == "right":
            cursor_at = min(len(string_input), cursor_at + 1)
        elif key_press == "left":
            cursor_at = max(0, cursor_at - 1)
        elif key_press in printable:
            string_input.insert(cursor_at, key_press)
            cursor_at = min(len(string_input), cursor_at + 1)
        else:
            effects.get_effects()["honk"].play()
        if not hide:
            draw_index = max(0, min(len(string_input) - max_width, cursor_at - max_width + draw_index))
            text_area["text"] = "".join(string_input[draw_index:draw_index + min(len(string_input), max_width)])
            draw_text_box(text_area=text_area, overwrite=True)
            cursor.cursor_set(min(max_width + column, max(column, column + cursor_at - draw_index)), row)
        return None

    return update_text_input


def main():
    """
    Drive the program.
    """
    clear_screen()
    print("Press escape or tab to go to test text_input")
    key_input = init_key_input()
    while True:
        key_input["key_get"](key_input)
        key_press = pull_input(key_input)[0]
        if not key_press:
            continue
        elif key_press in ("escape", "tab", "backspace"):
            break
        elif key_press in ("left", "right", "up", "down"):
            cursor.cursor_shift(key_press)
        else:
            print(key_press, end="", flush=True)
    draw_text_box(text_area={
        "column": 1, "row": 10, "width": 12, "height": 1,
        "text": "User input:"
    })
    text_input = start_text_input(13, 10, 25, hide=False)
    while True:
        key_input["key_get"](key_input)
        pressed = pull_input(key_input)[0]
        if pressed == "tab":
            break
        prompt_result = text_input(pressed)

        draw_text_box(text_area={
            "column": 30, "row": 2, "width": 12, "height": 1,
            "text": pressed}, flush_output=True)
        if not prompt_result is None:
            draw_text_box(text_area={
                "column": 1, "row": 2, "width": 12, "height": 1,
                "text": "\n".join(prompt_result)})
            break


if __name__ == '__main__':
    main()
